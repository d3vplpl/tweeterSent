import tweepy
import got3 as got
from textblob import TextBlob

consumer_key = r'HiKfocenZQpF6KdYXLA8omuXr'
consumer_secret = r'E37pNLbblVQ6Cm2gX2CEqsK5YVm0Jtlhs96BrNTnu8aXfnpw1p'

access_token = r'253927922-yRXGwbRRoSV5Ant6TL8nTBKxVcApAg9exF4g0YDU'
access_token_secret = r'mMI6uKwRDTWcWzyi8ofU31FZ5srjhgDU7h1q65pUrukAu'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.search('Morawiecki', count = 1000)
counter = 0

# query = 'python'
# max_tweets = 1000
# searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
#for tweet in tweepy.Cursor(api.search, q="11bitstudios", count=100, since_id='1',
#                           max_id='997690519814836224',
#                           lang="pl").items(100):
#    counter += 1
#    print(counter)
#    print(tweet.created_at, tweet.id, tweet.text)
    # print(tweet.id)


def getOlderTweets():
    def printTweet(descr, t):
        print(descr)
        print("Username: %s" % t.username)
        print("Retweets: %d" % t.retweets)
        print("Text: %s" % t.text)
        print("Mentions: %s" % t.mentions)
        print("Hashtags: %s\n" % t.hashtags)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('11bitstudios').setSince("2016-05-01"). \
        setUntil("2018-05-27").setMaxTweets(1000)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in tweets:
        print(tweet.text)
    #printTweet("Tweet", tweet)


getOlderTweets()
