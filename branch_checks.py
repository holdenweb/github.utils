import os
import urllib

import github3

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = github3.login(token=GITHUB_TOKEN)

org = gh.organization(ORG_NAME)

for repo in org.repositories(type="all"):
    print("==== {}: {} ====".format(repo.name, repo.ssh_url))
    brs = list(b.name for b in repo.branches())
    for br_name in "dev", "master":
        if br_name not in brs:
            print("@@@ MISSING {} BRANCH".format(br_name))
    print("{} Branch(es): {}".format(len(brs), ", ".join(brs)))
