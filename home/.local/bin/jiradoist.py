#!/usr/bin/python
# A little script to upload my JIRA tickets to todoist

import os
import time
import shutil

from jira import JIRA, JIRAError
from todoist.api import TodoistAPI

from pprint import PrettyPrinter
dt = PrettyPrinter(indent=4)


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


# Mapping from JIRA priority (1-5) to todoist priority (1-4)
priority_mapping = {unicode(i): min(i,4) for i in range(5)}

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

# Map all tickets from the given JQL to the given Todoist project
jql_project_mapping = {'assignee = harst AND filter not in ("Finished Tickets")': 'Magazino JIRA'}

# Where to read the configs from
password_base = os.path.join(os.getenv('HOME') + '/.password-store/')

JIRA_SERVER = "http://magazino.atlassian.net"


class JiradoistSyncher(object):
    def __init__(self):
        self.clear_temp()

        # Set up JIRA
        with open(password_base + 'jira_', 'r') as config:
            self.jira = JIRA(JIRA_SERVER, basic_auth=config.read().strip().split(','))


        # Set up Todoist
        with open(password_base + 'todoist_', 'r') as config:
            self.td_api = TodoistAPI(config.read().strip())
        self.td_api.sync()

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
                self.td_api.commit()
                print u"Added note to ticket {}: {}".format(issue.key, text)

    def text_from_jira_comment(self, comment):
        return comment.raw['author']['displayName'] + ": " + comment.body


    def clear_temp(self):
        if os.path.exists(os.path.expanduser('~/.todoist-sync')):
            shutil.rmtree(os.path.expanduser('~/.todoist-sync'))

    def sync(self):
        for jql, target_project in jql_project_mapping.iteritems():
            try:
                proj_id = next(proj.data['id']
                               for proj in self.td_api.projects.all()
                               if proj.data['name'] == target_project)
            except StopIteration:
                print "Cannot find target project {} in todoist".format(target_project)
                continue

            try:
                issues = self.jira.search_issues(jql)
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
                                                 proj_id)
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

        self.td_api.commit()
        print "Committed"
        self.td_api.sync()
        print "Synched"

if __name__ == '__main__':
    while True:
	td = JiradoistSyncher()
	td.sync()
	time.sleep(300)
