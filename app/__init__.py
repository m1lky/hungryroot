from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
from .models import pets, users, transactions
import random as rand
import bcrypt
import json
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/images/'
app.secret_key = '6a204bd89f3c8348afd5c77c717a097a' # random md5 hash

@app.route('/')
def index():
	pets_table = pets()
	pets_list = pets_table.get_pets()
	print(session)
	user_info = []
	if 'user_id' in session:
		transactions_table = transactions()
		liked_pets = transactions_table.get_likes_by_user(session['user_id'])
		# i feel terrible about this:
		liked_pets = [x['pet_id'] for x in liked_pets ]
		for p in pets_list:
			if p['rowid'] in liked_pets:
				p['is_liked'] = True
			else:
				p['is_liked'] = False
		
		users_table = users()
		user_info = users_table.get_user_data(['fname'], session['user_id'])
	return render_template("index.html", pets_list=pets_list, user_info=user_info)

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/login', methods=["POST"])
def login():
	if 'user_id' in session:
		return "Error: You're already logged in"
	users_table = users()
	user_info = users_table.get_login_info(request.form['email'])
	if user_info:
		post_password = request.form['password'].encode('utf-8')
		hashed = bcrypt.hashpw(post_password, user_info['password'])
		#bcrypt stores the salt in the hash, so this is how you check a password:
		if hashed == user_info['password']:
			session['user_id'] = user_info['rowid']
			if user_info['is_admin']:
				session['is_admin'] = True
			return redirect('/')
	
	return 'Error: Incorrect password'


@app.route('/sign_up', methods=["POST"])
def sign_up():
	if request.form['password1'] != request.form['password2']:
		return "Error: Passwords do not match"
	users_table = users()
	#if we have the email already, don't let them make another account
	test_for_duplicate = users_table.get_login_info(request.form['email'])
	if test_for_duplicate:
		return "Error: We already have that email in our system!"

	password = request.form['password1'].encode('utf-8') #TODO: validate information

	#bcrypt stores the salt automagically so we don't need to store it
	password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
	user = [
		request.form['fname'],
		request.form['lname'],
		request.form['email'],
		request.form['address1'],
		request.form['address2'],
		request.form['city'],
		request.form['state'],
		request.form['phone'],
		password_hash,
		]
	session['user_id'] = users_table.insert(user)
	return redirect('/')

@app.route('/admin_page')
def admin_page():
	# have to check for existence
	if 'is_admin' not in session or not session['is_admin']:
		return "403 Unauthorized"
	users_table = users()
	current_user_info = users_table.get_user_data(['fname'], session['user_id'])
	all_user_data = users_table.get_all_users()
	pets_table = pets()
	pets_list = pets_table.get_pets()
	return render_template('admin_page.html', pets_list=pets_list, user_info=current_user_info, users=all_user_data)

@app.route('/edit_pet/<rowid>')
def edit_pet(rowid):
	if 'is_admin' not in session or not session['is_admin']:
		return "403 Unauthorized"
	pets_table = pets()
	pets_table.update(request.args.to_dict(), rowid)
	return json.dumps({"rowid":rowid})

@app.route('/add_pet', methods=["POST"])
def add_pet():
	pets_table = pets();
	if 'image' not in request.files:
		flash('Error No image file')
		return redirect('/admin_page')
	image = request.files['image']
	if image.filename is '':
		flash('Error No image selected')
		return redirect('/admin_page')
	filename = secure_filename(image.filename)
	if image:
		image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	pet = [
		request.form['name'],
		filename,
		request.form['species'],
		request.form['breed'],
		request.form['age'],
		request.form['price']
		]
	pets_table.insert(pet)
	return redirect('/admin_page')

@app.route('/delete_pet')
def delete_pet():
	rowid = request.args['rowid']
	pets_table = pets()
	pets_table.delete(rowid)
	return redirect('/admin_page')

@app.route('/toggle_pet_like')
def toggle_pet_like():
	transactions_table = transactions()
	rowid = request.args['rowid']
	transactions_table.toggle(session['user_id'], rowid)
	return json.dumps({'rowid':rowid})
