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
    error_count = 0
    for coord in coordinates:

        if 'text' in coord.keys():
            try:
                text = str(coord['text'])
                text = text.replace('"', '\'')
                text = "<br>".join(text.splitlines())
            except UnicodeEncodeError:
                error_count += 1
                text = ""
        else:
            text = ""

        # Plot the point on the map
        # Notice the coordinates are swapped. This is on purpose because google maps
        #    expects them opposite of how twitter gives them
        map_obj.addpoint(coord['y'], coord['x'], color=color, title = text)

    if error_count:
        print "Unicode Error count:", error_count

    return map_obj

# Save a map to an html format for display
def saveMap(map_obj, output_fh = "map.html"):
    map_obj.draw(output_fh)
