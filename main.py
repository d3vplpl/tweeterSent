import tweepy
import got3 as got
import pandas as pd
import tools
from textblob import TextBlob
import scipy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve



odp = input('Get Twitter data? [y/n]:')
if odp == 'y':
    tools.get_Twitter_data()
odp = input('Load the twitter data from disk? [y/n]:')
if odp == 'y':
    d = pd.read_csv('saved_tweets.csv', delimiter='\t')


split = 0.7
d_train = d[:int(split*len(d))]
d_test = d[int((1-split)*len(d)):]

#print (d_test['review'])

vectorizer = CountVectorizer()

features = vectorizer.fit_transform(d_train.review)
test_features = vectorizer.transform(d_test.review)
i = 45000
j = 10
words = vectorizer.get_feature_names()[i:i+10]
pd.DataFrame(features[j:j+7,i:i+10].todense(), columns=words)

model1 = MultinomialNB()
model1.fit(features, d_train.sentiment)
pred1 = model1.predict_proba(test_features)

def performance(y_true, pred, color="g", ann=True):
    acc = accuracy_score(y_true, pred[:,1] > 0.5)
    auc = roc_auc_score(y_true, pred[:,1])
    fpr, tpr, thr = roc_curve(y_true, pred[:,1])
    plot(fpr, tpr, color, linewidth="3")
    xlabel("False positive rate")
    ylabel("True positive rate")
    if ann:
        annotate("Acc: %0.2f" % acc, (0.2,0.7), size=14)
        annotate("AUC: %0.2f" % auc, (0.2,0.6), size=14)
performance(d_test.sentiment, pred1)