import json
import os

# Get a list of all the absolute paths to files full of twitter data
#base_folder = '/fslhome/seanlane/Twitter/' # Base Folder
base_folder = '/fslhome/nathand8/Twitter/' # Base Folder
tweet_filenames = [os.path.join(base_folder, each) for each in os.listdir(base_folder) if each.endswith('.json')]
tweet_filenames.sort() # Make sure they're in order
# To use these, import tweet_util.tweet_filenames


# Helper function: detect if a field is in a tweet
def field_exists(fld, line):
    return fld in line


# Helper function: remove any occurrences of the field in the line
def remove_field(fld, line):
    while field_exists(fld, line):
        start_pos = line.index(fld) # Starting where the field begins
        end_pos = line.index(',', start_pos) + 1 # Ending after the next comma after the field
        line = line[0:start_pos] + line[end_pos: len(line)] # Cut that field out
    return line


# List of fields that json.loads has a hard time parsing
fields_to_remove = ['"source":']

# Helper function: take a string and turn it into a json representation
# Also remove any fields that are known not to parse (fields to remove)
def jsonify(raw_text):
    try:
        for fld in fields_to_remove:
            raw_text = remove_field(fld, raw_text)
        return json.loads(raw_text)
    except:
        return False

# Helper function: print out the tweet in a nice json format
def prettyPrint(tweet):
    print json.dumps(tweet, sort_keys=True, indent=4)

# Parse the given file, pull out all the tweets,
#  returns a list of tweets
def parseFile(filename):
    fh = open(filename, 'r')
    tweet_list = []
    jsonify_fail_count = 0
    for line in fh.readlines():
        tweet = jsonify(line)
        if not tweet:
            jsonify_fail_count += 1
            continue
        tweet_list.append(tweet)

    if jsonify_fail_count:
        print "Error jsonifying tweets: count =", jsonify_fail_count
    return tweet_list

