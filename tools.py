import zipfile, requests, os, csv
from datetime import datetime
import pandas as pd
import tweepy
import secret
import got3 as got
import random

def get_data():
    url = 'http://bossa.pl/pub/metastock/mstock/mstall.zip'
    print('Getting stock prices...')
    req = requests.get(url)
    print('Getting stock prices successful')
    # check if directory exists, if not create it
    if not (os.path.isdir('file')):
        os.mkdir('file')
    stock_file = open(os.path.join('file', os.path.basename(url)), 'wb')
    for chunk in req.iter_content(100000):
        stock_file.write(chunk)
    stock_file.close()
    zipf = zipfile.ZipFile(os.path.join('file', os.path.basename(url)))
    zipf.extractall((os.path.join(os.path.curdir, 'mst')))

# directories file and mst must exist in current dir

#CURRENT_YEAR = str(date.today().year)
path_mst = (os.path.join(os.path.curdir, 'mst'))

def prepare_data(ticker):

    closes = pd.read_csv(os.path.join(path_mst, ticker+'.mst'))
    closes.rename(index=str, columns={'<TICKER>': 'Ticker', '<DTYYYYMMDD>': 'Date', '<CLOSE>': 'Close', '<VOL>':'Vol'},inplace=True)
    return closes
    # to już koniec! reszta jest obsolete, zwracamy pandas

#the result of this method is saved tweets structure csv with fake sentiment
def get_Twitter_data(ticker, since, date_to):

    auth = tweepy.OAuthHandler(secret.consumer_key, secret.consumer_secret)
    auth.set_access_token(secret.access_token, secret.access_token_secret)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(ticker).setSince(since). \
        setUntil(date_to).setMaxTweets(1000)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    tw_list = []
    tw_list_dates = []
    #print(tweets[0].date)
    for tweet in tweets:
        tw_list.append(tweet.text.encode('utf-8'))
        tw_list_dates.append(tweet.date)
    df = pd.DataFrame({'review': tw_list})  # review is the body of the tweet (the actual text)
    df['date'] = pd.DataFrame({'date': tw_list_dates})
    df['sentiment'] = '5'
    for index, row in df.iterrows():
       df.set_value(index, 'sentiment', random.randint(0, 1))


    df1 = df.reindex(['date','sentiment', 'review'], axis=1)
    #print(df1)
    df1.to_csv('saved_tweets.csv', encoding='utf-8', index_label='id', sep='\t')

#get_data()
#prepare_data('11BIT')

#this method should open the saved tweets csv and using rockets dates fill the sentiments.
#for example set the sentiment of the rocket date tweet and 2 days before to 1 and 0 to the rest
def enrichSavedTweets(saved_tweets, rockets):


    for index, row in rockets.iterrows():
        date1 = datetime.strptime(str(row['Date']), '%Y%m%d')
        #print('date: ', date1)
        for index2, row2 in saved_tweets.iterrows():
            date2 = datetime.strptime(str(row2['date']), '%Y-%m-%d %H:%M:%S')
            date2 = date2.replace(hour=0, minute=0, second=0)
            if date2 == date1:
                print('date OK')
    return saved_tweets


def normalize_feature(data, f_min=-1.0, f_max=1.0):
    d_min, d_max = min(data), max(data)
    factor = (f_max - f_min) / (d_max - d_min)
    normalized = f_min + (data - d_min)*factor
    return normalized, factor