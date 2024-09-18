# from SF_api import current_app as app
from SF_api.Controllers.AuthController import AuthController
from .routes import routes
from flask import request
from flask_jwt_extended import (
    jwt_required
)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = None
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator

@routes.post('/auth/register')
def register():
	authController = AuthController()
	response = authController.register(request.get_json())
	return response

@routes.post('/auth/auth_request')
def auth_otp_request():
    authController = AuthController()
    resp = authController.auth_request(request.get_json())
    return resp

@routes.post('/auth/authenticate')
def authenticate():
    authController = AuthController()
    resp = authController.authenticate(request.get_json())
    return resp

@routes.post('/auth/google_authenticate')
def google_auth_validate():
    authController = AuthController()
    resp = authController.google_auth_validate(request.get_json())
    return resp

@routes.post('/auth/change_password')
def change_password():
    authController = AuthController()
    resp = authController.change_password(request.get_json())
    return resp

@routes.route('auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    authController = AuthController()
    resp = authController.refresh(request.get_json())
    return resp

@routes.post('/auth/signout')
@jwt_required()
def signout():
    authController = AuthController()
    response = authController.signout(request.get_json())
    return response