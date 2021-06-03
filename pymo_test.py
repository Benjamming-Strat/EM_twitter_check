import pymongo

# post = {"id":1}
# post2 = {"id":1}
# collection.insert_one(post)

# collection.insert_many([post,post2])

conn = pymongo.MongoClient()
db = conn.get_database('tweets')
collection = db.get_collection("tweet_data")
cursor = collection.find({"text":"Hallo"})

if cursor.count()==0:
    print("There is no tweet like this")
else:
    print("uh lala u got some real shit done hon")
