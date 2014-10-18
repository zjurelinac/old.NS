from peewee 	import *
from app 		import db
from datetime 	import datetime

class MetaModel( Model ):
	database = db


class User( MetaModel ):
	email 		= CharField( unique = True )
	password 	= CharField()

	def __repr__( self ):
		return '<User {0}>'.format( self.email )


class Note( MetaModel ):
	title 		= CharField( unique = True )
	content 	= TextField()
	date 		= DateTimeField( default = datetime.now() )
	user 		= ForeignKeyField( User, related_name = 'notes' )
	category 	= ForeignKeyField( Category, related_name = 'notes' )

	def __repr__( self ):
		return '<Note {0}>'.format( self.title )


class Category( MetaModel ):
	name 		= CharField()
	abbr 		= CharField( max_length = 2 )
	color 		= IntegerField()
	user 		= ForeignKeyField( User, related_name = 'categories' )

