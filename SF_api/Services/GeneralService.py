
from SF_api.Services.HelperService import HelperService
from SF_api.SqlInstances.GeneralSql import GeneralSql
from SF_api.SqlInstances.AuthSql import AuthSql
from SF_api import app
from flask import make_response, render_template
from SF_api.Database.baseService import DBService
from SF_api.Services.MailService import MailService
import traceback

class GeneralService:
	def __init__(self,DB=None):
		if DB:
			self.DB = DB
		else:
			self.DB = DBService()
		self.generalSql = GeneralSql(self.DB)
		self.authSql = AuthSql(self.DB)
		self.HelperService = HelperService()
		self.MailService = MailService()

	def generate_otp(self,data):
		try:
			otp = HelperService.generate_otp()
			self.DB.Begin()
			self.generalSql.generate_otp({'otp':otp,'mobile':data.get('mobile'),'customer_id':data.get('customer_id'),'email':data.get('email')})
			self.DB.Commit()
			if data.get('email'):
				template_data = {'name':data.get('email'),'otp':otp}
				rendered_template = render_template("send_login_otp.html",data=template_data)
				mail_data = {
					'sender':'vishnunmms@gmail.com',
					'recipients':[data.get('email')],
					'subject':'Login verification email',
					'message':rendered_template,
				}
				self.MailService.send_mail(mail_data)
			return otp
		except Exception as e:
			self.DB.Rollback()
			raise Exception(e)

	def otp_request(self,data):
		verified_user = self.authSql.check_user_exists(data)
		otp_generated = self.generate_otp({'mobile':data.get('mobile'),'customer_id':verified_user.get('id') if verified_user else None,'email':data.get('email')})
		return self.HelperService.success_response({'otp':otp_generated})
