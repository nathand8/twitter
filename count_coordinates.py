import tweet_util


def processCountsForFile(filename):
    print "======= For file:", filename, "======="
    processCountsForTweets(tweet_util.parseFile(filename))

def processCountsForTweets(tweets):
    exact_coord_ct = 0
    user_loc_ct = 0
    place_id_ct = 0
    total_tweets_ct = 0
    for tweet in tweets:
        total_tweets_ct += 1
        if ('geo' in tweet and tweet['geo'] and 'coordinates' in tweet['geo'] and tweet['geo']['coordinates']):
            exact_coord_ct += 1
        if ('user' in tweet and tweet['user'] and 'location' in tweet['user'] and tweet['user']['location']):
            user_loc_ct += 1
        if ('place' in tweet and tweet['place'] and 'id' in tweet['place'] and tweet['place']['id']):
            place_id_ct += 1

    print "Total tweets:", total_tweets_ct, "(%.3f%%)" % (float(total_tweets_ct)/float(total_tweets_ct)*100)
    print "Place IDs:", place_id_ct, "(%.3f%%)" % (float(place_id_ct)/float(total_tweets_ct)*100)
    print "User Location:", user_loc_ct, "(%.3f%%)" % (float(user_loc_ct)/float(total_tweets_ct)*100)
    print "Exact coords:", exact_coord_ct, "(%.3f%%)" % (float(exact_coord_ct)/float(total_tweets_ct)*100)
    

if __name__ == "__main__":
    for filename in tweet_util.tweet_filenames:
        processCountsForFile(filename)
        if raw_input('Would you like to stop? [y,N] ').lower() in ['y', 'yes', 'Y', 'Yes']:
            exit()
    print "End of file list"
