#!/usr/bin/python
""" Parse and relay a notification """
import sys
import os

def message(title, message, urgency='NORMAL'):
    os.system('notify-send "{}" "{}" --urgency={}'.format(title, message, urgency))

replace = {' (Magazino)': ''}

appname, summary, body, icon, urgency = sys.argv[1:]

try:
    # Split into summary and roomname, make roomname
    # lower case initials with hashtag prefix
    summary, rn = summary.split(" - ")
    rn = '#' + ''.join([r[0] for r in rn.split(' ')]).lower()

    # Replace arbitrary items
    for keyword, replaceword in replace.iteritems():
        summary = summary.replace(keyword, replaceword)

    # Room name in italics
    summary = summary + " <i>" + rn + "</i>"
except:
    pass

message(summary, body, urgency)
