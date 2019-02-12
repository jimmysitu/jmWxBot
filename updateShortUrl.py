#!/usr/bin/python3

import requests
import json
import time

from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest="inFile",
                      help="Intput file in json format")
    parser.add_option('-o', '--output', dest="outFile",
                      help="Output file in json format")
    parser.add_option('-t', '--token', dest="token",
                      help="Selected subject")

    (opts, args) = parser.parse_args()

    url = 'http://api.suolink.cn/api.php'


    Records = []
    if opts.inFile:
        with open(opts.inFile, 'r', encoding='utf-8') as jsonFile:
            Records = json.load(jsonFile)

    for r in Records:
        payloads = {'url':"urlencode('%s')" % r['LongUrl'], 'format':'json', 'key':opts.token}
        response = requests.get(url=url, params=payloads)
        rsp = json.loads(response.text)
        if rsp['err'] == "":
            print(response.text)
            print("Updated short url from %s to %s" %(r['ShortUrl'], rsp['url']))
            r['ShortUrl'] = rsp['url']
            time.sleep(2)
        else:
            print(response.text)
            exit(1)

    with open(opts.outFile, 'w', encoding='utf-8') as jsonFile:
        json.dump(Records, jsonFile, ensure_ascii=False, indent=4, sort_keys=True)

    print('Updated records short url')
