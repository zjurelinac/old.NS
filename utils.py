from functools 	import wraps
from flask 		import session, request, redirect, url_for, make_response, jsonify

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
			return rest_respond( responseDict )
		
		return f( *args, **kwargs )
	return decorated_function


def rest_respond( rdict ):
	if( rdict is None ): 
		abort( 500 )
	return make_response( jsonify( rdict ), rdict.get( "code" ) )

def hashfunc( str ):
	return base64.b85encode( hashlib.sha512( str.encode() ).digest() )


def random_string( len ):
	return ''.join( [ random.choice( string.ascii_letters + string.digits + '\\+' ) 
					  for _ in range( 0, len ) ] )

