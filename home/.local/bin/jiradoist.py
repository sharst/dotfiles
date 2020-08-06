#!/usr/bin/python
# A little script to upload my JIRA tickets to todoist

import datetime
import os
import time
import shutil

from jira import JIRA, JIRAError
from todoist.api import TodoistAPI
import todoist
import requests
from ruamel.yaml import safe_load

from pprint import PrettyPrinter
dt = PrettyPrinter(indent=4)


config = safe_load(open(os.path.expanduser('~/.jiradoist_config.yaml')))

# Mapping from JIRA priority (1-5) to todoist priority (1-4)
priority_mapping = {unicode(i): min(i,4) for i in range(6)}

# Just convenience to remember the todoist colors
class colors:
    GREEN = 0
    SLIME = 1
    RED = 2
    PINK = 3
    PURPLE = 4
    BLUE = 5
    PETROL = 6
    GRAY = 7
    DARKPETROL = 8
    TURQUOISE = 9
    DARK_RED = 10
    LIGHT_GREEN = 11
    BLACK = 12



# Mapping from JIRA status to Todoist label color
label_colors = {u'Open': colors.GRAY,
                u'Committed': colors.GRAY,
                u'In progress': colors.SLIME,
                u'Waiting': colors.SLIME,
                u'To be reviewed': colors.PETROL,
                u'Done': colors.GREEN,
                u'Released': colors.GREEN,
                u'To Do': colors.GRAY,
                u'Backlog': colors.GRAY}

JQL_PROJECT_MAPPING = config.get('jql_project_mapping', {})
JIRA_SERVER = config.get('jira_server_url')
JIRA_KEYFILE = config.get('jira_keyfile')
PASSWORD_BASE = os.path.expanduser(config.get('config_path', '~'))
SYNC_EVERY = config.get('sync_every', 300)


def search_all_issues(jira, jql_str, fields=None):
    """
    Extends jira.search_issues and returns not only the first 50 issues but all issues found
    :param jira: jira.JIRA instance
    :param jql_str: the JQL search string to use
    :param fields: comma-separated string of issue fields to include in the results
    :return: list of jira issues
    """
    issue_matches = jira.search_issues(jql_str, maxResults=100, fields=fields)
    # maxResults seems to not be working for values higher than 100 or False, so
    # we need to catch the issues in batches:
    while len(issue_matches) < issue_matches.total:
        issue_matches += (jira.search_issues(
            jql_str, startAt=len(issue_matches), maxResults=100, fields=fields))
    return issue_matches


JIRA.DEFAULT_OPTIONS['server'] = JIRA_SERVER


class JiradoistSyncher(object):
    def __init__(self):
        while True:
            try:
                self._setup_jira()
                self._setup_todoist()
                break
            except Exception as e:
                print "Setup failed, trying again in 10 s"
                print e
                time.sleep(10)

    def _setup_jira(self):
        with open(os.path.join(PASSWORD_BASE, 'jira_'), 'r') as config:
            access_token, access_token_secret = config.read().strip().split(',')

        with open(os.path.join(PASSWORD_BASE, JIRA_KEYFILE), 'r') as keyf:
            key_cert = keyf.read()

        oauth_dict = {'access_token': access_token,
                'access_token_secret': access_token_secret,
                'consumer_key': 'jira-api-tests',
                'key_cert': key_cert}
        self.jira = JIRA(oauth=oauth_dict)

    def _setup_todoist(self):
        self.clear_temp()
        # Set up Todoist
        with open(os.path.join(PASSWORD_BASE, 'todoist_'), 'r') as config:
            self.td_api = TodoistAPI(config.read().strip())
        self.safe_sync()

    def get_or_create_label(self, text, color):
        label = next((label for label in self.td_api.labels.all()
                      if label['name'] == text and
                      label['color'] == color),
                     None)

        if not label:
            label = self.td_api.labels.add(text, color=color)

        return label

    def update_labels(self, item, issue):
        status = issue.fields.status.name
        label = self.get_or_create_label(status,
                                         label_colors.get(status, colors.GRAY))['id']
        item.update(labels=[label])

    def update_urgency(self, item, issue):
        item.update(priority=priority_mapping[issue.fields.priority.id])

    def update_comments(self, item, issue):
        notes = [note['content'] for note in self.td_api.notes.all()
                 if note['item_id'] == item['id']]

        for comment in self.jira.comments(issue):
            text = self.text_from_jira_comment(comment)
            if text not in notes:
                note = self.td_api.notes.add(item['id'], text)
                print u"Added note to ticket {}: {}".format(issue.key, text)

    def text_from_jira_comment(self, comment):
        return comment.raw['author']['displayName'] + ": " + comment.body

    def clear_temp(self):
        if os.path.exists(os.path.expanduser('~/.todoist-sync')):
            shutil.rmtree(os.path.expanduser('~/.todoist-sync'))

    def sync(self):
        for jql, target_project in JQL_PROJECT_MAPPING.iteritems():
            print "Synching {} <-- {}".format(target_project, jql)
            try:
                proj_id = next(proj.data['id']
                               for proj in self.td_api.projects.all()
                               if proj.data['name'] == target_project)
            except StopIteration:
                print "Cannot find target project {} in todoist".format(target_project)
                continue

            try:
                issues = search_all_issues(self.jira, jql)
            except JIRAError:
                print "Cannot evaluate JQL expression {}".format(jql)
                continue

            items = [item for item in self.td_api.items.all()
                     if item.data['project_id'] == proj_id]
            keys = [item.data['content'].split(' ')[0] for item in items]
            jira_keys = [issue.key for issue in issues]

            for issue in issues:
                if issue.key not in keys:
                    item = self.td_api.items.add(u'{} {} {}/browse/{}'.format(issue.key,
                                                                              issue.fields.summary,
                                                                              JIRA_SERVER,
                                                                              issue.key),
                                                 project_id=proj_id)
                    print u"Adding task {} {}".format(issue.key, issue.fields.summary)
                    items.append(item)
                    keys.append(issue.key)

                item = items[keys.index(issue.key)]
                self.update_labels(item, issue)
                self.update_urgency(item, issue)
                self.update_comments(item, issue)

            for item in items:
                if item.data['content'].split(' ')[0] not in jira_keys:
                    item.delete()
                    print u"Deleting task {}".format(item.data['content'])
            self.safe_sync()

    def safe_sync(self):
        try:
            self.td_api.commit()
            print "Committed.."
            self.td_api.sync()
            print "...aaand synched!"
        except (todoist.api.SyncError, requests.exceptions.ConnectionError) as e:
            print "Couldn't sync, restarting connection to todoist..."
            print e
            self._setup_todoist()


if __name__ == '__main__':
    while True:
        print datetime.datetime.now().strftime("%d.%m. %H:%M") + " Starting sync"
        td = JiradoistSyncher()
        td.sync()
        print datetime.datetime.now().strftime("%d.%m. %H:%M") + " Sync done, sleeping 5min"
        time.sleep(SYNC_EVERY)
