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
    if os.path.exists(repo.name):
        os.system("cd {}; git checkout master && git pull; git checkout develop && git pull".format(repo.name))
    else:
        os.system('git clone {}'.format(repo.ssh_url))
