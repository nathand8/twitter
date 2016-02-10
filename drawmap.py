import pygmaps

utah = pygmaps.maps(39.384507, -111.574680, 7)

fh = open('tweets_and_locations.txt', 'r')
#fh = open('small.txt', 'r')
for x in fh.readlines():
    try:
        c1 = x[1: x.index(',')]
        c2 = x[x.index(',') + 1: x.index(']')]
        m = x[x.index(']') + 3: len(x) - 2]
        m.replace('\n', ' ')
        utah.addpoint(float(c1), float(c2), color = '#FF0000', title = m)
    except:
        print x

utah.draw('test.html')

