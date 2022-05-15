import zipfile, requests, os, csv
from datetime import datetime
from datetime import timedelta
import pandas as pd
import tweepy as tw
import secret
import got3 as got
#import GetOldTweets3 as got
import random
no_of_tweets_limit = 10
#20144 tweetów pobierało się 35 minut

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
    closes.rename(index=str, columns={'<TICKER>': 'Ticker', '<DTYYYYMMDD>': 'Date', '<CLOSE>': 'Close', '<VOL>': 'Vol'},inplace=True)
    return closes


#the result of this method is saved tweets structure csv with fake sentiment
def get_Twitter_data(ticker, since, date_to):

    auth = tw.OAuthHandler(secret.consumer_key, secret.consumer_secret)
    auth.set_access_token(secret.access_token, secret.access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    #print('twitter auth: ', auth)
    tweet_criteria = got.manager.TweetCriteria().setQuerySearch(ticker).setSince(since). \
        setUntil(date_to).setMaxTweets(no_of_tweets_limit)  # to jest ilosc limitu tweetow

    print('criteria: ', tweet_criteria)
    #public_tweets = api.home_timeline()
    #for tweet in public_tweets:
    #    print(tweet.text)
    search_words = ticker
    tweets = tw.Cursor(api.search_tweets,
                       q=search_words,

                       ).items(5000)
    #tweets = got.manager.TweetManager.getTweets(tweet_criteria)
    tw_list = []
    tw_list_dates = []
    for tweet in tweets:
        tw_list.append(tweet.text.encode('utf-8'))
        tw_list_dates.append(tweet.created_at)
    df = pd.DataFrame({'review': tw_list})  # review is the body of the tweet (the actual text)
    df['date'] = pd.DataFrame({'date': tw_list_dates})
    df['sentiment'] = '0'
    df1 = df.reindex(['date', 'sentiment', 'review'], axis=1)
    df1.to_csv('saved_tweets.csv', encoding='utf-8', index_label=False, sep='\t', date_format='%Y%m%d')

#CHYBA to trzeba od nowa zrobić!
#this method should open the saved tweets csv and using rockets dates fill the sentiments.
#for example set the sentiment of the rocket date tweet and 2 days before to 2 and leave rest at default 0
def enrichSavedTweets(saved_tweets, rockets):
    saved_tweets['sentiment'] = '0'
    for index, row in saved_tweets.iterrows():
        date_tweet = row['date']
        date_tweet = date_tweet.replace(hour=0, minute=0, second=0)
        for index2, row2 in rockets.iterrows():
            date_rocket = datetime.strptime(str(row2['Date']),  '%Y%m%d')
            date_rocket = date_rocket.replace(hour=0, minute=0, second=0)

            print ('Comparing ', (date_tweet-timedelta(days=2)), ' and ', date_rocket)
            if date_tweet + timedelta(days=1) == date_rocket:
                print("date of tweet: ", date_tweet, "matches date of rocket: ", date_rocket,
                      "so this is a tweet that indicates rocket's date")
                saved_tweets.at[index, 'sentiment'] = '1'

    saved_tweets.to_csv('saved_tweets.csv', encoding='utf-8', index_label=False,  sep='\t')
    print('Enrichment complete')
    return saved_tweets

#this method should set sentiment for the date provided
def set_sentiment_for_given_date(saved_tweets, given_date):
    saved_tweets['sentiment'] = '0'
    for index, row in saved_tweets.iterrows():
        date_tweet = row['date']
        if given_date == date_tweet:
            print("Given date equals tweet date")
            saved_tweets.at[index, 'sentiment'] = '1'
    saved_tweets.to_csv('saved_tweets.csv', encoding='utf-8', index_label=False, sep='\t')
    print('setting complete')


# this method should shift marked sentiments by amount of days so they would indicate the signal earlier
def phase_shifter(saved_tweets, amount_of_days_to_shift):

    for index, row in saved_tweets.iteerrow():
        #saved_twwets['date']
        pass

def normalize_feature(data, f_min=-1.0, f_max=1.0):
    d_min, d_max = min(data), max(data)
    factor = (f_max - f_min) / (d_max - d_min)
    normalized = f_min + (data - d_min)*factor
    return normalized, factor

def lookup(date_pd_series, format=None):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date, format=format) for date in date_pd_series.unique()}
    return date_pd_series.map(dates)