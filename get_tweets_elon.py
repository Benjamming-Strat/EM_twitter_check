import config
from tweepy import OAuthHandler, Cursor, API
from tweepy.streaming import StreamListener
import logging
import re
import pymongo

'''

collect elon musk's tweets, store it in mongoDataBase


'''

def authenticate():
      
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    return auth



def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)




def remove_at_hash_http(text):
    special_pattern = re.compile('@\S+|http\S+|#\S+')
    return special_pattern.sub(r'', text)



if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)

    cursor = Cursor(api.user_timeline, id = 'elonmusk', tweet_mode = 'extended',count=500)
    
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
            
            filter = {"text":tweet["text"],
                      "tweet_time":tweet["tweet_time"]}
            cursor = collection.find(filter)
            if cursor.count()==0:
                collection.insert_one(tweet)
                print("inserted")
        else:
            db = conn.tweets        #building a database db named tweets
            collection = db.tweet_data #building table to store tweets
            filter = {"text":tweet["text"],
                      "tweet_time":tweet["tweet_time"]}
            cursor = collection.find(filter)
            if cursor.count()==0:
                collection.insert_one(tweet)
                print("inserted")