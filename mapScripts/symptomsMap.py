import sys
from twitter.tweetmap import *

items_colors_map = {
    'fever': '#FFCF68', 
    'cough': '#6CC0FD', 
    'headache': '#8EC866', 
    'sore throat': '#D22B1A', 
    'sneeze': '#F28AD7',  
    'runny nose': '#AB89C1'
}

def getCoordinates(tweets, items_colors_map):

    # Initialize the map of items to coordinates
    coordinates = {}
    for item in items_colors_map.keys():
        coordinates[item] = []

    # Add coordinates to their
    for t in tweets:
        coord = bestLocation(t)
        if coord:
            for symptom in t.get('symptoms'):
                coordinates[symptom].append(coord)
    return coordinates

def putCoordinatesOnMap(coordinates, items_colors_map):
    # Put the coordinates on a map of the US
    emap = pygmaps.maps(39.456334, -96.201513, 5)
    for item in items_colors_map.keys():
        coords = coordinates.get(item)
        color = items_colors_map.get(item) or '#FFFFFF'
        if coords:
            print item, len(coords), color
            emap = addCoordinates(emap, coords, color=color)
    return emap

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: filename.py input_file.json output_file.html"
        print "    This will parse in tweets with symptoms already attached"
        print "    and put them on a map, color coordinated by symptom"
        sys.exit()

    input = sys.argv[1]
    output = sys.argv[2]

    tweets = parseFile(input)
    coordinates = getCoordinates(tweets, items_colors_map)
    america = putCoordinatesOnMap(coordinates, items_colors_map)

    saveMap(america, output)
