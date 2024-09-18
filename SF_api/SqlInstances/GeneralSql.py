from SF_api.Database.baseService import DBService
from werkzeug.security import generate_password_hash,check_password_hash


class GeneralSql:
	def __init__(self,DB=None):
		if DB:
			self.DB = DB
		else:
			self.DB = DBService()

	def generate_otp(self,data):
		create_sql = """ insert into otps (customer_id,mobile,otp,email) values (%s,%s,%s,%s) """
		insert_data = (data.get('customer_id'),data.get('mobile'),data.get('otp'),data.get('email'))
		self.DB.executeWithPrepared(create_sql,insert_data)
