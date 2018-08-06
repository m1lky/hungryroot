import sqlite3
# models inherit from this class and represent tables
class database:
	conn = None
	cursor = None
	total_count = None # totals are used for easy pagination

	# allows results to be returned as associative arrays, rather than objects
	def dict_factory(self, cursor, row):
		d = {}
		for idx,col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def __init__(self):
		self.conn = sqlite3.connect('/root/hungryroot/app/database/pet_store', timeout=10)
		self.conn.row_factory = self.dict_factory
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()
