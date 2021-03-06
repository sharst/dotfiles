#!/usr/bin/python
""" Parse and relay a notification """
import sys
import re
import os

def message(title, message, urgency='NORMAL'):
    os.system('notify-send "{}" "{}" --urgency={}'.format(title, message, urgency))

summary_replace = {' (Magazino)': '',
                   'Direct Message': ' '}
body_replace = {'magazino.hipchat.com': '',
                'mattermost.magazino.eu': '',
                '@': ''}


appname, summary, body, icon, urgency = sys.argv[1:]

try:
    # Split into summary and roomname, make roomname
    # lower case initials with hashtag prefix
    summary, rn = summary.split(" - ")
    rn = '#' + ''.join([r[0] for r in rn.split(' ')]).lower()
    rn = rn.rstrip('(')
    # Room name in italics
    summary = summary + " <i>" + rn + "</i>"
except:
    pass

try:
    # Replace arbitrary items
    for keyword, replaceword in summary_replace.iteritems():
        summary = summary.replace(keyword, replaceword)

    for keyword, replaceword in body_replace.iteritems():
        body = body.replace(keyword, replaceword)

    # Replace stuff in brackets
    body = re.sub('\[.*\]', '', body)
except:
    pass

# For mattermost, name is shown in body
summary, body = body.split(':', 1)

message(summary, body, urgency)
