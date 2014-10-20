from app 	import app
from models import User
from flask 	import render_template, session, request, jsonify, make_response
from utils 	import login_required



# User API

@app.route( '/login', methods = [ 'POST' ] )
def validate_user():

	email = request.json.get( 'email' )
	password = request.json.get( 'password' )

	responseDict = {}

	if( email is not None and password is not None ):

		try:
			user = User.validate( email, password )
			session[ "user" ] = user
			
			responseDict[ "message" ] = "Successfully logged in"
			responseDict[ "code" ] = 200

		except User.DoesNotExist:
			responseDict[ "message" ] = "No user with given email"
			responseDict[ "code" ] = 403


	else:
		responseDict[ "message" ] = "Bad request"
		responseDict[ "code" ] = 400

	return make_response( jsonify( responseDict ), responseDict[ "code" ] )



@app.route( '/signup', methods = [ 'POST' ] )
def create_user():
	
	email = request.json.get( 'email' )
	password = request.json.get( 'password' )
	password2 = request.json.get( 'password2' )

	if( email is not None and password is not None and password2 is not None ):

		if( password == password2 ):

			try:
				user = User.createNew( email, password )

				responseDict[ "message" ] = "Successfully signed up"
				responseDict[ "code" ] = 200

			except User.IntegrityError:
				responseDict[ "message" ] = "Conflict"
				responseDict[ "code" ] = 409

		else:
			responseDict[ "message" ] = "Bad request: Passwords do not match"
			responseDict[ "code" ] = 400


	else:
		responseDict[ "message" ] = "Bad request: Data error"
		responseDict[ "code" ] = 400

	return make_response( jsonify( responseDict ), responseDict[ "code" ] )



@app.route( '/logout', methods = [ 'GET' ] )
@login_required
def logout_user():

	session.clear();
	responseDict[ "code" ] = 200
	responseDict[ "message" ] = "Successfully logged out"

	return make_response( jsonify( responseDict ), responseDict[ "code" ] )



# Note API

@app.route( '/note/<note_id:int>', methods = [ 'POST' ] )
@login_required
def get_note( note_id ):
	pass



@app.route( '/note', methods = [ 'POST' ] )
@login_required
def add_note():

	title = request.json.get( 'title' )
	content = request.json.get( 'content' )
	tags = request.json.get( 'tags' )
	category_id = request.json.get( 'category_id' )

	user = session[ "user" ]

	if( title is not None and content is not None and category_id is not None ):

		try:
			Note.addNew( title, content, tags, category_id, user )
			responseDict[ "code" ] = 200
			responseDict[ "message" ] = "Successfully added a new note"

		except ValueError:
			responseDict[ "code" ] = 400
			responseDict[ "message" ] = "Bad request: No such category"

	else:
		responseDict[ "code" ] = 400
		responseDict[ "message" ] = "Bad request: Data error"

	return make_response( jsonify( responseDict ), responseDict[ "code" ] )



@app.route( '/note/<note_id:int>', methods = [ 'PUT' ] )
@login_required
def edit_note( note_id ):
	pass



@app.route( '/note/<note_id:int>', methods = [ 'DELETE' ] )
@login_required
def delete_note( note_id ):
	pass



# Category API

@app.route( '/category/<cat_id:int>', methods = [ 'GET' ] )
@login_required
def get_category():
	pass

	

@app.route( '/category', methods = [ 'POST' ] )
@login_required
def add_category():
	pass



@app.route( '/category/<cat_id:int>', methods = [ 'PUT' ] )
@login_required
def edit_category():
	pass



@app.route( '/category/<cat_id:int>', methods = [ 'DELETE' ] )
@login_required
def delete_category():
	pass



@app.route( '/categories', methods = [ 'GET' ] )
@login_required
def list_categories():
	pass

# Search API
