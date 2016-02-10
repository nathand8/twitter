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
