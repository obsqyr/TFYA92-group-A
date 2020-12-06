# This is for testing to make a mongodb database

#import pymongo
import mongomock
#client = pymongo.MongoClient() # default host and port
# Examples to specify host and port
#client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://localhost:27017/')
#connect('mongoenginetest', host='mongomock://localhost')
client = mongomock.MongoClient()

db = client.test_database
collection = db.test_collection
post = {"author": "Linda",
        "text": "This is a test to create a mongodb database.",
        "tags": ["mongodb", "python"],
        "date": "6 december"}
post_id = db.posts.insert_one(post)
print("This is the post_id: ", post_id)
