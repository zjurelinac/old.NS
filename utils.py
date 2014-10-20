from functools 	import wraps
from flask 		import session, request, redirect, url_for

import string
import random
import hashlib
import base64

def login_required( f ):
	@wraps( f )
	def decorated_function( *args, **kwargs ):
		if session.get( "user" ) is None:

			responseDict[ "code" ] = 403
			responseDict[ "message" ] = "Unauthorized access"
			return make_response( jsonify( responseDict ), responseDict[ "code" ] )
		
		return f( *args, **kwargs )
	return decorated_function


def hashfunc( str ):
	return base64.b64encode( hashlib.sha512( str.encode() ).hexdigest() )


def random_string( len ):
	return ''.join( [ random.choice( string.ascii_letters + string.digits + '\\+' ) 
					  for _ in range( 0, len ) ] )
