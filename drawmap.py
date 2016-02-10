import pygmaps

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
    for coord in coordinates:
        if 'text' in coord.keys():
            text = coord['text']
        else:
            text = ""
        map_obj.addpoint(coord['x'], coord['y'], color=color, title = text)

# Save a map to an html format for display
def saveMap(map_obj, output_fh = "map.html"):
    map_obj.draw(output_fh)
