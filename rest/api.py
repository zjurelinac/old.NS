from app 	import app
from models import User
from peewee import IntegrityError
from flask 	import render_template, session, request
from utils 	import login_required, rest_respond



# User API

@app.route( '/login', methods = [ 'POST' ] )
def validate_user():

	responseDict = {}

	if( session.get( "user_id" ) is not None ):
		responseDict[ "message" ] = "Collision: Already logged in."
		responseDict[ "code" ] = 409

	elif( request.json is not None ):

		email = request.json.get( 'email' )
		password = request.json.get( 'password' )


		if( email is not None and password is not None ):

			try:
				user = User.validate( email, password )

				if( user is None ):
					responseDict[ "message" ] = "Unauthorized: Wrong password."
					responseDict[ "code" ] = 403

				else:
					session[ "user_id" ] = user.id
					session[ "user_email" ] = user.email

					responseDict[ "message" ] = "OK: Successfully logged in."
					responseDict[ "code" ] = 200

			except User.DoesNotExist:
				responseDict[ "message" ] = "Unauthorized: No user with given email."
				responseDict[ "code" ] = 403


		else:
			responseDict[ "message" ] = "Bad request: Data error."
			responseDict[ "code" ] = 400

	else:
		responseDict[ "message" ] = "Bad request: No JSON data sent."
		responseDict[ "code" ] = 400


	return rest_respond( responseDict )



@app.route( '/signup', methods = [ 'POST' ] )
def create_user():

	responseDict = {}

	if( request.json is not None ):

		email = request.json.get( 'email' )
		password = request.json.get( 'password' )
		password2 = request.json.get( 'password2' )

		if( email is not None and password is not None and password2 is not None ):

			if( password == password2 ):

				try:
					user = User.createNew( email, password )

					responseDict[ "message" ] = "Created: Successfully signed up."
					responseDict[ "code" ] = 201

				except IntegrityError:
					responseDict[ "message" ] = "Conflict: Email already exists."
					responseDict[ "code" ] = 409

			else:
				responseDict[ "message" ] = "Bad request: Passwords do not match."
				responseDict[ "code" ] = 400


		else:
			responseDict[ "message" ] = "Bad request: Data error."
			responseDict[ "code" ] = 400

	else:
		responseDict[ "message" ] = "Bad request: No JSON data sent."
		responseDict[ "code" ] = 400

	return rest_respond( responseDict )



@app.route( '/logout', methods = [ 'GET' ] )
@login_required
def logout_user():

	session.clear();

	responseDict[ "code" ] = 200
	responseDict[ "message" ] = "OK: Successfully logged out."

	return rest_respond( responseDict )



# Note API

@app.route( '/note/<int:note_id>', methods = [ 'POST' ] )
@login_required
def get_note( note_id ):

	responseDict = {}

	user_id = session[ "user_id" ]

	try:
		note = Note.getNoteObject( note_id, user_id )

		responseDict[ "note" ] = note
		responseDict[ "message" ] = "OK: Successfully retirieved a note"
		responseDict[ "code" ] = 200


	except Note.DoesNotExist:
		responseDict[ "message" ] = "Not found: No note with a given id."
		responseDict[ "code" ] = 404

	rest_respond( responseDict )



@app.route( '/note', methods = [ 'POST' ] )
@login_required
def add_note():

	responseDict = {}

	if( request.json is not None ):

		title = request.json.get( 'title' )
		content = request.json.get( 'content' )
		tags = request.json.get( 'tags' )
		category_id = request.json.get( 'category_id' )

		user_id = session[ "user_id" ]

		if( title is not None and content is not None and category_id is not None ):

			try:
				Note.addNote( title, content, tags, category_id, user_id )
				responseDict[ "message" ] = "Successfully added a new note."
				responseDict[ "code" ] = 200

			except ValueError:
				responseDict[ "message" ] = "Bad request: No such category."
				responseDict[ "code" ] = 400

		else:
			responseDict[ "message" ] = "Bad request: Data error."
			responseDict[ "code" ] = 400

	else:
		responseDict[ "message" ] = "Bad request: No JSON data sent."
		responseDict[ "code" ] = 400

	return rest_respond( responseDict )



@app.route( '/note/<int:note_id>', methods = [ 'PUT' ] )
@login_required
def edit_note( note_id ):

	responseDict = {}

	if( request.json is not None ):

		title = request.json.get( 'title' )
		content = request.json.get( 'content' )
		tags = request.json.get( 'tags' )
		category_id = request.json.get( 'category_id' )

		user_id = session[ "user_id" ]

		if( title is not None and content is not None and category_id is not None ):

			try:
				Note.editNote( note_id, title, content, tags, category_id, user_id )
				responseDict[ "message" ] = "Successfully added a new note."
				responseDict[ "code" ] = 200

			except ValueError:
				responseDict[ "message" ] = "Bad request: No such category."
				responseDict[ "code" ] = 400

		else:
			responseDict[ "message" ] = "Bad request: Data error."
			responseDict[ "code" ] = 400

	else:
		responseDict[ "message" ] = "Bad request: No JSON data sent."
		responseDict[ "code" ] = 400

	return rest_respond( responseDict )



@app.route( '/note/<int:note_id>', methods = [ 'DELETE' ] )
@login_required
def delete_note( note_id ):

	responseDict = {}

	if( request.json is not None ):

		title = request.json.get( 'title' )
		content = request.json.get( 'content' )
		tags = request.json.get( 'tags' )
		category_id = request.json.get( 'category_id' )



# Category API

@app.route( '/category/<int:cat_id>', methods = [ 'GET' ] )
@login_required
def get_category():
	pass



@app.route( '/category', methods = [ 'POST' ] )
@login_required
def add_category():
	pass



@app.route( '/category/<int:cat_id>', methods = [ 'PUT' ] )
@login_required
def edit_category():
	pass



@app.route( '/category/<int:cat_id>', methods = [ 'DELETE' ] )
@login_required
def delete_category():
	pass



@app.route( '/categories', methods = [ 'GET' ] )
@login_required
def list_categories():
	pass

# Search API


# Debug API

@app.route( '/debug/sess_dump', methods = [ 'GET' ] )
def sess_dump():
	#session[ 'hello' ] = 'world'
	responseDict = { "code" : 200, "session" : [ ( k, session[ k ] ) for k in session ],
					 "user" : [ session.get( "user_id" ), session.get( "user_email" ) ] }
	return rest_respond( responseDict )
