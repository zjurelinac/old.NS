from peewee 	import *
from app 		import db
from datetime 	import datetime, date

class MetaModel( Model ):
	database = db


class User( MetaModel ):
	email 				= CharField( unique = True )
	password 			= CharField()
	activation_code 	= IntegerField()
	registration_date 	= DateField( default = date.today() )
	password_reset_code = CharField( default = '' )
	password_reset_date = DateField()


	def __repr__( self ):
		return '<User {0}>'.format( self.email )


class Category( MetaModel ):
	name 		= CharField()
	abbr 		= CharField( max_length = 2 )
	color 		= IntegerField()
	user 		= ForeignKeyField( User, related_name = 'categories' )

	def __repr( self ):
		return '<Category {0}>'.format( self.name )


class Note( MetaModel ):
	title 		= CharField( unique = True )
	content 	= TextField()
	date 		= DateTimeField( default = datetime.now() )
	user 		= ForeignKeyField( User, related_name = 'notes' )
	category 	= ForeignKeyField( Category, related_name = 'notes' )

	def __repr__( self ):
		return '<Note {0}>'.format( self.title )



class Keyword( MetaModel ):
	name 		= CharField()
	user 		= ForeignKeyField( User, related_name = 'keywords' )

class KeywordToNote( MetaModel ):
	note 		= ForeignKeyField( Note )
	keyword 	= ForeignKeyField( Keyword )

	class Meta:
		primary_key = CompositeKey( 'note', 'keyword' )
