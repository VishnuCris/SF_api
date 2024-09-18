
import mysql.connector
from SF_api import app

class DBService:
	def __init__(self):
		self.conn = mysql.connector.connect(user = app.config['DB_USERNAME'],
                               host = app.config['DB_HOST'],
                              database = app.config['DB_DATABASE'],
                              port = app.config['DB_PORT'],
                              password=app.config['DB_PASSWORD']
                              )
		self.cursor = self.conn.cursor(dictionary=True)

	def closeConnection(self):
		# if self.conn:
		# 	self.conn.close()
		pass

	def select(self,sql):
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		self.closeConnection()
		return rows

	def execute(self,sql):
		rows = self.cursor.execute(sql)
		self.closeConnection()
		return rows

	def selectWithPrepared(self,sql,values,single_data = False):
		self.cursor.execute(sql,values)
		rows = self.cursor.fetchall()
		if single_data:
			row = rows[0] if rows and len(rows) else None
			return row
		self.closeConnection()
		return rows
	def executeWithPrepared(self,sql,values):
		self.cursor.execute(sql,values)
		self.closeConnection()

	def Begin(self):
		self.cursor.execute('start transaction')

	def Commit(self):
		self.cursor.execute('commit')

	def Rollback(self):
		self.cursor.execute('rollback')
