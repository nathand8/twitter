import sys
import os
import time

from pyspark import SparkContext
from operator import add

sc = SparkContext()

# Import tweet_util
sc.addPyFile("/fslhome/nathand8/twitter/tweet_util.py")
from tweet_util import *

# Import symptoms_analysis
sc.addPyFile("/fslhome/nathand8/twitter/symptoms_analysis.py")
from symptoms_analysis import *

if len(sys.argv) != 3:
    print "Usage: filename.py <input_folder> <output_folder>"
    print "    Outputs only tweets with symptoms associated with them"
    print sys.argv
    exit(-1)

target = sys.argv[1]
output = sys.argv[2]

print 
print "=========================================================="
print "Working on folder", target
print "Outputing to folder", output
print time.strftime("%c")
print "=========================================================="
print 

lines = sc.textFile(target)
result = lines.map(lambda x: jsonify(x)) \
        .filter(lambda tweet: tweet) \
        .map(addSymptomChecks) \
        .filter(lambda tweet: len(tweet.get('symptoms')) > 0) \
        .map(lambda tweet: json.dumps(tweet)) \
        .saveAsTextFile(output)

print
print "============ Results ==========="
print result
print
print
print "============ Finished ==========="
print
sc.stop()
