# from app import app
from SF_api import app
# from waitress import serve

if __name__ == '__main__':
	if app.config['ENV'] == 'production':
		serve(app,port=app.config['PORT'],host=app.config['HOST'])
	else:
		app.run(debug=True,port=app.config['PORT'],host=app.config['HOST'])