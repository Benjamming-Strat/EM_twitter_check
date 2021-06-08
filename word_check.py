'''

compare tweets to find a relation to cryptocurrencies


'''

import pandas as pd
import pymongo
import re
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Tweets:
       
       def create_tweets(self):
              crypto_dict = {'cry_word':['crypto','coin','doge','to the moon']}

              #Pymongo - connection to the database

              conn = pymongo.MongoClient()
              db = conn.get_database('tweets')
              collection = db.get_collection("tweet_data")
              cursor = collection.find()


              date_list= []
              tweet_list= []
              id=1
              for ele in cursor:

                     result = re.findall('Doge|Crypto|crypto|coin|doge|to the moon', ele["text"])

                     if result != []:
                            
                            date_list.append(ele["tweet_time"])
                            tweet_list.append(ele["text"])
                            
              data = list(zip(tweet_list, date_list))
              df_tweets = pd.DataFrame(data, columns=["tweet","date"]) 
              df_tweets["date"] = df_tweets["date"].dt.strftime("%d-%m-%Y")
              df_tweets['date'] = pd.to_datetime(df_tweets['date'], format='%d-%m-%Y')
              df_tweets["date_after_tweet"] = df_tweets["date"] + timedelta(days=1)
              print(df_tweets)
              return df_tweets

       
       def sentiment(self, df):
              self.df = df
              score_list = []
              #sentiment analysis
              s  = SentimentIntensityAnalyzer()
              for index,senti in self.df.iterrows():
                     text = senti["tweet"]
                     sentiment = s.polarity_scores(text)
                     score = sentiment['compound']
                     score_list.append(score)
              self.df["score"] = score_list
              
              return self.df
              
                     
b = Tweets()
df_tweets = b.create_tweets()
df_sentiment = b.sentiment(df_tweets)