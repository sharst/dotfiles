#!/usr/bin/python
""" Relay a notification, but replace keyword """
import sys
import subprocess

replace = {' (Magazino)': '',
           ' (Deploy Fiege)': ' #fiege',
           ' (Emergency Room)': ' #em',
           ' (Deployment)': ' #deploy',
           ' (Mastering Statistics)': ' #statistics',
           ' (Map Alignment Task Force)', ' #maps'}

appname, summary, body, icon, urgency = sys.argv[1:]

for keyword, replaceword in replace.iteritems():
    summary = summary.replace(keyword, replaceword)

subprocess.call(["notify-send", summary, body])
