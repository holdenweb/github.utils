import itertools
import os
import urllib

from collections import namedtuple

import github3
import jinja2

pr_rname = namedtuple("pr_rname", ['pr', 'repo'])
tbl_row = namedtuple("tbl_row",
                     ['creator', 'repo_name', 'number', 'title', 'creation_time',
                      'assignee', 'labels', 'mergeable_state', 'html_url'])
template = jinja2.Template(open("page.html").read())

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = github3.login(token=GITHUB_TOKEN)

org = gh.organization(ORG_NAME)

for repo in sorted(org.repositories(type="private"), key=lambda x: x.name):
    brs = [br for br in repo.branches() if not br.name.startswith("release")]
    print("{}: {} branches".format(repo.name, len(brs)))
    for br in brs:
       print("    ", br.name)
