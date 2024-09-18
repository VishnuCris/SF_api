from flask import (
	Blueprint,current_app as app,jsonify,request,g,session,make_response
)
from functools import wraps
from flask_jwt_extended import (
	set_access_cookies,set_refresh_cookies,
	jwt_required,unset_jwt_cookies
)
routes = Blueprint('routes',__name__)
from .authRoute import *
from .generalRoute import *




