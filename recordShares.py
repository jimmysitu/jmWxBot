#!/usr/bin/python3

import wxpy
import urllib.request
import json

from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest="inFile",
                      help="Output file in json format")
    parser.add_option('-o', '--output', dest="outFile",
                      help="Output file in json format")

    (opts, args) = parser.parse_args()

    Record = []
    if opts.inFile:
        with open(opts.inFile, 'r', encoding='utf-8') as jsonFile:
            Record = json.load(jsonFile)

    bot = wxpy.Bot(console_qr=True)

    @bot.register(chats=[bot.self], msg_types=wxpy.SHARING, except_self=False)
    def register_sharing(msg):
        global Record
        print(msg)
        for i in range(0, len(Record)):
            if Record[i]['Text'] == msg.text:
                Record[i] = {
                    'Text': msg.text,
                    'LongUrl': msg.url,
                    'ShortUrl': urllib.request.urlopen("http://tinyurl.com/api-create.php?url=%s" % msg.url).read().decode('utf-8')
                }
                return Record[i]['ShortUrl']
            else:
                Record.append(
                    {
                        'Text': msg.text,
                        'LongUrl': msg.url,
                        'ShortUrl': urllib.request.urlopen("http://tinyurl.com/api-create.php?url=%s" % msg.url).read().decode('utf-8')
                    }
                )
                return Record[-1]['ShortUrl']

    @bot.register(chats=[bot.self], msg_types=wxpy.TEXT, except_self=False)
    def regiter_text(msg):
        global Record
        if msg.text == 'end':
            with open(opts.outFile, 'w', encoding='utf-8') as jsonFile:
                json.dump(Record, jsonFile, ensure_ascii=False, indent=4, sort_keys=True)
            jsonFile.close()
            bot.logout()
        elif msg.text == 'save':
            with open(opts.outFile, 'w', encoding='utf-8') as jsonFile:
                json.dump(Record, jsonFile, ensure_ascii=False, indent=4, sort_keys=True)
                print('Saved records')
        elif msg.text == 'reload':
            if opts.inFile:
                with open(opts.inFile, 'r', encoding='utf-8') as jsonFile:
                    Record = json.load(jsonFile)
                print('Reloaded records')
            else:
                print('No input file, cannot reload')



    wxpy.embed()
    #bot.join()


