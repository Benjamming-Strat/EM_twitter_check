"""
Controller file for the web application.

The central file of the application. 
"""

from flask import Flask
from flask import render_template
from flask import request
import sys
sys.path.insert(0, r'C:\Users\LSchw\Documents\benjamin\spiced_projects\final_project\EM_twitter_check') 
import get_tweets_elon
from get_tweets_elon import authenticate, remove_at_hash_http, remove_emoji
import config
from tweepy import OAuthHandler, Cursor, API
from tweepy.streaming import StreamListener
import logging
import re
import pymongo

  
  
app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html", title="Rate that Tweet!")


@app.route("/helloworld")
def hi():
    tAccount = request.args.get('twitter-account')
    crypto = request.args.get('crypto')


    html_form_data = dict(request.args)


    auth = authenticate()
    api = API(auth)

    cursor = Cursor(api.user_timeline, id = tAccount, tweet_mode = 'extended',count=500)
    
    tweet_list = []
    id = 0
    
    for status in cursor.items(500):
        id += 1
        print(id)
        
        
        text = status.full_text
        likes = status.favorite_count
        time_created = status.created_at
        
    

        # take extended tweets into account
        # TODO: CHECK
        
        if 'extended_tweet' in dir(status):
            text =  status.extended_tweet.full_text
            #if 'retweeted_status' in dir(status):
            #   r = status.retweeted_status
            #  if 'extended_tweet' in dir(r):
            #     text =  r.extended_tweet.full_text

        tweet = {
            'id' : id,
            'text': text,
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count,
            'tweet_time':status.created_at
        }
        
        tweet["text"]=remove_at_hash_http(tweet["text"])
        tweet["text"]=remove_emoji(tweet["text"])
        tweet_list.append(tweet)
        
        
        
        conn = pymongo.MongoClient()
        
        
        # if tweet is in DB do not insert
        dbnames = conn.list_database_names()
        if 'tweets' in dbnames:
            db = conn.get_database('tweets')
            collection = db.get_collection("tweet_data")
            
            filter = {"text":tweet["text"]} #"tweet_time":tweet["tweet_time"]
            cursor = collection.find(filter)
            
            
            if cursor.count()==0:
                collection.insert_one(tweet)
                print("inserted to exiting DB ")
            
        else:
            db = conn.tweets        #building a database db named tweets
            collection = db.tweet_data #building table to store tweets
            filter = {"text":tweet["text"],
                    "tweet_time":tweet["tweet_time"]}
            cursor = collection.find(filter)
            if cursor.count()==0:
                collection.insert_one(tweet)
                print("inserted to new DB")



    return render_template("test.html", html_account=tAccount, html_crypto=crypto)

    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
    
    
