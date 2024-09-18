from SF_api import mail, app
from flask_mail import Message
from flask import current_app
import threading
from time import sleep

class MailService:
    def __init__(self):
        pass

    def send_mail(self, data):
        msg = Message(data.get('subject'), sender=data.get('sender'), recipients=data.get('recipients'))
        msg.html = data.get('message')
        
        email_thread = threading.Thread(target=self.send_email_in_thread, args=(msg,))
        email_thread.start()

    def send_email_in_thread(self, msg):
        with app.app_context():
        	mail.send(msg)
