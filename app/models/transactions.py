import sqlite3
from .database import database
class transactions(database):
	def __init__(self):
		database.__init__(self)
		# useful for prototyping, since redeploying the database is easy:
		# just delete and re-run any code that uses this class
		try:
			result = self.cursor.execute("select count(rowid) from transactions").fetchall()
			self.total_count = result[0]["count(rowid)"]
		except sqlite3.OperationalError as e:
			#primary keys are (sort of) auto increment by default
			self.cursor.execute("create table transactions ( user_id integer not null, pet_id integer not null, is_liked bool, primary key(user_id, pet_id))")

	def get_likes_by_user(self, user_id):
		query = 'select pet_id from transactions where user_id = ?'
		result = self.cursor.execute(query, [user_id]).fetchall()
		return result

	def toggle(self, user_id, pet_id):
		query = 'select is_liked from transactions where user_id = ? and pet_id = ?'
		result = self.cursor.execute(query, [user_id, pet_id]).fetchone()
		if result:
			self.__delete(user_id, pet_id)
		else:
			self.__insert(user_id, pet_id)

	def __insert(self, user_id, pet_id):

		query = 'insert into transactions ( user_id, pet_id, is_liked) values( ?, ?, 1)'
		self.cursor.execute(query, [user_id, pet_id])
		self.conn.commit()
		

	def __delete(self, user_id, pet_id):
		query = 'delete from transactions where user_id = ? and pet_id = ?'
		self.cursor.execute(query, [user_id, pet_id])
		self.conn.commit()