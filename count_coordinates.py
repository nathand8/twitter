import tweet_util
import os
from optparse import OptionParser

def processCountsForMultipleFiles(file_list, prompt_every_file = True):
    for filename in file_list:
        processCountsForFile(filename)
        if prompt_every_file and raw_input('Would you like to stop? [y,N] ').lower() in ['y', 'yes', 'Y', 'Yes']:
            exit()
    print "End of file list"

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
    help_text = """
    %prog data/tweet_file.json
    """
    parser = OptionParser(usage=help_text, version="%prog 1.0")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        fh_input = False
    elif len(args) == 1:
        fh_input = args[0]
    elif len(args) == 2:
        fh_input = args[0]

    print "Input file:", fh_input

    if fh_input:
        if os.path.isdir(fh_input):
            tweet_filenames = [os.path.join(fh_input, each) for each in os.listdir(fh_input) if (each.endswith('.json') or each.endswith('.bz2'))]
            processCountsForMultipleFiles(tweet_filenames, False)
        else:
            processCountsForFile(fh_input)
    else:
        processCountsForMultipleFiles(tweet_filenames, True)
