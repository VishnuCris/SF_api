# from SF_api import current_app as app
from SF_api.Controllers.GeneralController import GeneralController
from .routes import routes
from flask import request, make_response
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

@routes.post('/generate_otp')
def generate_otp():
    generalController = GeneralController()
    resp = generalController.generate_otp(request.get_json())
    return resp

@routes.post('/protected')
@jwt_required()
def general_protected():
    generalController = GeneralController()
    resp = make_response({'status':True,'data':[]})
    return resp

@routes.post('/otp_request')
def otp_request():
    generalController = GeneralController()
    resp = generalController.otp_request(request.get_json())
    return resp

@routes.post('/list')
@jwt_required()
def master():
    print(get_jwt_identity())
    response = make_response({'status':True,'messsage':'12345'})
    return response