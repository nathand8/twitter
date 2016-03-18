import json
import os
import bz2

# Get a list of all the absolute paths to files full of twitter data
#base_folder = '/fslhome/seanlane/Twitter/' # Base Folder
#base_folder = '/fslhome/nathand8/Twitter/' # Base Folder
#tweet_filenames = [os.path.join(base_folder, each) for each in os.listdir(base_folder) if each.endswith('.json')]
#tweet_filenames.sort() # Make sure they're in order
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

# Helper function: pull the text out of a tweet
#    Also decodes the special characters
def extractText(tweet):
    text = tweet.get('text')
    if text:
        return str(text.encode('utf8'))
    else:
        return None

# Mapping of full state name to state abbreviation
us_states_abbrv = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'National': 'NA',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# Mapping of city names to state abbreviation (used in neighborhood matching)
neighborhood_cities = {
    'San Francisco': 'CA',
    'Daly City': 'CA'
}
        

# Helper function: getState
#    Look into the tweet and try to determine which state it comes from
def getState(tweet, verbose=False):
    place = tweet.get('place')
    if place:
        place_type = place.get('place_type')
        country_code = place.get('country_code')
        if place_type and country_code and country_code == 'US':
            if place_type == 'city':
                place_name = place.get('full_name')
                state = place_name.split(',')[-1].strip()
                return state
            elif place_type == 'admin':
                place_name = place.get('full_name')
                if place_name.split(',')[-1].strip() == 'US':
                    state_name = place_name.split(',')[0].strip()
                    state = us_states_abbrv.get(state_name)
                    if not state and verbose: 
                        print "Unknown state in US:", state_name
                    return state
            elif place_type == 'neighborhood':
                place_name = place.get('full_name')
                city = place_name.split(',')[-1].strip()
                state = neighborhood_cities.get(city)
                if not state and verbose:
                    print "Unknown city:", city
                return state
            else:
                if verbose: print 'Unknown place type:', place_type
                return None
        else:
            if verbose:
                if not place_type:
                    print "No place type:", place
                elif not country_code:
                    print "No country code:", country_code
                elif country_code != 'US':
                    print "Non US country:", country_code


# Decompress BZ2
#    Takes a filename that's compressed in bz2 format and decompresses it
#    Returns true if it succeeded, false if it failed
def decompressBZ2(input_filepath, output_filepath, verbose=True):
    if verbose:
        print "Decompressing .bz2 file", input_filepath
    new_file = open(output_filepath, 'wb')
    file = bz2.BZ2File(input_filepath, 'rb')
    for data in iter(lambda : file.read(100 * 1024), b''):
        new_file.write(data)
    new_file.close()
    return True

# Parse the given file, pull out all the tweets,
#  returns a list of tweets
def parseFile(filename):
    if filename.endswith('.bz2'):
        output_filepath = filename.strip('.bz2')
        if decompressBZ2(filename, output_filepath):
            filename = output_filepath
        else:
            print "Failed to decompress .bz2 file", filename
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

# Returns a string saying "list removed"
# or the original object
# repeats the process on all children
def removeListsRecursive(obj):
    if type(obj) == type([]):
        return "List Removed (removeListRec)"
    elif type(obj) == type({}):
        for key in obj.keys():
            obj[key] = removeListsRecursive(obj.get(key))
        return obj
    else:
        return obj
