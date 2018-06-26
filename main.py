import tweepy
import got3 as got
import pandas as pd
import tools
from textblob import TextBlob

consumer_key = r'HiKfocenZQpF6KdYXLA8omuXr'
consumer_secret = r'E37pNLbblVQ6Cm2gX2CEqsK5YVm0Jtlhs96BrNTnu8aXfnpw1p'

access_token = r'253927922-yRXGwbRRoSV5Ant6TL8nTBKxVcApAg9exF4g0YDU'
access_token_secret = r'mMI6uKwRDTWcWzyi8ofU31FZ5srjhgDU7h1q65pUrukAu'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

counter = 0


tweetCriteria = got.manager.TweetCriteria().setQuerySearch('11bitstudios').setSince('2018-05-01'). \
        setUntil('2018-05-27').setMaxTweets(1000)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
tw_list = []
for tweet in tweets:
    tw_list.append(tweet.text.encode('utf-8'))

df = pd.DataFrame({'review': tw_list}) #review is the body of the tweet (the actual text)
df['sentiment'] = ''
df.reindex(['sentiment','review'])
print(df)
df.to_csv('saved_tweets.csv', encoding='utf-8', index_label='id', sep='\t')
