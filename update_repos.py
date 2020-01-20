import os
import urllib
import sys

import github3

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = github3.login(token=GITHUB_TOKEN)

org = gh.organization(ORG_NAME)

if len(sys.argv) > 1:
    repolist = [gh.repository(ORG_NAME, name) for name in sys.argv[1:]]
else:
    repolist = org.repositories(type="all")

for repo in repolist:
    print("==== {}: {}".format(repo.name, repo.ssh_url))
    if os.path.exists(repo.name):
        os.system("cd {}; git fetch --all".format(repo.name))
    else:
        os.system('git clone {}'.format(repo.ssh_url))
