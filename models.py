from peewee 	import *
from app 		import db
from datetime 	import datetime, date
from utils 		import hashfunc

class MetaModel( Model ):
	database = db


class User( MetaModel ):
	email 				= CharField( unique = True )
	password 			= CharField()
	activation_code 	= CharField()
	registration_date 	= DateField( default = date.today() )
	password_reset_code = CharField( null = True )
	password_reset_date = DateField( null = True )


	def __repr__( self ):
		return '<User {0}>'.format( self.email )

	@classmethod
	def validate( cls, email, password ):
		""" Throws an exception User.DoesNotExist if no user with given email """
		user = User.get( cls.email == email )

		if( user.password != hashfunc( password ) ):
			return None
		
		return user

	@classmethod
	def createNew( cls, email, password ):
		""" Throws an exception User.IntegrityError if the same email is already in use """
		user = User.create( email = email, password = hashfunc( password ), activation_code = random_string( 64 ) )




class Category( MetaModel ):
	name 		= CharField()
	abbr 		= CharField( max_length = 2 )
	color 		= IntegerField()
	user 		= ForeignKeyField( User, related_name = 'categories' )

	def __repr__( self ):
		return '<Category {0}>'.format( self.name )


class Note( MetaModel ):
	title 		= CharField( unique = True )
	content 	= TextField()
	date 		= DateTimeField( default = datetime.now() )
	user 		= ForeignKeyField( User, related_name = 'notes' )
	category 	= ForeignKeyField( Category, related_name = 'notes' )

	def __repr__( self ):
		return '<Note {0}>'.format( self.title )

	@classmethod
	def addNew( cls, title, content, tags, category_id, user ):
		try:
			with db.transaction():
				category = Category.get( Category.id == category_id )
				note = Note.create( title = title, content = content, category = category, user = user )
				
				for tag in tags:
					tag = Tag.byName( tag, user )
					TagToNote.create( note = note, tag = tag )

		except Category.DoesNotExist:
			raise ValueError

	@classmethod
	def editNote( cls, id, title, content, tags, category, user ):
		note = Note.select().where( Note.user == user && Note.id == id )
		
		note.title = title
		note.content = content
		note.category = category





class Tag( MetaModel ):
	name 		= CharField()
	user 		= ForeignKeyField( User, related_name = 'tags' )

	def __repr__( self ):
		return '<Tag {0}>'.format( self.name )

	@classmethod
	def byName( cls, name, user ):
		try:
			tag = Tag.get( Tag.name == name and Tag.user == user )
		except Tag.DoesNotExist:
			tag = Tag.create(  )




class TagToNote( MetaModel ):
	note 		= ForeignKeyField( Note )
	tag 		= ForeignKeyField( Tag )

	class Meta:
		primary_key = CompositeKey( 'note', 'tag' )
