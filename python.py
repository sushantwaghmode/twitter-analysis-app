import csv
import string
import tweepy
import re
import pandas as pd
import numpy as np
import configurations
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def AccessTwitter(search_string):
    
    key = configurations.consumer_key
    secret = configurations.consumer_secret
    access_token = configurations.access_token
    access_secret = configurations.access_secret
    
    auth = tweepy.OAuthHandler(consumer_key=key,consumer_secret=secret)
    auth.set_access_token(access_token, access_secret)
    
    api = tweepy.API(auth)
    tweets = []
    
    for tweet in api.search(q=search_string,count=100,lang="en"):
        tweets.append(tweet)
    data = pd.DataFrame(data=[(tweet.text) for tweet in tweets], columns=['Tweets'])
    data['clean_tweets']= data['Tweets'].apply(lambda x:cleanTweet(x))
    data['subjectivity'] = data['clean_tweets'].apply(getsubjectivity)
    data['polarity'] = data['clean_tweets'].apply(getpolarity)
    data['analysis'] = data['polarity'].apply(getanalysis)
    all_words = ' '.join(tweet for tweet in data['clean_tweets'])
    allwords = word_tokenize(all_words)
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in allwords:
        if w not in stop_words:
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    fd = pd.DataFrame(fdist.most_common(10),                    
    columns = ["Word","Frequency"]).drop([0]).reindex()

    # sentiment bar
    sentiment_bar = data['analysis']
    # sentiment pie
    sentiment_pie = data['analysis']
    # word cloud
    word_cloud = WordCloud(width=800,height=400,random_state=1,max_font_size=120).generate(all_words)
    # frequently used words
    n=fd['Word']
    s= fd['Frequency']

    return (sentiment_bar,sentiment_pie,word_cloud,n,s)

def cleanTweet(text):
    text = re.sub(r'@[A-Za-z0-9_:]+','',text)
    text = [char for char in text if char not in string.punctuation]
    text = ''.join(text)
    text = re.sub('#',' ',text)
    text = re.sub('\W+',' ',text)
    text = re.sub('RT[\s]+',' ',text)
    text = re.sub('\n','',text)
    text = re.sub('https?:\/\/\S+',' ',text)
    return text

def getsubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getpolarity(text):
    return TextBlob(text).sentiment.polarity

def getanalysis(score):
    if score<0:
        return 'negative'
    elif score==0:
        return 'neutral'
    else:
        return 'positive'

