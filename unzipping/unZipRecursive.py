#! /usr/bin/env python

from twitter import tweet_util
import sys
import optparse
import os

class Main(object):
    def __init__(self):
        self.verbose = False
        self.debug = False
        self.parse_options()

    def msg(self, text):
        if self.verbose:
            print text

    def parse_options(self):
        parser = optparse.OptionParser(usage = "%prog [options]",
                                       version = "%prog 0.1")

        parser.add_option("-f","--filename",type="str",dest="filename",
                          default='test.json',
                          help="filename to send")

        parser.add_option("-d","--debug",dest="debug",
                          action="store_true",
                          help="debug, don't actually do anything to the files "
                                  "just print out the names. this will automatically "
                                  "turn on the verbose option")

        parser.add_option("-v","--verbose",dest="verbose",
                          action="store_true",
                          help="print out help statements")

        (options,args) = parser.parse_args()
        self.filename = options.filename
        self.debug = options.debug
        self.verbose = options.verbose or options.debug

        if not os.path.exists(self.filename):
            parser.print_help()
            parser.error("The file you input (" + self.filename + ") doesn't exist")
            sys.exit(1)

    def recursiveUnzip(self, folder):

        # don't scan if it isn't a folder
        if not os.path.isdir(folder):
            return

        # list all the .bz2 files in the current directory,
        bz2_files = [each for each in os.listdir(folder) if each.endswith('.bz2')]

        # for all the .bz2 files:
        for file in bz2_files:
            zip_file = os.path.join(folder, file)
            output_file = zip_file.strip(".bz2")

            # if the unzipped version already exists, skip it
            if os.path.isfile(output_file):
                self.msg("Skipping " + zip_file)
                continue

            # unzip the file to its same name - ".bz2"
            if self.debug:
                self.msg("Would decompress " + zip_file)
            else:
                tweet_util.decompressBZ2(zip_file, output_file, verbose=self.verbose)


        # list all the directories in the current directory
        nested_dirs = [os.path.join(folder, each) for each in os.listdir(folder) if os.path.isdir(os.path.join(folder, each))]

        # for all the directories:
        for dir in nested_dirs:
            # recursively unzip
            self.recursiveUnzip(dir)


    def run(self):
        if self.debug:
            self.msg("Debugging. Files won't really be changed")
        if self.verbose:
            self.msg("Verbose mode")

        # go into the file recursively
        self.recursiveUnzip(self.filename)



if __name__ == "__main__":
    m = Main()
    m.run()
