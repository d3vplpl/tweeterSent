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

odp = input('Get Twitter data? [y/n]:')
if odp == 'y':
    tools.get_Twitter_data()
odp = input('Load the twitter data from disk? [y/n]:')
if odp == 'y':
    d = pd.read_csv('saved_tweets.csv', delimiter='\t')
    #d = pd.read_csv("movie_reviews/labeledTrainData.tsv", delimiter="\t")


split = 0.7
d_train = d[:int(split*len(d))]
d_test = d[int((1-split)*len(d)):]
def build_model(max_features=None, min_df=1, nb_alpha=1.0):
    vectorizer = TfidfVectorizer(max_features=max_features, min_df=min_df)
    features = vectorizer.fit_transform(d_train.review)
    model = MultinomialNB(alpha=nb_alpha)
    model.fit(features, d_train.sentiment) #model powstaje z train
    pred = model.predict_proba(vectorizer.transform(d_test.review)) #a predykcja z test
    return {
    "max_features": max_features,
    "min_df": min_df,
    "nb_alpha": nb_alpha,
    "auc": roc_auc_score(d_test.sentiment, pred[:,1])
    }

#print (d_test['review'])


param_values = {
"max_features": [10000, 30000, 50000, None],
"min_df": [1, 2, 3],
"nb_alpha": [0.01, 0.1, 1.0]
}
results = []
for p in product(*param_values.values()):
    res = build_model(**dict(zip(param_values.keys(), p)))
    results.append( res )
    print (res)

#features = vectorizer.fit_transform(d_train.review)
#test_features = vectorizer.transform(d_test.review)
i = 45000
j = 10
#words = vectorizer.get_feature_names()[i:i+10]
#pd.DataFrame(features[j:j+7, i:i+10].todense(), columns=words)

def performance(y_true, pred, color="g", ann=True):
    print(y_true, pred[:, 1])
    acc = accuracy_score(y_true, pred[:, 1] > 0.5)
    auc = roc_auc_score(y_true, pred[:, 1])
    fpr, tpr, thr = roc_curve(y_true, pred[:, 1])
    plt.plot(fpr, tpr, color, linewidth="3")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    if ann:
        plt.annotate("Acc: %0.2f" % acc, (0.2, 0.7), size=14)
        plt.annotate("AUC: %0.2f" % auc, (0.2, 0.6), size=14)
    plt.show()
performance(d_test.sentiment, pred1)