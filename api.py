from app 	import app
from flask 	import render_template
from utils 	import login_required

# User API

@app.route( '/login', methods = [ 'POST' ] )
def validate_login():
	
