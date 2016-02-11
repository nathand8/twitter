import pygmaps
from tweet_util import *
from count_coordinates import *
from optparse import OptionParser
import sys

# Default maps
utah = pygmaps.maps(39.384507, -111.574680, 7)
america = pygmaps.maps(39.456334, -96.201513, 5)

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

        if 'text' in coord.keys():
            try:
                text = str(coord['text'])
                text = text.replace('"', '\'')
                text = "<br>".join(text.splitlines())
            except UnicodeEncodeError:
                error_count += 1
                text = "--Unicode Encoding Error--"
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

def mapFile(tweets_filename, map_filename = "map.html", map = america):
    print "Parsing tweets..."
    tweets = parseFile(tweets_filename)
    print "======= For file:", tweets_filename, "======="
    processCountsForTweets(tweets)
    coordinates = []
    for t in tweets:
        if 'coordinates' in t and t['coordinates']:
            coordinates.append({
                'x':t['coordinates']['coordinates'][0],
                'y':t['coordinates']['coordinates'][1],
                'text':t['text']
                })

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

