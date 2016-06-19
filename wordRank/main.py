# coding=utf-8
import time
import datetime
import sys
import re
import urllib
import urllib2
import argparse
import os

opener = urllib2.build_opener()
agents = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
]
# opener.addheaders = [('User-agent', '')]

SLEEP = 61

cnt = 0
failCnt = 0
startLine = 0
errorSleep = SLEEP
filename = sys.argv[1]
if len(sys.argv) > 2:
    startLine = int(sys.argv[2])
for line in open(filename):
    if cnt < startLine:
        cnt += 1
        continue
    end = line.find(',')
    word = line[:end]
    url = "http://search.yahoo.co.jp/search?ei=UTF-8&p={0}".format(word)
    agentId = cnt % len(agents)
    opener.addheaders = [('User-agent', agents[agentId])]
    try:
        response = opener.open(url)
        html = response.read()
    except urllib2.URLError, e:
        if failCnt == 1:
            agents.pop(agentId)
            sys.stderr.write('pop agent {0}'.format(agentId))
            failCnt = 0
        else:
            failCnt = 1
        sys.stderr.write('{0} wait {1} sec'.format(e.reason, errorSleep))
        sys.stderr.flush()
        time.sleep(errorSleep)
        errorSleep *= 2
        continue
    errorSleep = SLEEP
# fail if it includes 約くぁwせdrftgyふじこlp；件
# re.findall searches the all of html
    start = html.find('約') + len('約')
    if '約' in word:
        start = html.find('約', html.find('検索した結果')) + len('約')
    end = html.find('件', start)
    sys.stderr.write('{0} '.format(cnt))
    print('{0}\t{1}'.format(word, html[start:end]))
    sys.stdout.flush()
    cnt += 1
# you shouldn't make this value too small
    time.sleep(10)

