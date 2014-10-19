from functools 	import wraps
from flask 		import session, request, redirect, url_for

import string
import random
import hashlib
import base64

def login_required( f ):
    @wraps( f )
    def decorated_function( *args, **kwargs ):
        if session.get( "email" ) is None:
            return redirect( url_for( 'show_login_form', next = request.url ) )
        return f( *args, **kwargs )
    return decorated_function


def hashfunc( str ):
	return base64.b64encode( hashlib.sha512( str.encode() ).hexdigest() )


def randomString( len ):
	return ''.join( [ random.choice( string.ascii_letters + string.digits + '\\+' ) 
					  for _ in range( 0, len ) ] )
