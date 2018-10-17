import tweepy
import got3 as got
import pandas as pd
import tools
from textblob import TextBlob
import scipy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from matplotlib import pyplot as plt
from itertools import product

odp = input('Get Bossa data? [y/n]:')
if odp == 'y':
    tools.get_data()
odp = input('Get Twitter data? [y/n]:')
if odp == 'y':
    tools.get_Twitter_data('11bitstudios', '2018-01-01', '2018-08-01')

#d = pd.read_csv('saved_tweets.csv', delimiter='\t')


def build_model(max_features=None, min_df=1, nb_alpha=1.0):
    vectorizer = TfidfVectorizer(max_features=max_features, min_df=min_df)
    features = vectorizer.fit_transform(d_train.review)
    model = MultinomialNB(alpha=nb_alpha)
    model.fit(features, d_train.sentiment)
    pred = model.predict_proba(vectorizer.transform(d_test.review))
    return {"max_features": max_features, "min_df": min_df, "nb_alpha": nb_alpha, "auc": roc_auc_score(d_test.sentiment,
                                                                                                       pred[:, 1])}


def search_for_optimal_params():
    param_values = {
    "max_features": [10000, 30000, 50000, None],
    "min_df": [1, 2, 3],
    "nb_alpha": [0.01, 0.1, 1.0]
    }
    results = []
    for p in product(*param_values.values()):
        res = build_model(**dict(zip(param_values.keys(), p)))
        results.append(res)
        print(res)


def performance(y_true, pred, color="g", ann=True):
    print(y_true, pred[:, 1])
    acc = accuracy_score(y_true, pred[:, 1] > 0.5)
    auc = roc_auc_score(y_true, pred[:, 1])
    fpr, tpr, thr = roc_curve(y_true, pred[:,1])
    plt.plot(fpr, tpr, color, linewidth="3")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    if ann:
        plt.annotate("Acc: %0.2f" % acc, (0.2, 0.7), size=14)
        plt.annotate("AUC: %0.2f" % auc, (0.2, 0.6), size=14)
    plt.show()
#performance(d_test.sentiment, pred1)
#'max_features': 10000, 'min_df': 1, 'nb_alpha': 0.01, 'auc': 0.8656838656838657}

def normalize_feature(data, f_min=-1.0, f_max=1.0):
    d_min, d_max = min(data), max(data)
    factor = (f_max - f_min) / (d_max - d_min)
    normalized = f_min + (data - d_min)*factor
    return normalized, factor
bossa_data = tools.prepare_data('11BIT')
print('bossa data: ', bossa_data)
res = build_model(10000, 1, 0.01)
print('res: ', res)

def finding_rocket():
    counter = 0 #we need this to skip first value
    for index, row in bossa_data.iterrows():

        counter += 1
        if counter > 2 and (row['Close'] / previous_close > 1.20):
            #print(row['Date'], ' ', row['Close'])
            #print('row: ', row)
            #df1.loc[df2.index[0]] = df2.iloc[0]
            rockets.loc[index] = row
        previous_close = row['Close']
bossa_data = tools.prepare_data('11BIT')
rockets = pd.DataFrame(columns=bossa_data.columns)

finding_rocket()

d = pd.read_csv('saved_tweets.csv', delimiter='\t')

d = tools.enrichSavedTweets(d, rockets)


split = 0.7
d_train = d[:int(split*len(d))]
d_test = d[int((1-split)*len(d)):]
res = build_model(10000, 1, 0.01)
print('ROCKETS', rockets)
