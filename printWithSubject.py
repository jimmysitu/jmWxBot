#!/usr/bin/python3

import json

from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest="inFile",
                      help="Intput file in json format")
    parser.add_option('-s', '--subject', dest="subject",
                      help="Output file in json format")

    (opts, args) = parser.parse_args()

    Records = []
    if opts.inFile:
        with open(opts.inFile, 'r', encoding='utf-8') as jsonFile:
            Records = json.load(jsonFile)

    for r in Records:
        if r['Subject'] == opts.subject:
            print(r['Text']);
            print(r['ShortUrl']);


