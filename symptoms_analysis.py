import re

# Remove Punctuation from a unicode string
# Copied from
# http://stackoverflow.com/questions/11066400/remove-punctuation-from-unicode-formatted-strings
import unicodedata
import sys

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                              if unicodedata.category(unichr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)
# End Remove Punctuation

def cleanText(tweet):
    if not tweet:
        return

    text = tweet.get('text')
    if not text:
        return None
    # remove retweet entities
    #text = re.sub("(RT|via)((?:\\b\\W*@\\w+)+)", "", text)
    # remove at people
    #text = re.sub("@\\w+", "", text, flags=re.U)
    if tweet.get('entities'):
        for mention in tweet.get('entities').get('user_mentions'):
            text = text.replace('@' + mention.get('screen_name'), '')
    # remove hashtags
    #for hashtag in tweet.get('entities').get('hashtags'):
    #   text = text.replace('#' + hashtag.get('text'), '')
    # remove html links
    if tweet.get('entities'):
        for url in tweet.get('entities').get('urls'):
            text = text.replace(url.get('url'), '')
    # remove punctuation
    text = remove_punctuation(text)
    # remove numbers
    text = re.sub("\d", "", text)
    # remove unnecessary spaces
    text = re.sub("[ \t]{2,}", " ", text)
    text = re.sub("^\\s+|\\s+$", "", text)
    text = text.lower()
    return text

symptoms = [
        'fever',
        'cough',
        'headache',
        'sore throat',
        'sneeze',
        'runny nose'
]

def addSymptomChecks(tweet):
    # Addes attributes to a tweet based on symptoms found in text

    if not tweet:
        return None
    if not tweet.get('text'):
        return tweet

    tweet['symptoms'] = []
    text = cleanText(tweet)
    for symptom in symptoms:
        if symptom in text:
            tweet['symptoms'].append(symptom)

    return tweet
