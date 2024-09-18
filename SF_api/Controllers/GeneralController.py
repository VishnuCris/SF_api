
from SF_api.Services.GeneralService import GeneralService

class GeneralController:

	def __init__(self):
		self.generalService = GeneralService()

	def generate_otp(self,data):
		self.generalService = GeneralService()
		return self.generalService.generate_otp(data)

	def otp_request(self,data):
		self.generalService = GeneralService()
		return self.generalService.otp_request(data)

