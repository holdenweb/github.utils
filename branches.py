import itertools
import os
import urllib

from collections import namedtuple

from github import Github
import jinja2

pr_rname = namedtuple("pr_rname", ['pr', 'repo'])
tbl_row = namedtuple("tbl_row",
                     ['creator', 'repo_name', 'number', 'title', 'creation_time',
                      'assignee', 'labels', 'mergeable_state', 'html_url'])
template = jinja2.Template(open("page.html").read())

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = Github(GITHUB_TOKEN)

org = gh.get_organization(ORG_NAME)

for repo in org.get_repos("private"):
    brs = [br for br in repo.get_branches() if not br.name.startswith("release")]
    if len(brs) > 3:
        print("{}: {} branches".format(repo.name, len(brs)))
#        for br in brs:
#            print("    ", br.name)