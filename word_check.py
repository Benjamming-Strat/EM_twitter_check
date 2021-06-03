'''
compare tweets to find a relation to cryptocurrencies
'''

import pandas as pd
import pymongo
import re



crypto_dict = {'cry_word':['crypto','coin','doge','to the moon']}

#Pymongo - connection to the database
conn = pymongo.MongoClient()
db = conn.get_database('tweets')
collection = db.get_collection("tweet_data")
cursor = collection.find()


date_list= []
tweet_list= []
#
for ele in cursor:
       # complete DB-entry
       #for word in crypto_dict["cry_word"]:
              #pattern = f'.*{word}.*[\n]*'
              #result = re.findall(pattern, ele["text"])
       result = re.findall('crypto|coin|doge|to the moon', ele["text"])
       if result != []:
              date_list.append(ele["tweet_time"])
              tweet_list.append(ele["text"])
              #print(f'Tweet:{ele["text"]} \n ON: {ele["tweet_time"]}')
                     # for i in result:
                     #        filter = {"text":i}
                     #        #how to get the date of this specific tweet
                     #        cursor_text = collection.find(filter)
                     #        for ct in cursor_text:
                     #               date_list.append(ele["tweet_time"])
                     
      # for item in cursor_text:
print(len(date_list))              