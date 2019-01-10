#!/usr/bin/python3
import datetime
import os
from pytz import timezone
import sys

from O365 import Connection, Account

scope_helpers = ['Calendars.Read', 'User.Read', 'basic']
token_location = os.path.expanduser('~/o365_token.txt')

try:
    with open(os.path.expanduser('~/.password-store/outlook_'), 'r') as config:
        credentials = tuple(config.read().strip().split(','))
except:
    print("User credentials not found")
    sys.exit()

def authenticate():
    account = Account(credentials=credentials, token_file_name=token_location)
    account.authenticate(scopes=scope_helpers)
    # Move token file to default location

account = Account(credentials=credentials, token_file_name=token_location)
if not account.connection.check_token_file():
    print("Auth problem!")
    sys.exit()

schedule = account.schedule()
cal = schedule.get_default_calendar()

now = datetime.datetime.now()
future = now + datetime.timedelta(minutes=10)

# Get events that start in less than 10 minutes
q = cal.new_query('start').less_equal(future).chain('and').on_attribute('end').greater(future)
q.order_by('start', ascending=False)
events = cal.get_events(query=q)

if events:
    print("{} {}".format(events[0].start.strftime("%H:%M"), events[0].subject))
else:
    print("Nothing")


