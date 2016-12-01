"""
List all repositories specifying each requirement
"""
import os
import subprocess
import sys

from collections import defaultdict

import github3

# Best practise dictates that authentication data
# is always obtained from the environment
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = os.environ['GITHUB_ORGANISATION']

# Authenticate with Github and create a connection
# to the data for our Github organisation
gh = github3.login(token=GITHUB_TOKEN)
org = gh.organization(ORG_NAME)

# There may be a more comprehensible way to do this
# `data` becomes the result of the shell command
# XXX Platform dependency!!!!
data = subprocess.getoutput("find repos -name requirements\*.txt"
                            ).splitlines()

# Establish a list of the requirement specifications
# for each package.
reqdict = defaultdict(list)
for filename in data:
    with open(filename.strip()) as inf:
        for reqt in inf:
            reqt = reqt.strip()
            if not reqt or reqt.startswith("#"):
                continue
            repo = os.path.dirname(filename) # ???
            reqdict[reqt.lower()].append(filename)

print(len(reqdict), "requirements in all\n")

# Hack to let me take a look at current outputs
for k in sorted(reqdict.keys(), key=lambda k: k.lower()):
    print("{}".format(k), *("  {}".format(v[6:])
                            for v in sorted(reqdict[k],
                                            key=lambda k: k.lower())),
          sep="\n", end="\n\n")


