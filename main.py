from app 	import app, db
from api 	import *
from views 	import *
from models import *

if __name__ == '__main__':
	db.create_tables( [ User, Note, Category, Keyword, KeywordToNote ], safe = True )
	app.run()
