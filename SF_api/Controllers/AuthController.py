
from SF_api.Services.AuthService import AuthService

class AuthController:

	def __init__(self):
		self.authService = AuthService()

	def register(self,data):
		return self.authService.register(data)
		
	def authenticate(self,data):
		return self.authService.authenticate(data)

	def auth_request(self,data):
		return self.authService.auth_request(data)

	def change_password(self,data):
		return self.authService.change_password(data)

	def google_auth_request(self,data):
		return self.authService.google_auth_request(data)

	def google_auth_validate(self,data):
		return self.authService.google_auth_validate(data)

	def signout(self,data):
		return self.authService.signout(data)



