import os

from collections import defaultdict
from glob import glob

repos = [line.strip() for line in open("repos.txt") if line!='\n']

class Requirements:
    def __init__(self, name):
        self.name = name
        self.deps = set()
    def add_req(self, req):
        self.deps.add(req)
    def provides(self, req):
        if req in self.deps:
            return True
        for dep in self.deps:
            if dep in dep_dict:
                if dep_dict[dep].provides(req):
                    return True
        return False
    def optimise(self):
        raw_deps = {d for d in self.deps if d not in dep_dict}
        trans_deps = self.deps - raw_deps
        for dep in raw_deps:
            if any(dep_dict[d].provides(dep) for d in trans_deps):
                self.deps = self.deps - {dep}

def lines_of(f):
    for line in f:
        if line == "\n" or line.startswith("#"):
            continue
        yield line.strip()

dep_dict = {}
for repo in repos:
    reqs = glob(os.path.join("repos", repo, "requirements*.txt"))
    dep_dict[repo] = repo_req = Requirements(repo)
    for req in reqs:
        for line in lines_of(open(req)):
            repo_req.add_req(line)

for repo in sorted(dep_dict):
    print("===", repo, "===")
    for dep in sorted(dep_dict[repo].deps):
        print('\t', dep)
print("+++++++++++++++++++++++++++++++++++++++++++")

for repo in dep_dict:
    dep_dict[repo].optimise()

for repo in dep_dict:
    dep_dict[repo].optimise()

for repo in dep_dict:
        dep_dict[repo].optimise()


for repo in sorted(dep_dict):
    print("===", repo, "===")
    for dep in sorted(dep_dict[repo].deps):
        print('\t', dep)



print("Finished")