#!/usr/bin/python3

import wxpy
import json

from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest="inFile",
                      help="Intput file in json format")
    parser.add_option('-s', '--subject', dest="subject",
                      help="Selected subject")

    (opts, args) = parser.parse_args()

    Records = []
    if opts.inFile:
        with open(opts.inFile, 'r', encoding='utf-8') as jsonFile:
            Records = json.load(jsonFile)

    msg = "【%s】\n" % opts.subject
    for r in Records:
        if r['Subject'] == opts.subject:
            msg = msg + ("%s\n" % r['Text'])
            msg = msg + ("%s\n" % r['ShortUrl'])

    bot = wxpy.Bot(console_qr=True)
    bot.self.send(msg)
    print("Send Message:")
    print(msg)
