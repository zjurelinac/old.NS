from peewee 	import *
from app 		import db
from datetime 	import datetime, date
from utils 		import hashfunc, random_string

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
		""" Throws an exception User.DoesNotExist if there is no user with a given email """
		user = User.get( cls.email == email )

		if( user.password != password ):
			return None
		
		return user

	@classmethod
	def createNew( cls, email, password ):
		""" Throws an exception User.IntegrityError if the same email is already in use """
		with db.transaction():
			User.create( email = email, password = password, activation_code = random_string( 64 ) )

	@classmethod
	def deleteUser( cls, user ):
		pass




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
	def getNoteObject( cls, note_id, user_id ):
		""" Thows a Note.DoesNotExist if user has no note with a given id """
		note = Note.get( Note.id == note_id and Note.user.id == user_id ).join( Category ).join( TagToNote ).join( Tag )

		return {
			"title" 	: 	note.title,
			"content" 	: 	note.content,
			"date" 		: 	note.date.isoformat( 'T' ),
			"category" 	: 	note.category.getCategoryObject(),
			"tags" 		: 	Tag.( note_id )
		}

	@classmethod
	def addNote( cls, title, content, tags, category_id, user ):
		""" Throws a ValueError if user doesn't own a Category with a given id """
		try:
			with db.transaction():
				category = Category.get( Category.id == category_id and Category.user.id == user_id )
				note = Note.create( title = title, content = content, category = category, user = user )
				
				for tag in tags:
					tag = Tag.byName( tag, user )
					TagToNote.create( note = note, tag = tag )

		except Category.DoesNotExist:
			raise ValueError

	@classmethod
	def editNote( cls, id, title, content, tags, category_id, user_id ):
		""" Throws  1) Note.DoesNotExist if user doesn't have a note with a given id
					2) ValueError if user doesn't own a Category with a given id """
		try:
			with db.transaction():
				category = Category.get( Category.id == category_id )
				note = Note.get( Note.user.id == user_id and Note.id == id ).join( Category ).join( TagToNote ).join( Tag )

				note.title = title
				note.content = content
				note.category = category

				for tag in tags:
					pass

		except Category.DoesNotExist:
			raise ValueError
		
	@classmethod
	def deleteNote( cls, id, user_id ):
		""" Thows a Note.DoesNotExist if user has no note with a given id """
		note = Note.get( Note.id == note_id and Note.user.id == user_id )
		note.delete_instance()




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

	@classmethod
	def ofNote( cls, note_id ):




class TagToNote( MetaModel ):
	note 		= ForeignKeyField( Note )
	tag 		= ForeignKeyField( Tag )

	class Meta:
		primary_key = CompositeKey( 'note', 'tag' )
