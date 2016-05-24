"""
List all repositories specifying each requirement
"""
import os
import subprocess
import sys

from collections import defaultdict

import github3

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

gh = github3.login(token=GITHUB_TOKEN)

org = gh.organization(ORG_NAME)

data = subprocess.getoutput("find repos -name requirements\*.txt").splitlines()

reqdict = defaultdict(list)
for filename in data:
    filename = filename.strip()
    inf = open(filename)
    for reqt in inf:
        reqt = reqt.strip()
        if reqt == "" or reqt.startswith("#"):
            continue
        repo = os.path.dirname(filename)
        reqdict[reqt.lower()].append(filename)

print(len(reqdict), "requirements in all\n")
for k in sorted(reqdict.keys(), key=lambda k: k.lower()):
    print("{}".format(k), *("  {}".format(v[6:])
                            for v in sorted(reqdict[k],
                                            key=lambda k: k.lower())),
          sep="\n", end="\n\n")


