from app 	import app
from flask 	import render_template, abort
from utils 	import login_required

@app.route( '/login', methods = [ 'GET' ] )
def show_login_form():
	return render_template( "login.html" )


@app.route( '/signup', methods = [ 'GET' ] )
def show_signup_form():
	return render_template( "signup.html" )


#@app.route( '/', methods = [ 'GET' ] )
#@login_required
#def index():
#	return 'index'

@app.errorhandler( 404 )
def page_not_found( e ):
	return render_template( "errors/404.html", error = e ), 404

@app.errorhandler( 403 )
def forbidden_access( e ):
	return render_template( "errors/403.html", error = e ), 403


@app.errorhandler( 500 )
def forbidden_access( e ):
	return render_template( "errors/500.html" ), 500


