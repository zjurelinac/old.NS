"""
	app.py

	Application configuration and intialization,
	database settings
"""

from flask 				import Flask
from peewee 			import *

import os

APP_ROOT = os.path.dirname( os.path.realpath( __file__ ) )
DATABASE = os.path.join( APP_ROOT, 'database.db' )
DEBUG = True

app = Flask( __name__ )
app.config.from_object( __name__ )
db = SqliteDatabase( app.config[ 'DATABASE' ], threadlocals = True )
