# twitter

Use tweet_util to parse tweets out of a file and loop through them
```
>>> from twitter.tweet_util import *
>>> tweets = parseFile('Twitter/america.json')
>>> for x in tweets:
...     if x['coordinates']: print x['coordinates']['coordinates']
... 
[-117.3745, 34.000369999999997]
[-77.355911300000002, 35.606658899999999]
[-86.363963299999995, 43.608619400000002]
etc..
```

Use tweetmap.py to put coordinates on a map
```
nathand8@SuperComputer ~ $ python twitter/tweetmap.py Twitter/america.json 
Input file: Twitter/america.json
Output file: map.html
Parsing tweets...
======= For file: Twitter/america.json =======
Total tweets: 2255 (100.000%)
Place IDs: 2243 (99.468%)
User Location: 1701 (75.432%)
Exact coords: 345 (15.299%)
Unicode Error count: 84 (text for these tweets will be lost)
```
