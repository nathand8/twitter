
from twitter.tweetmap import *

def mapFile(tweets_filename, map_filename = "map.html", map = america):
    print "Parsing tweets..."
    tweets = parseFile(tweets_filename)
    print "======= For file:", tweets_filename, "======="
    processCountsForTweets(tweets)
    coordinates = []
    for t in tweets:
        coord = bestLocation(t)
        if coord:
            coordinates.append(coord)
    map = addCoordinates(map, coordinates)
    saveMap(map, map_filename)

items = [
        'fever',
        'cough',
        'headache',
        'sore throat',
        'sneeze',
        'runny nose'
]
items_colors = {
    'fever': '#FFCF68', 
    'cough': '#6CC0FD', 
    'headache': '#8EC866', 
    'sore throat': '#D22B1A', 
    'sneeze': '#F28AD7',  
    'runny nose': '#AB89C1'
}

all_tweets = parseFile('output.json')
tweets = all_tweets
#ret = all([addSentimentAnalysis(t) for t in tweets])
#if not ret: print "Error adding sentiment analysis to the tweets"
#tweets = [addSentimentAnalysis(t) for t in random_subset(iter(all_tweets), 500)]

coordinates = {
    'fever':[], 
    'cough':[], 
    'headache':[], 
    'sore throat':[], 
    'sneeze':[], 
    'runny nose':[] 
}
for t in tweets:
    coord = bestLocation(t)
    if coord:
        for symptom in t.get('symptoms'):
            coordinates[symptom].append(coord)

emap = pygmaps.maps(39.456334, -96.201513, 5)
for item in items:
    coords = coordinates.get(item)
    color = items_colors.get(item) or '#FFFFFF'
    if coords:
        print item, len(coords), color
        emap = addCoordinates(emap, coords, color=color)

saveMap(emap, "map.html")

# Generate PNG from HTML:
# ~/exploratory/python-webkit2png/webkit2png $ python scripts.py "file:///Users/nathand/exploratory/tryagain.html" -o output.png -F javascript -g 1382 786 -w 1 && open output.png