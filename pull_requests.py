import itertools
import os
import urllib

from collections import namedtuple

from github import Github
import jinja2

pr_rname = namedtuple("pr_rname", ['pr', 'repo'])
tbl_row = namedtuple("tbl_row", ['creator', 'repo_name', 'number', 'title', 'creation_time', 'assignee', 'labels', 'mergeable_state', 'html_url'])
template = jinja2.Template(open("page.html").read())

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = Github(GITHUB_TOKEN)

org = gh.get_organization(ORG_NAME)

prs = []
for repo in org.get_repos("private"):
    for pr in repo.get_pulls('open'):
        prs.append(pr_rname(pr, repo))


def pr_sort(r):
   return (r.pr.user.name, r.repo.name, r.pr.mergeable_state)

prs.sort(key=pr_sort)

rows = []
for pr, repo in prs:
    issue = repo.get_issue(pr.number)
    labels = [l.name for l in issue.get_labels()]
    rows.append(tbl_row(pr.user.name.split()[0],
                       repo.name,
                       pr.number,
                       pr.title,
                       pr.created_at,
                       pr.assignee.name.split()[0] if pr.assignee else "-",
                       ", ".join(labels),
                       pr.mergeable_state if pr.mergeable_state else "unknown",
                       pr.html_url))

print(template.render(rows=rows, rowcount=len(rows)), file=open("/tmp/test.html", "w"))