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
SECRET_KEY = "_2j%7%&hz!i(*a57$y33ff_*6^sat_jdv-w7p4cv&ujws)+2ph"
DEBUG = True

app = Flask( __name__ )
app.config.from_object( __name__ )
db = SqliteDatabase( app.config[ 'DATABASE' ], threadlocals = True )
