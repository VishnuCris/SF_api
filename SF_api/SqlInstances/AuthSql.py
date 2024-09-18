
from SF_api.Database.baseService import DBService
from werkzeug.security import generate_password_hash,check_password_hash


class AuthSql:
	def __init__(self,DB=None):
		if DB:
			self.DB = DB
		else:
			self.DB = DBService()

	def register(self):
		pass

	def validate_email(self,data):
		email_sql = """select id from users where email = %s"""
		data_to_select = (data['email'],)
		return self.DB.selectWithPrepared(email_sql, data_to_select,True)

	def validate_mobile(self,data):
		email_sql = """select id from users where mobile = %s"""
		data_to_select = (data['mobile'],)
		return self.DB.selectWithPrepared(email_sql, data_to_select,True)

	def validate_password(self,data):
		email_sql = """select * from users where password = %s and (email = %s or mobile = %s)"""
		data_to_select = (data.get('password'),data.get('email'),data,get('mobile'))
		return self.DB.selectWithPrepared(email_sql, data_to_select,True)

	def check_user_exists(self,data):
		user_exists = """ select * from users where email = %s or mobile = %s """
		data_to_select = (data.get('email'),data.get('mobile'))
		return self.DB.selectWithPrepared(user_exists, data_to_select,True)

	def create_user(self,data):
		create_sql = """ insert into users (name,email,mobile,password,google_auth_secret) values (%s,%s,%s,%s,%s) """
		insert_data = (data.get('name'),data.get('email'),data.get('mobile'),data.get('password'),data.get('google_auth_secret'))
		self.DB.executeWithPrepared(create_sql,insert_data)

	def get_user(self,data):
		user_exists = """ select * from users where email = %s or mobile = %s """
		data_to_select = (data.get('email'),data.get('mobile'))
		return self.DB.selectWithPrepared(user_exists, data_to_select,True)

	def validate_otp(self,data):
		otp_validation = """ select * from otps where otp = %s and (mobile = %s or email = %s) order by id desc limit 1"""
		data_to_select = (data.get('otp'),data.get('mobile'),data.get('email'))
		otp_data = self.DB.selectWithPrepared(otp_validation, data_to_select,True)
		if otp_data:
			self.DB.executeWithPrepared(""" delete from otps where id = %s """,(otp_data.get('id'),))
		return otp_data

	def change_password(self,data):
		if data.get('mobile'):
			update_sql = """ update users set password = %s where mobile = %s """
			update_data = (data.get('password'),data.get('mobile'))
		elif data.get('email'):
			update_sql = """ update users set password = %s where email = %s """
			update_data = (data.get('password'),data.get('email'))
		else:
			raise Exception("Either mobile nor email id is present in request")

		self.DB.executeWithPrepared(update_sql,update_data)

	def check_user_with_password(self,data):
		user_exists = """ select * from users where (email = %s or mobile = %s)"""
		data_to_select = (data.get('email'),data.get('mobile'))
		row = self.DB.selectWithPrepared(user_exists, data_to_select,True)
		if row and check_password_hash(row.get('password'),data.get('password')):
			return row
		return None