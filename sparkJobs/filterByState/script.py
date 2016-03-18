import sys
import os
import time

from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="TwitterFilterStates")

# Import tweet_util
sc.addPyFile("/fslhome/nathand8/twitter/tweet_util.py")
from tweet_util import *

if len(sys.argv) not in [3, 4]:
    print "Usage: filterByState.py <input_folder> <output_folder>"
    print "    Outputs only tweets with a state associated with them"
    print "    Put a True at the end if the data should discretize on the first directory"
    print sys.argv
    exit(-1)

target = sys.argv[1]
output = sys.argv[2]

# See if it should split on the first directory
if len(sys.argv) == 4 and sys.argv[3] in ['T', 'True', 'true', 'yes', 'y', 'Y', 'split', 'Split', '-s', '-S']:
    split = True
else:
    split = False

if split:
    target_folder = target.split('*')[0]
    rest = target.split('*')[1:]
    dirs = [{'target': os.path.join(target_folder,o,'*'.join(rest).strip('/')), 'output': os.path.join(output,o)}  for o in os.listdir(target_folder) if os.path.isdir(os.path.join(target_folder,o))]
else:
    dirs = [{'target': target, 'output': output}]

# Testing timing (DELETEME)
#import random

def filterFile(input_dir, output_dir):
    print 
    print "=========================================================="
    print "Working on folder", input_dir
    print "Outputing to folder", output_dir
    print time.strftime("%c")
    print "=========================================================="
    print 

    # Dry Run
    #time.sleep(random.random())
    #return True

    lines = sc.textFile(input_dir)
    result = lines.map(lambda x: jsonify(x)) \
            .filter(lambda tweet: tweet) \
            .filter(lambda tweet: getState(tweet)) \
            .map(lambda tweet: json.dumps(tweet)) \
            .saveAsTextFile(output_dir)

    print
    print "============ Results ==========="
    print output
    print
    print
    print "============ Finished ==========="
    print
    return True

for d in dirs:
    start_time = time.time()
    ret = filterFile(d['target'], d['output'])
    if not ret:
        print "Something failed on the last job"
    end_time = time.time()
    seconds_elapsed = end_time - start_time
    minutes_elapsed = seconds_elapsed/60
    print 
    print "=========================================================="
    print "Time Elapsed: %.2f seconds (%.2f minutes)" % (seconds_elapsed, minutes_elapsed)
    print "=========================================================="
    print 

sc.stop()
