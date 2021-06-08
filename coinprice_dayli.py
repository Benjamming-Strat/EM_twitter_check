'''
Using coingecko's API to get the historical daily prices of desired coins
and building a dataframe with that data
columns = Tweet, date,date+1,difference, ratio

	
successful operation - Result in the Format:

[
1594382400000 (time),
1.1 (open),
2.2 (high),
3.3 (low),
4.4 (close)
]

'''




import requests
import json
from datetime import datetime
from word_check import Tweets
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt



class Coin:      
    
    def create_ohlc(self):
        date_list = []
        coin_name = "bitcoin"
        
        request = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_name}/ohlc?vs_currency=usd&days=180")
        data_text = request.text
        data = json.loads(data_text)
        
        for i in range(len(data)):
            #timestamp is unix timestamp
          timestamp = data[i][0]/1000


          date = datetime.fromtimestamp(timestamp)
          date_list.append(date)
        return date_list
    
    def coin_filter(self, coin, df):
        self.coin = str.lower(coin)
        self.df = df
        #crytpo may stand for bitcoin in total
        #now its only filtered by the coin but it should also contain Doge, Crypto and stuff
        
       
        self.df.tweet = self.df.tweet.str.lower() #will match all cases of ht word
        
        #ways to improve = fuzzy matching, word embeddings of teh tweet not the tweet, angle (cosine ) of tweets       
        filter = self.df["tweet"].str.contains(self.coin)
        df_filter = self.df[filter]
        return df_filter
        
    def create_history(self, coin, df):
        #d_date_format: dd-mm-yyyy
        
        self.coin_name = str.lower(coin)
        self.df = df
        usd_today = []
        usd_tomor = []
        self.df["date"] = self.df["date"].dt.strftime("%d-%m-%Y")
        self.df["date_after_tweet"] = self.df["date_after_tweet"].dt.strftime("%d-%m-%Y")
        
        
        d_date = self.df["date"]
        
        for d in list(d_date):
            
           
            request = requests.get(f"https://api.coingecko.com/api/v3/coins/{self.coin_name}/history?date={d}&localization=false")
            data_text = request.text
            data = json.loads(data_text)
            
            usd_price = round(data["market_data"]["current_price"]["usd"],2)
            #print(f"date: {d} and price: {usd_price}")
            usd_today.append(usd_price)
        
        d_date_1 = self.df["date_after_tweet"]
        
        for d_1 in list(d_date_1):
            request_1 = requests.get(f"https://api.coingecko.com/api/v3/coins/{self.coin_name}/history?date={d_1}&localization=false")
            data_text_1 = request_1.text
            data_1 = json.loads(data_text_1)
            usd_price_1 = round(data_1["market_data"]["current_price"]["usd"],2)
            
            #print(f"date: {d} and price: {usd_price}")
            usd_tomor.append(usd_price_1)
        
        # print(usd_today)
        # print(usd_tomor)
        diff_list = []
        for i in range(len(usd_today)):
            diff_price = (usd_tomor[i] - usd_today[i])/usd_today[i]
            diff_list.append(diff_price)
            # print(diff_price)
        
        self.df["ratio"] = diff_list
        return self.df
        
        
    # def concat_df(self,df_1, df_2):
    #     df_total = pd.Concatenate(df_1, df_2)
        
    #     return df_total
            
 
#instanciation        
bitcoin = Coin()
dogecoin = Coin()
tweets = Tweets()

#creating tweets from module word_check
df_tweet = tweets.create_tweets()

#filter the coin
df_tweet_bitcoin = bitcoin.coin_filter("Bit",df_tweet)
df_tweet_dogecoin = dogecoin.coin_filter("Doge",df_tweet)
#create historic price-data and difference between prices
#bitcoin
df_bitcoin = bitcoin.create_history("Bitcoin",df_tweet_bitcoin)
df_bitcoin_sentiment = tweets.sentiment(df_bitcoin)

#dogecoin
df_dogecoin = dogecoin.create_history("Dogecoin",df_tweet_dogecoin)
df_dogecoin_sentiment = tweets.sentiment(df_dogecoin)

#total
df_total_sentiment = tweets.sentiment(df_tweet)

df_total = pd.concat([df_dogecoin_sentiment, df_bitcoin_sentiment])
print("____________________________The Super awesome Dataframe of Elons TWEETS________________________")
print(df_total)
print("________________________________________________________________")

sns.scatterplot(data=df_total, x="ratio", y="score")
plt.show()



















# #sentiment analysis
# s  = SentimentIntensityAnalyzer()
# for index,senti in df_coinratio.iterrows():
#     text = senti["tweet"]
#     sentiment = s.polarity_scores(text)
#     score = sentiment['compound']
#     print(f"Sentiment-Analysis: \n_________\nThe Tweet: {text}: \nhas a compound score of {score} \n ---End of Tweet---")
#     print()

