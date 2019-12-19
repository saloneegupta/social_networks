import twitter
import pprint
import json
from pprint import pprint
import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from googleapiclient.discovery import build
from collections import Counter
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import easygui
import pprint
import sys
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from texttable import Texttable

WORLD_WOE_ID = 1
def twitter_setup():
    consumer_key = '2D2qQNR2rSUwzulwEGFPXR3zp'
    consumer_secret = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
    access_token = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
    access_token_secret = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

class TwitterClient(object):
    def __init__(self):
        consumer_key = '2D2qQNR2rSUwzulwEGFPXR3zp'
        consumer_secret = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
        access_token = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
        access_token_secret = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

def view_trends():
    CONSUMER_KEY = '2D2qQNR2rSUwzulwEGFPXR3zp'
    CONSUMER_SECRET = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
    OAUTH_TOKEN = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
    OAUTH_TOKEN_SECRET = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    print("-" * 50)
    print('World Trends : ')
    print("-" * 50)
    for i in world_trends[0][u'trends']:
        print(i[u'name'])
    sys.stdin.read(1)

def change_trends():
    global WORLD_WOE_ID
    data_enterbox_ID=easygui.enterbox('Enter the WOEID to change location: ','WOEID LOCATION WISE')
    WORLD_WOE_ID = int(data_enterbox_ID)
    CONSUMER_KEY = '2D2qQNR2rSUwzulwEGFPXR3zp'
    CONSUMER_SECRET = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
    OAUTH_TOKEN = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
    OAUTH_TOKEN_SECRET = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    
    print('\n Altered Trends : \n')
    for i in world_trends[0][u'trends']:
        print(i[u'name'])
    sys.stdin.read(1)
    
def combined_graph():
    CONSUMER_KEY = '2D2qQNR2rSUwzulwEGFPXR3zp'
    CONSUMER_SECRET = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
    OAUTH_TOKEN = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
    OAUTH_TOKEN_SECRET = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    q = input('Enter a Name to Search: ')
    print('Extracting Data');
    search_results = twitter_api.search.tweets(q=q, count=70)
    statuses = search_results['statuses']
    hashtags = [hashtag['text']
                for status in statuses
                for hashtag in status['entities']['hashtags']]
    retweets1 = twitter_api.statuses.retweets(id=317127304981667841)
    status_texts = [status['text']
                    for status in statuses]
    words = [w
             for t in status_texts
             for w in t.split()]
    print('Processing Data');
    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:  
            break
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
    screen_names = [user_mention['screen_name']
                    for status in statuses
                    for user_mention in status['entities']['user_mentions']]
    screen_names=set(screen_names)
    screen_names=list(screen_names)
    G=nx.Graph()
    for r in min(screen_names,screen_names[0:8]):
        G.add_edge(str(q), str(r));
    plt.subplot(2,2,1);
    plt.title('Users')
    nx.draw(G, with_labels = True)
    #plt.savefig('social/'+q+'1.png')
    #plt.show(block=True)
    #plt.close('all')
    G2=nx.Graph()
    for r in min(words,words[0:8]):
        G2.add_edge(str(q),r);
    plt.subplot(2,2,2);
    plt.title('Words')
    nx.draw(G2, with_labels = True)
    #plt.savefig('social/'+q+'2.png')
    #plt.show(block=True)
    #plt.close('all')
    G3=nx.Graph()
    for r in min(retweets1,retweets1[0:8]):
        G3.add_edge(str(q), str(r['user']['screen_name']));
    plt.subplot(2,2,3);
    plt.title('Retweeters')
    nx.draw(G3, with_labels = True)
    #plt.savefig('social/'+q+'3.png')
    #plt.show(block=True)
    #plt.close('all')
    G4=nx.Graph()
    for r in min(hashtags,hashtags[0:8]):
        G4.add_edge(str(q), r);
    plt.subplot(2,2,4);
    plt.title('Hashtags')
    nx.draw(G4, with_labels = True)
    plt.savefig('social/'+q+'4.png')
    plt.show(block=True)
    plt.close('all')

def network_models():
    CONSUMER_KEY = '2D2qQNR2rSUwzulwEGFPXR3zp'
    CONSUMER_SECRET = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
    OAUTH_TOKEN = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
    OAUTH_TOKEN_SECRET = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    q = input('Enter a Name to Search: ')
    print('Extracting Data');
    search_results = twitter_api.search.tweets(q=q, count=30)
    statuses = search_results['statuses']
    retweets1 = twitter_api.statuses.retweets(id=317127304981667841)
    print('Processing Data');
    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:  
            break
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
    screen_names = [user_mention['screen_name']
                    for status in statuses
                    for user_mention in status['entities']['user_mentions']]
    screen_names=set(screen_names)
    screen_names=list(screen_names)
    ans=1;
    while(ans==1):
        os.system('clear')
        ch=int(input('1) Small World Network for Users\n2) Random Network for Users\n3) Small World Network for Retweeters\n4) Random Network for Retweeters\nEnter choice: '));
        if(ch==1):
            plt.subplot(1,2,1)
            G=nx.watts_strogatz_graph(8, 2, 0.7);
            plt.title('Small World Network for Users');
            nx.draw(G, with_labels = True);
            print('\nSmall World Network for Users')
            print('\nDegree Centrality')
            t1=nx.degree_centrality(G)
            print(nx.degree_centrality(G));
            print('\nMost Important node based on Degree Centrality: ')
            v1=[]
            for i in t1.keys():
                if(t1[i]==max(t1.values())):
                    v1.append(i);
                    print('Node '+str(i));
            print('\nCloseness Centrality')
            t2=nx.closeness_centrality(G)
            print(nx.closeness_centrality(G));
            print('\nMost Important node based on Closeness Centrality: ')
            v2=[]
            for i in t2.keys():
                if(t2[i]==max(t2.values())):
                    v2.append(i);
                    print('Node '+str(i));
            print('\nBetweeness Centrality')
            t3=nx.betweenness_centrality(G)
            print(nx.betweenness_centrality(G));
            print('\nMost Important node based on Betweeness Centrality: ')
            v3=[]
            for i in t3.keys():
                if(t3[i]==max(t3.values())):
                    v3.append(i);
                    print('Node '+str(i));
            print('\n\nMost Important Node in the network: ')
            for i in v1:
                if(i in v2 and i in v3):
                    print('Node '+str(i)+' - '+screen_names[i]);
            plt.subplot(1,2,2)
            G=nx.Graph();
            nx.draw(G);
            for i in range(8):
                plt.text(0.5, 0.2+(i*0.08), str(i)+'-'+screen_names[i], horizontalalignment='center', verticalalignment='center', fontsize=9)
            plt.savefig('social1/'+q+'1.png')
            plt.show();
            plt.close('all');
        elif(ch==2):
            plt.subplot(1,2,1)
            G=nx.gnp_random_graph(8,0.2);
            plt.title('Random Network for Users');
            nx.draw(G, with_labels = True);
            print('\nRandom Network for Users')
            print('\nDegree Centrality')
            t1=nx.degree_centrality(G)
            print(nx.degree_centrality(G));
            print('\nMost Important node based on Degree Centrality: ')
            v1=[]
            for i in t1.keys():
                if(t1[i]==max(t1.values())):
                    v1.append(i);
                    print('Node '+str(i));
            print('\nCloseness Centrality')
            t2=nx.closeness_centrality(G)
            print(nx.closeness_centrality(G));
            print('\nMost Important node based on Closeness Centrality: ')
            v2=[]
            for i in t2.keys():
                if(t2[i]==max(t2.values())):
                    v2.append(i);
                    print('Node '+str(i));
            print('\nBetweeness Centrality')
            t3=nx.betweenness_centrality(G)
            print(nx.betweenness_centrality(G));
            print('\nMost Important node based on Betweeness Centrality: ')
            v3=[]
            for i in t3.keys():
                if(t3[i]==max(t3.values())):
                    v3.append(i);
                    print('Node '+str(i));
            print('\n\nMost Important Node in the network: ')
            for i in v1:
                if(i in v2 and i in v3):
                    print('Node '+str(i)+' - '+screen_names[i]);
            plt.subplot(1,2,2)
            G=nx.Graph();
            nx.draw(G);
            for i in range(8):
                plt.text(0.5, 0.2+(i*0.08), str(i)+'-'+screen_names[i], horizontalalignment='center', verticalalignment='center', fontsize=9)
            plt.savefig('social1/'+q+'2.png')
            plt.show();
            plt.close('all');
        elif(ch==3):
            plt.subplot(1,2,1)
            G=nx.watts_strogatz_graph(8, 2, 0.8);
            plt.title('Small World Network for Retweeters');
            nx.draw(G, with_labels = True);
            print('\nSmall World Network for Retweeters')
            print('\nDegree Centrality')
            t1=nx.degree_centrality(G)
            print(nx.degree_centrality(G));
            print('\nMost Important node based on Degree Centrality: ')
            v1=[]
            for i in t1.keys():
                if(t1[i]==max(t1.values())):
                    v1.append(i);
                    print('Node '+str(i));
            print('\nCloseness Centrality')
            t2=nx.closeness_centrality(G)
            print(nx.closeness_centrality(G));
            print('\nMost Important node based on Closeness Centrality: ')
            v2=[]
            for i in t2.keys():
                if(t2[i]==max(t2.values())):
                    v2.append(i);
                    print('Node '+str(i));
            print('\nBetweeness Centrality')
            t3=nx.betweenness_centrality(G)
            print(nx.betweenness_centrality(G));
            print('\nMost Important node based on Betweeness Centrality: ')
            v3=[]
            for i in t3.keys():
                if(t3[i]==max(t3.values())):
                    v3.append(i);
                    print('Node '+str(i));
            print('\n\nMost Important Node in the network: ')
            for i in v1:
                if(i in v2 and i in v3):
                    print('Node '+str(i)+' - '+screen_names[i]);
            plt.subplot(1,2,2)
            G=nx.Graph();
            nx.draw(G);
            for i in range(8):
                plt.text(0.5, 0.2+(i*0.08), str(i)+'-'+screen_names[i], horizontalalignment='center', verticalalignment='center', fontsize=9)
            plt.savefig('social1/'+q+'3.png')
            plt.show();
            plt.close('all');
        else:
            plt.subplot(1,2,1)
            G=nx.gnp_random_graph(8,0.2);
            plt.title('Random Network for Retweeters');
            nx.draw(G, with_labels = True);
            print('\nRandom Network for Retweeters')
            print('\nDegree Centrality')
            t1=nx.degree_centrality(G)
            print(nx.degree_centrality(G));
            print('\nMost Important node based on Degree Centrality: ')
            v1=[]
            for i in t1.keys():
                if(t1[i]==max(t1.values())):
                    v1.append(i);
                    print('Node '+str(i));
            print('\nCloseness Centrality')
            t2=nx.closeness_centrality(G)
            print(nx.closeness_centrality(G));
            print('\nMost Important node based on Closeness Centrality: ')
            v2=[]
            for i in t2.keys():
                if(t2[i]==max(t2.values())):
                    v2.append(i);
                    print('Node '+str(i));
            print('\nBetweeness Centrality')
            t3=nx.betweenness_centrality(G)
            print(nx.betweenness_centrality(G));
            print('\nMost Important node based on Betweeness Centrality: ')
            v3=[]
            for i in t3.keys():
                if(t3[i]==max(t3.values())):
                    v3.append(i);
                    print('Node '+str(i));
            print('\n\nMost Important Node in the network: ')
            for i in v1:
                if(i in v2 and i in v3):
                    print('Node '+str(i)+' - '+screen_names[i]);
            plt.subplot(1,2,2)
            G=nx.Graph();
            nx.draw(G);
            for i in range(8):
                plt.text(0.5, 0.2+(i*0.08), str(i)+'-'+screen_names[i], horizontalalignment='center', verticalalignment='center', fontsize=9)
            plt.savefig('social1/'+q+'4.png')
            plt.show();
            plt.close('all');
        ans=int(input('\nDo you want to continue?'))
    
def advance_analysis():
    CONSUMER_KEY = '2D2qQNR2rSUwzulwEGFPXR3zp'
    CONSUMER_SECRET = 's7A2pwgTvoOdZvzbA5lzP06YG9tm3IST9qZjkAkF2spKrXxyW1'
    OAUTH_TOKEN = '1007573251231383553-nu1OkcCDaJDLd9UDVsVZx6FFKy5BKo'
    OAUTH_TOKEN_SECRET = '2L10gEAkQnGeZe4g88d13mgywW6eOoRYkiBN8kFhvixE1'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    q = str(input('Enter a Name to Search: '))
    count = int(input('\nEnter the number of tweets to fetch: '))
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']

    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:  
            break
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    status_texts = [status['text']
                    for status in statuses]

    screen_names = [user_mention['screen_name']
                    for status in statuses
                    for user_mention in status['entities']['user_mentions']]

    hashtags = [hashtag['text']
                for status in statuses
                for hashtag in status['entities']['hashtags']]

    words = [w
             for t in status_texts
             for w in t.split()]

    screen_names=set(screen_names)
    screen_names=list(screen_names)
    print(' \n\n Texts From top 5 Tweets : ')
    print json.dumps(status_texts[0:5], indent=1)
    print(' \n\n User Names For top 5 Tweets : ')
    print json.dumps(screen_names[0:5], indent=1)
    print(' \n\n Hashtags From top 5 Tweets : ')
    print json.dumps(hashtags[0:5], indent=1)
    print(' \n\n Collection of the words collected from the tweets : ')
    print json.dumps(words[0:5], indent=1)
    retweets = [
        (status['retweet_count'],
         status['retweeted_status']['user']['screen_name'],
         status['text'])

        for status in statuses

        if status.has_key('retweeted_status')
    ]

    print(' \n\n Top Users who use this keyword: ')
    print json.dumps(screen_names[0:8], indent=1)
    
    print('\n\n Top Retweeters for the Tweet : ')
    retweets1 = twitter_api.statuses.retweets(id=317127304981667841)
    print [str(r['user']['screen_name']) for r in retweets1]

    for item in [words, screen_names, hashtags]:
        c = Counter(item)

    def lexical_diversity(tokens):
        try:
            return 1.0 * len(set(tokens)) / len(tokens)
        except:
            return 0;

    def average_words(statuses):
        total_words = sum([len(s.split()) for s in statuses])
        try:
            return 1.0 * total_words / len(statuses)
        except:
            return 0;

    print('\n\n Lexical Diversity in Words : ')
    print lexical_diversity(words)
    print('\n\n Lexical Diversity in Screen Names : ')
    print lexical_diversity(screen_names)
    print('\n\n Lexical Diversity in Hashtags : ')
    print lexical_diversity(hashtags)
    print('\n\n Lexical Diversity in Status Texts : ')
    print average_words(status_texts)

    sys.stdin.read(1)

def analyze_tweets():
    api = TwitterClient()
    q = input('Enter a Name to Search: ')
    tweets = api.get_tweets(query=q, count=1000)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("\n\nGood tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("\n\nBad tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    print("\n\nUnbiased tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
    t1 = Texttable()
    t2 = Texttable()
    print "\n\n"
    t1.add_row(['Good Tweets']);
    for tweet in ptweets[:10]:
        t1.add_row([tweet['text']]);
    print t1.draw()
    print "\n\n"
    t2.add_row(['Bad Tweets']);
    for tweet in ntweets[:10]:
        t2.add_row([tweet['text']]);
    print t2.draw()
    sys.stdin.read(1)


def search_tweet():
    api = TwitterClient()
    t = Texttable()
    print('\n1) Search by keyword\n2) Search by username');
    choice=int(input('Enter choice: '));
    if(choice==1):
        q = str(input('Enter a Name to Search: '))
        nu = int(input('\nEnter the number of tweets to fetch: '))
        tweets = api.get_tweets(query=q, count=100)
        
        i=1;
        t.add_row(['','Tweets']);
        for tweet in tweets[:nu]:
            t.add_row([i, tweet['text']]);
            i+=1;
        print t.draw()
    elif(choice==2):
        extractor = twitter_setup()
        q = str(input('Enter a Name to Search: '))
        nu = int(input('\nEnter the number of tweets to fetch: '))
        try:
            tweets = extractor.user_timeline(screen_name=q, count=100)
            t.add_row(['','Tweets']);
            i=1;
            for tweet in tweets[:nu]:
                t.add_row([i, tweet.text]);
                i+=1;
            print t.draw()
        except:
            print('User not found');
    sys.stdin.read(1)


def user():
    ch = 1
    while ch != 7:
        os.system('clear')
        print("-" * 50)
        print("User Menu")
        print("-" * 50)
        print('\n1) View Trends \n2) Search Tweets \n3) Analyze Tweets \n4) Advanced Tweet Analysis \n5) Community Detection and Graph Creation\n6) Network Models and Computation \n7) Exit')
        ch = int(input('\nEnter your choice : '))
        if ch == 1:
            view_trends()
        elif ch == 2:
            search_tweet()
        elif ch == 3:
            analyze_tweets()
        elif ch == 4:
            advance_analysis()
        elif ch == 5:
            combined_graph()
        elif ch == 6:
            network_models()
        elif ch ==7:
            print('\nApplication Closing')
        else:
            print('\nWrong choice entered, Please try again')
            sys.stdin.read(1)

def main():
    user()
    

main()

