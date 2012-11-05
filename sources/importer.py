#!/usr/bin/env python

import yaml
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="File to import", metavar="FILE")
(options, args) = parser.parse_args()

stream = open(options.filename, 'r')
print yaml.load(stream)