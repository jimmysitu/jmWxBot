#!/usr/bin/python3

import requests
import json

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

    host = 'https://dwz.cn'
    path = '/admin/v2/create'
    url = host + path
    method = 'POST'
    content_type = 'application/json'

    token = opts.token

    headers = {'Content-Type':content_type, 'Token':token}

    Records = []
    if opts.inFile:
        with open(opts.inFile, 'r', encoding='utf-8') as jsonFile:
            Records = json.load(jsonFile)

    for r in Records:
        bodys = {'url':r['LongUrl']}
        response = requests.post(url=url, data=json.dumps(bodys), headers=headers)
        rsp = json.loads(response.text)
        if rsp['Code'] == 0:
            r['ShortUrl'] = rsp['ShortUrl']
        else:
            print(response.text)
            exit(1)

    with open(opts.outFile, 'w', encoding='utf-8') as jsonFile:
        json.dump(Records, jsonFile, ensure_ascii=False, indent=4, sort_keys=True)

    print('Updated records short url')
