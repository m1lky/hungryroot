import sqlite3
from .database import database
# from flask import current_app as app
import os
class pets(database):
	def __init__(self):
		database.__init__(self)
		# useful for prototyping, since redeploying the database is easy:
		# just delete and re-run any code that uses this class
		try:
			result = self.cursor.execute("select count(rowid) from pets").fetchall()
			self.total_count = result[0]["count(rowid)"]
		except sqlite3.OperationalError as e:
			#sqlite adds primary keys by default
			self.cursor.execute("create table pets ( name text, image text, species text, breed text, age integer, price real)")
			self.total_count = 0
	# params should be passed in the format of 
	# {column: "operation value", ...}
	def get_pets(self, params=[]):
		#todo: add join here for the pet likes
		query = "select rowid, *  from pets"
		if params:
			where_clause = " where"
			for key, val in params.items():
				where_clause += " " + key + " " + val + " and "
			where_clause = where_clause[:-4] # strip the last 'and'
			query += where_clause
		result = self.cursor.execute(query).fetchall()
		return result

	def insert(self, params):
		query = 'insert into pets ( name, image, species, breed, age, price) values( ?, ?, ?, ?, ?, ?)'
		self.cursor.execute(query, params)
		self.conn.commit()

	#accepts a dictionary to update rowid with
	def update(self, params, rowid):
		if not rowid or not params:
			return False
		#compose query
		query = 'update pets set ';
		for index, value in params.items():
			query += index + " = ?, "
		query = query[0:-2] + " where rowid = ?"
		values = [params[k] for k in params]
		values.append(rowid)
		print(query)
		print(values)
		self.cursor.execute(query, values)
		self.conn.commit()

	def delete(self, rowid):
		query = "select image from pets where rowid = ?"
		result = self.cursor.execute(query, [rowid]).fetchone()
		try:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], result['image']))
		except:
			print("image not found:", result['image'])
		query = "delete from pets where rowid = ?"
		self.cursor.execute(query, [rowid])
		self.conn.commit()


