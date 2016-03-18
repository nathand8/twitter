from factorAnalysis import *

def mapEmotionsFile(tweets_filename, map_filename = "map.html", map = america):
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

emotions = ['joy', 'sadness', 'disgust', 'unknown', 'anger', 'surprise', 'fear']
emotions_colors = {'joy': '#FFCF68', 'sadness': '#6CC0FD', 'disgust': '#8EC866', 'anger': '#D22B1A', 'surprise': '#F28AD7',  'fear': '#AB89C1', 'unknown': '#434343'}

#if __name__ == "__main__":
all_tweets = parseFile('sample.json') # lines.map(jsonify).filter(lambda tweet: tweet)
tweets = random_subset(iter(all_tweets), 500)
ret = all([addSentimentAnalysis(t) for t in tweets])
if not ret: print "Error adding sentiment analysis to the tweets"
#tweets = [addSentimentAnalysis(t) for t in random_subset(iter(all_tweets), 500)]

coordinates = {'joy':[], 'sadness':[], 'disgust':[], 'anger':[], 'surprise':[], 'fear':[], 'unknown':[]}
for t in tweets:
	coord = bestLocation(t)
	if coord:
		bestfit = t.get('sentiment_bestfit') or 'unknown'
		coordinates[bestfit].append(coord)

emap = pygmaps.maps(39.456334, -96.201513, 5)
for emotion in emotions:
	coords = coordinates.get(emotion)
	color = emotions_colors.get(emotion) or '#FFFFFF'
	if coords:
		print emotion, len(coords), color
		emap = addCoordinates(emap, coords, color=color)

saveMap(emap, "tryagain.html")

# Generate PNG from HTML:
# ~/exploratory/python-webkit2png/webkit2png $ python scripts.py "file:///Users/nathand/exploratory/tryagain.html" -o output.png -F javascript -g 1382 786 -w 1 && open output.png