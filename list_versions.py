import os
import urllib

import github3

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

os.chdir('repos')
gh = github3.login(token=GITHUB_TOKEN)

org = gh.organization(ORG_NAME)

os.system("find . -name package_meta.py > package_metas")
with open("package_metas") as filenames:
    for i, fn in enumerate(filenames):
        with open(fn.strip()) as lines:
            for line in lines:
                if "BASE" in line:
                    print(fn.strip(), ":", line, end="")
                    break
