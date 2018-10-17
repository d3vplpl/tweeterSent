import zipfile, requests, os, csv
import numpy as np
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
    f = open(os.path.join(path_mst, ticker+'.mst'))
    cs = csv.reader(f)
    cs_list = list(cs)

    header = cs_list.pop(0) #removes header
    float_list = []
    ticker = ''
    for el in cs_list:
        ticker = el.pop(0) #removes ticker
        float_list.append([i for i in el])
    n_array = np.array(float_list)
    closes = n_array[:,4]
    #print(closes)

    #prev_close = n_array[around_item_indx[0][0] + i, :][4]
    #next_open = n_array[around_item_indx[0][0] + i + 1, :][1]


    return closes

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

    return saved_tweets