# Import stuff to interface with r
from rpy2.robjects import r

# Import libraries for r
r('library("sentiment")')

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
	r.assign("text", text)
	return r('classify_emotion(data.frame(text), algorithm="bayes", prior=1.0)')

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