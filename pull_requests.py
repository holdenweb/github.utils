import itertools
import os
import urllib

import github3

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = github3.login(token=GITHUB_TOKEN)

org = gh.organization(ORG_NAME)

prs = []
for repo in org.repositories(type="all"):
    for pr in repo.pull_requests(state='open'):
        prs.append((pr, repo.name))
    break

def pr_sort(r):
   return (r[0].user.login, r[1], r[0].mergeable_state)

prs.sort(key=pr_sort)

print("=======", len(prs), "issues =======")
for (user_login, repo, ms), pr_list in itertools.groupby(prs,key=pr_sort):
    print("Pull requests for user", user_login)
    for pr, repo_name in prs:
        print("==== {} Repo {} =====".format(pr.user.login, repo_name))
        print(pr.title, "created on", pr.created_at)
        print(pr.assignee)
        print("Mergeable state:", pr.mergeable_state if pr.mergeable_state else "unknown")
        print(getattr(pr.assignee, 'name', '-'))
        print(pr.url)
