from app 	import app
from flask 	import render_template

@app.route( '/login', methods = [ 'GET' ] )
def show_login_form():
	return 'login'


@app.route( '/signup', methods = [ 'GET' ] )
def show_signup_form():
	return 'signup'
