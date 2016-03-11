import pygmaps
from tweet_util import *
from count_coordinates import *
from optparse import OptionParser
import sys

# Default maps
utah = pygmaps.maps(39.384507, -111.574680, 7)
america = pygmaps.maps(39.456334, -96.201513, 5)
# America Box for curl command: -132.800716,24.791677,-67.028126,48.859042

# Coordinates should be in this format:
#       coord = {
#           'x': 39.12324,
#           'y': -111.573231,
#           'text': "I'm here in the grand canyon..." (optional)
#       }
#
# The map object should be created from pygmaps library:
#       utah = pygmaps.maps(39.384507, -111.574680, 7)
#       addCoordinates(utah, coordinates)
#       utah.draw('mapOfUtah.html')
#
def addCoordinates(map_obj, coordinates, color = "#FF0000"):
    error_count = 0
    for coord in coordinates:

        text = extractText(coord)
        if text:
            text = text.replace('"', '\'')
            text = "<br>".join(text.splitlines())
        else:
            text = "--Undefined--"

        # Plot the point on the map
        # Notice the coordinates are swapped. This is on purpose because google maps
        #    expects them opposite of how twitter gives them
        map_obj.addpoint(coord['y'], coord['x'], color=color, title = text)

    if error_count:
        print "Unicode Error count:", error_count, "(text for these tweets will be lost)"

    return map_obj


# Save a map to an html format for display
def saveMap(map_obj, output_fh = "map.html"):
    map_obj.draw(output_fh)


# Helper function to find the best location for a tweet
# Returns a coordinate data structure (see above)
def bestLocation(tweet):

    # Exact coordinates
    if tweet.get('coordinates') and tweet.get('coordinates').get('coordinates'):
        tuple = tweet['coordinates']['coordinates']

    # Relative coordinates by place
    elif tweet.get('place'):
        tuple = tweet['place']['bounding_box']['coordinates'][0][0]

    # We have no coordinates
    else:
        return None

    return {
        'x':tuple[0],
        'y':tuple[1],
        'text':(tweet.get('text') + u' -' + tweet.get('user').get('screen_name'))}


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

if __name__ == "__main__":
    help_text = """
    %prog data/tweet_file.json
    """
    parser = OptionParser(usage=help_text, version="%prog 1.0")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        print "Incorrect number of arguments"
        parser.print_help()
        sys.exit(1)
    elif len(args) == 1:
        fh_input = args[0]
        fh_output = "map.html"
    elif len(args) == 2:
        fh_input = args[0]
        fh_output = args[1]

    print "Input file:", fh_input
    print "Output file:", fh_output
    mapFile(fh_input, fh_output)

