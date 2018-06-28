import zipfile, requests, os, csv
import numpy as np
import pandas as pd
import tweepy
import got3 as got

def get_data():
    url = 'http://bossa.pl/pub/metastock/mstock/mstall.zip'
    print('getting stock prices...')
    req = requests.get(url)
    print('getting stock prices succeded')
    stock_file = open(os.path.join('file', os.path.basename(url)), 'wb')
    for chunk in req.iter_content(100000):
        stock_file.write(chunk)
    stock_file.close()
    zipf = zipfile.ZipFile(os.path.join('file', os.path.basename(url)))
    zipf.extractall((os.path.join( os.path.curdir, 'mst')))

# directories file and mst must exist in current dir

#CURRENT_YEAR = str(date.today().year)
path_mst = (os.path.join(os.path.curdir, 'mst'))

def prepare_data(ticker):

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
    print(closes)

    #prev_close = n_array[around_item_indx[0][0] + i, :][4]
    #next_open = n_array[around_item_indx[0][0] + i + 1, :][1]


    return closes
            #print(a)


def get_Twitter_data():

    consumer_key = r'HiKfocenZQpF6KdYXLA8omuXr'
    consumer_secret = r'E37pNLbblVQ6Cm2gX2CEqsK5YVm0Jtlhs96BrNTnu8aXfnpw1p'

    access_token = r'253927922-yRXGwbRRoSV5Ant6TL8nTBKxVcApAg9exF4g0YDU'
    access_token_secret = r'mMI6uKwRDTWcWzyi8ofU31FZ5srjhgDU7h1q65pUrukAu'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #api = tweepy.API(auth)

    #counter = 0

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('11bitstudios').setSince('2018-06-01'). \
        setUntil('2018-06-27').setMaxTweets(1000)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    tw_list = []
    for tweet in tweets:
        tw_list.append(tweet.text.encode('utf-8'))

    df = pd.DataFrame({'review': tw_list})  # review is the body of the tweet (the actual text)
    df['sentiment'] = ''
    df1 = df.reindex(['sentiment', 'review'], axis=1)
    print(df1)
    df1.to_csv('saved_tweets.csv', encoding='utf-8', index_label='id', sep='\t')

#get_data()
#prepare_data('11BIT')