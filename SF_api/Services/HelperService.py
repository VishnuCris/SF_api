
from werkzeug.security import generate_password_hash,check_password_hash
import random
from flask import make_response, jsonify

class HelperService:

	@staticmethod
	def hash_password(password):
		return generate_password_hash(password,  method='pbkdf2:sha256')

	@staticmethod
	def generate_otp():
		random_six_digit_number = random.randint(100000, 999999)
		return random_six_digit_number

	@staticmethod
	def success_response(parameters):
		return make_response({
					'status':True,
					'status_code':200,
					'data':parameters
				})

	@staticmethod
	def error_response(parameters):
		return make_response({
					'status':False,
					'status_code':500,
					'data':parameters
				})


