
# from SF_api.Services.services import hashPassword
from SF_api import app
from flask import make_response, render_template
from flask_jwt_extended import (
	create_access_token,create_refresh_token,
	set_refresh_cookies,set_access_cookies,
	get_csrf_token,jwt_required,unset_jwt_cookies,get_jwt_identity
)
from werkzeug.security import generate_password_hash,check_password_hash
from SF_api.SqlInstances.AuthSql import AuthSql
from SF_api.Database.baseService import DBService
from SF_api.Services.HelperService import HelperService
from SF_api.Services.GeneralService import GeneralService
from SF_api.Services.MailService import MailService

import pyotp
import base64
import qrcode
from io import BytesIO
import os

class AuthService:
	def __init__(self):
		self.DB = DBService()
		self.authSql = AuthSql(self.DB)
		self.GeneralService = GeneralService(self.DB)
		self.HelperService = HelperService()
		self.MailService = MailService()

	def auth_request(self,data):
		verified_user = self.authSql.check_user_exists(data)
		if not verified_user:
			return self.HelperService.error_response({'status':False,'message':'You are not registered with us'})
		
		# if data.get('password'):
		verified_user = self.authSql.check_user_with_password(data)
		if not verified_user:
			return self.HelperService.error_response({'status':False,'message':'Wrong password'})

		if data.get('flag') == 'google_auth':
			# qr_code_url = self.google_auth_request({'verified_user':verified_user})
			# return self.HelperService.success_response({'message':'redirect_to_google_auth_otp_page','qr_code_url':qr_code_url})
			return self.HelperService.success_response({'message':'redirect_to_google_auth_otp_page'})

		otp_generated = self.GeneralService.generate_otp({'mobile':data.get('mobile'),'customer_id':verified_user.get('id'),'email':data.get('email')})
		
		if data.get('email'):
			template_data = {'name':verified_user.get('name'),'otp':otp_generated}
			rendered_template = render_template("send_login_otp.html",data=template_data)
			mail_data = {
				'sender':'vishnunmms@gmail.com',
				'recipients':[verified_user.get('email')],
				'subject':'Login verification email',
				'message':rendered_template,
			}
			self.MailService.send_mail(mail_data)
		return self.HelperService.success_response({'otp':otp_generated})


	def authenticate(self,data):
		otp_validation = self.authSql.validate_otp(data)
		if otp_validation:
			user = self.authSql.check_user_exists(data)
			if user:
				access_token = create_access_token(identity=user.get('id'))
				csrf_token = get_csrf_token(access_token)
				response = self.HelperService.success_response({'message':'Logged in succesfully','csrf_token':csrf_token})
				set_access_cookies(response, access_token)
				return response
			return self.HelperService.error_response({'message':'wrong password'})
		return self.HelperService.error_response({'message':'Invalid Otp'})

	def change_password(self,data):
		try:
			otp_validation = self.authSql.validate_otp(data)
			if otp_validation:
				verified_user = self.authSql.check_user_exists(data)
				if verified_user:
					data['password'] = HelperService.hash_password(data.get('password'))
					self.DB.Begin()
					change_password = self.authSql.change_password(data)
					self.DB.Commit()
					return self.HelperService.success_response({'message':'password updated succesfully'})
				return self.HelperService.error_response({'message':'Mobile number not registered with us'})
			return self.HelperService.error_response({'message':'Invalid Otp'})
		except Exception as e:
			self.DB.Rollback()
			raise Exception(e)

	def google_auth_request(self,data):
		try:
			verified_user = data.get('verified_user')

			# get google auth secret from users table
			secret = verified_user.get('google_auth_secret')

			# Generate a provisioning URI
			otp = pyotp.TOTP(secret)
			provisioning_uri = otp.provisioning_uri(name=verified_user['email'], issuer_name="Sample App")

			# make qrcode directory if exists
			if not os.path.exists(f"{os.getcwd()}/{app.config['FLASK_APP_FOLDER']}/static/qrcodes/"):
				os.makedirs(f"{os.getcwd()}/{app.config['FLASK_APP_FOLDER']}/static/qrcodes/")
			
			# Generate a QR code
			img = qrcode.make(provisioning_uri)
			qr_code_path = f"{os.getcwd()}/{app.config['FLASK_APP_FOLDER']}/static/qrcodes/{verified_user['mobile']}.png"
			img.save(qr_code_path)

			return f"{app.config['DOMAIN_URL']}static/qrcodes/{verified_user['mobile']}.png"
		except Exception as e:
			self.DB.Rollback()
			raise Exception(e)

	def google_auth_validate(self,data):
		try:
			verified_user = self.authSql.check_user_exists(data)
			if not verified_user:
				return self.HelperService.error_response({'message':'you are not registered with us'})

			#secret = verified_user.get('google_auth_secret')
			secret = app.config['GOOGLE_AUTH_SECRET']
			otp = pyotp.TOTP(secret)
			if otp.verify(data.get('google_otp')):
				# remove qrcode file after verification
				qr_code_path = f"{os.getcwd()}/{app.config['FLASK_APP_FOLDER']}/static/qrcodes/{verified_user['mobile']}.png"
				if os.path.isfile(qr_code_path):
					os.remove(qr_code_path)

				# access token generation
				access_token = create_access_token(identity=verified_user.get('id'))
				csrf_token = get_csrf_token(access_token)
				response = self.HelperService.success_response({'message':'google authenticated','csrf_token':csrf_token})
				set_access_cookies(response, access_token)
				return response
			else:
				return self.HelperService.error_response({'message':'code not matched'})
		except Exception as e:
			self.DB.Rollback()
			raise Exception(e)

	def register(self,data):
		try:
			check_user = self.authSql.check_user_exists(data)
			if check_user:
				return self.HelperService.error_response({'message':'You have already registered, please sign in.'})

			otp_validation = self.authSql.validate_otp(data)
			if not otp_validation:
				return self.HelperService.error_response({'message':'Invalid otp'})

			''' Hashing password '''
			data['password'] = HelperService.hash_password(data['password'])

			# Generate a new TOTP secret for the user
			secret = pyotp.random_base32()
			data['google_auth_secret'] = secret

			self.DB.Begin()
			self.authSql.create_user(data)
			self.DB.Commit()
			
			''' token generation '''
			user = self.authSql.get_user(data)
			access_token = create_access_token(identity=user.get('id'))
			response = self.HelperService.success_response({'msg':'Registered Succesfully','access_token':access_token})
			set_access_cookies(response, access_token)
			return response
		except Exception as e:
			self.DB.Rollback()
			raise Exception(e)

	def signout(self,data):
		response = self.HelperService.success_response({'msg':'logged out successfully'	})
		unset_jwt_cookies(response)
		return response