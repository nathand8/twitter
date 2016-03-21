from twitter.tweet_util import *

# Get a random subset
# Stolen from
# http://stackoverflow.com/questions/2612648/reservoir-sampling
import random
def random_subset( iterator, K ):
    result = []
    N = 0
    for item in iterator:
        N += 1
        if len( result ) < K:
            result.append( item )
        else:
            s = int(random.random() * N)
            if s < K:
                result[ s ] = item
    return result
# End of random subset

# Remove Punctuation from a unicode string
# Copied from
# http://stackoverflow.com/questions/11066400/remove-punctuation-from-unicode-formatted-strings
import unicodedata
import sys
import re

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)
# End Remove Punctuation

# Import stuff to interface with r
import numpy as np
from rpy2.robjects import r
import pandas.rpy.common as com
from pandas import DataFrame

# Import libraries for r
r('library("sentiment")')

def addSentimentAnalysis(tweet):
	sa = sentimentAnalysis(tweet)
	tweet['sentiment_anger'] = sa[0]
	tweet['sentiment_disgust'] = sa[1]
	tweet['sentiment_fear'] = sa[2]
	tweet['sentiment_joy'] = sa[3]
	tweet['sentiment_sadness'] = sa[4]
	tweet['sentiment_surprise'] = sa[5]
	tweet['sentiment_bestfit'] = sa[6] if type(sa[6]) is str else None
	return tweet

def cleanText(tweet):
	text = tweet.get('text')
	# remove retweet entities
	text = re.sub("(RT|via)((?:\\b\\W*@\\w+)+)", "", text, flags=re.U)
	# remove at people
	#text = re.sub("@\\w+", "", text, flags=re.U)
	for mention in tweet.get('entities').get('user_mentions'):
		text = text.replace('@' + mention.get('screen_name'), '')
	# remove hashtags
	#for hashtag in tweet.get('entities').get('hashtags'):
	#	text = text.replace('#' + hashtag.get('text'), '')
	# remove html links
	for url in tweet.get('entities').get('urls'):
		text = text.replace(url.get('url'), '')
	# remove punctuation
	text = remove_punctuation(text)
	# remove numbers
	text = re.sub("\d", "", text, flags=re.U)
	# remove unnecessary spaces
	text = re.sub("[ \t]{2,}", " ", text, flags=re.U)
	text = re.sub("^\\s+|\\s+$", "", text, flags=re.U)
	text = text.lower()
	return text

def sentimentAnalysis(tweet):
	text = cleanText(tweet)
	r.assign("foo", text)
	return r('classify_emotion(data.frame(foo), algorithm="bayes", prior=1.0)')

def roughTimeOfDay(raw_tweet_time):
	# 6 = Late Night (0 - 3)
	# 1 = Early morning (4 - 7)
	# 2 = Late morning (8 - 11)
	# 3 = Afternoon (12 - 15)
	# 4 = Early Evening (16 - 19)
	# 5 = Late Evening (20 - 23)
	hour = int(raw_tweet_time.split(' ')[3].split(':')[0])
	if hour in range(0,4):
		return 6
	elif hour in range(4,8):
		return 1
	elif hour in range(8,12):
		return 2
	elif hour in range(12,16):
		return 3
	elif hour in range(16,20):
		return 4
	elif hour in range(20, 24):
		return 5

def determineNumberOfFactorsToExtract(data):
	# Given some data, determine the number of factors you should extract.
	# Creates a graph and displays it so you can choose
	# Stolen from
	# http://www.statmethods.net/advstats/factor.html
	r('library(nFactors)')
	r.assign('data', data)
	r('ev = eigen(cor(data))')
	r('ap = parallel(subject=nrow(data),var=ncol(data),rep=100,cent=0.5')
	r('nS = nScree(x=ev$values, aparallel=ap$eigen$qevpea)')
	r('plotnScree(nS)')
	return

days = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}

if __name__ == "__main__":
	all_tweets = parseFile('sample.json')
	tweets = random_subset(iter(all_tweets), 500)
	ret = all([addSentimentAnalysis(t) for t in tweets])
	if not ret: print "Error adding sentiment analysis to the tweets"
	#tweets = [addSentimentAnalysis(t) for t in random_subset(iter(all_tweets), 500)]

	rows_list = []
	for tweet in tweets:
		rows_list.append({
			'tweet_length': len(tweet.get('text')),
			'hour_of_the_day' : int(tweet.get('created_at').split(' ')[3].split(':')[0]),
#			'rough_time_of_day' : roughTimeOfDay(tweet.get('created_at')),
#			'day_of_week' : days.get(tweet.get('created_at').split(' ')[0]),
			'user_friends_count': tweet.get('user').get('friends_count'),
			'user_followers_count': tweet.get('user').get('followers_count'),
			'user_statuses_count': tweet.get('user').get('statuses_count'),
			'is_english': 1 if tweet.get('lang') == 'en' else 0,
			'hashtags_count': len(tweet.get('entities').get('hashtags')),
			'urls_count': len(tweet.get('entities').get('urls')),
			'user_mentions_count': len(tweet.get('entities').get('user_mentions')),
#			'annoyed_face_presence': 1 if u'\U0001f612' in tweet.get('text') else 0,
#			'sad_face_presence': 1 if u'\U0001f614' in tweet.get('text') else 0,
#			'heart_emoji_presence': 1 if u'\u2764' in tweet.get('text') else 0,
#			'crying_lauging_face_presence': 1 if u'\U0001f602' in tweet.get('text') else 0,
			'kissy_winky_face_presence': 1 if u'\U0001f618' in tweet.get('text') else 0,
#			'smily_face_presence': 1 if u'\U0001f60a' in tweet.get('text') else 0,
			'sentiment_anger': float(tweet.get('sentiment_anger')),
#			'sentiment_disgust': float(tweet.get('sentiment_disgust')),
#			'sentiment_fear': float(tweet.get('sentiment_fear')),
#			'sentiment_joy': float(tweet.get('sentiment_joy')),
#			'sentiment_sadness': float(tweet.get('sentiment_sadness')),
#			'sentiment_surprise': float(tweet.get('sentiment_surprise')),
#			'favorited': 1 if tweet.get('favorited') else 0,
#			'retweet_count': tweet.get('retweet_count'),
		})

	# Use R to run the factor analysis
	# Stolen from
	# http://www.statmethods.net/advstats/factor.html
	df = DataFrame(rows_list) 
	r.assign("pydata", com.convert_to_r_dataframe(df))
	results = None
	results = r('factanal(pydata, 3, rotation="varimax")')
	if results: print results

