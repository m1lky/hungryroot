import sqlite3
from .database import database
class users(database):
	def __init__(self):
		database.__init__(self)
		# useful for prototyping, since redeploying the database is easy:
		# just delete and re-run any code that uses this class
		try:
			result = self.cursor.execute("select count(rowid) from users").fetchall()
			self.total_count = result[0]["count(rowid)"]
		except sqlite3.OperationalError as e:
			#primary keys are (sort of) auto increment by default
			self.cursor.execute("create table users ( fname text, lname text, email text, address1 text, address2 text, city text, state text, phone text, password text, is_admin bool default false)")
			self.total_count = 0

	def get_all_users(self):
		query = 'select *,rowid from users'
		result = self.cursor.execute(query).fetchall()
		return result

	def get_user_data(self, columns, user_id):
		query = 'select '
		for x in columns:
			query += x + " "
		query += "from users where rowid = ?"
		result = self.cursor.execute(query, [user_id]).fetchone()
		return result

	def get_login_info(self, email):
		query = 'select rowid,password,is_admin from users where email = ?'
		result = self.cursor.execute(query, [email]).fetchone()
		return result

	def insert(self, params):
		query = 'insert into users ( fname, lname, email, address1, address2, city, state, phone, password, is_admin) values( ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)'
		self.cursor.execute(query, params)
		self.conn.commit()
		return self.cursor.lastrowid
