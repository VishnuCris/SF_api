import os
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS
import secrets
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
 	create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import werkzeug
from SF_api.logging import setup_logger
from SF_api.config import Config
from flask_mail import Mail, Message
import logging,logging.config
import traceback

app = Flask(__name__,static_folder='static')

with app.app_context():
    app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
    app.config.from_object(Config)
    # app.config.from_pyfile(app.config['BASE_PATH']+'/../config_values.py')
    
    # mail instance
    mail = Mail(app)
    
    # jwt instance
    jwt = JWTManager(app)

    # cors setup
    CORS(app, resources={
        r"/api/*": {
            "origins": [app.config['UI_DOMAIN']],
            "methods": ["GET", "POST"],
            "headers": ["Content-Type"],
            "supports_credentials": True
        }
    })

    # logs
    errorlog = setup_logger('error',f"{app.config['BASE_PATH']}/logs/error.log")
    alllog = setup_logger('info',f"{app.config['BASE_PATH']}/logs/app.log")

    # routes
    from .Routes.routes import routes
    app.register_blueprint(routes,url_prefix='/api')

    # request handlers
    @app.after_request
    def after_request(response):
        alllog.info('########### ALL LOGS ##########')
        alllog.info(response.get_json())
        return response

    @app.errorhandler(Exception)
    def handle_bad_request(e):
        errorlog.info('########### ERRORS LOGS ##########')
        errorlog.error(e,exc_info=True)
        return jsonify({'message':str(e),'status':False,'status_code':500})

