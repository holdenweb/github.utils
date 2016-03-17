"""
Evaluate project dependencies recursively.

First, enumerate all the direct depuirements of each project, so we know which
dependencies it provides.

By accumulating a list of the dependencies *provided* by those dependecies, we
can then eliminate the dependencies that will be transitively provided.

Ultimately the goal is to reduce the depuirements files of projects in size.

In order to do this effectively it may be necessary to split dependencies into
groups (some are depuired only for development, some only for testing, and so on).
"""

import os

from glob import glob

repos = [line.strip() for line in open("repos.txt") if line!='\n']

class Module:
    def __init__(self, name):
        self.name = name
        self._deps = set()       # Direct dependencies
        self._trans_deps = set() # Their dependencies, and theirs ...
        self.trans_done = False
    def add_dep(self, dep):
        self._deps.add(dep)
    @property
    def trans_deps(self):
        if not self.trans_done:
            #print("Computing transitive dependencies for", self.name)
            for dep in self._deps:
                if dep in dep_dict:
                    module = dep_dict[dep]
                    self._trans_deps = self._trans_deps.union(module.trans_deps)
            self.trans_done = True
            #print(self.name, "transitive dependencies done")
        return self._trans_deps.union(self._deps)
    def provides(self, dep):
        if dep in self.trans_reps({}):
            return True
        #for dep in self._deps:
            #if dep in dep_dict:
                #if dep_dict[dep].provides(dep):
                    #return True
        #return False

def lines_of(f):
    for line in f:
        if line == "\n" or line.startswith("#"):
            continue
        yield line.strip()

def get_deps():
    dep_dict = {}
    for repo in repos:
        deps = glob(os.path.join("repos", repo, "requirements*.txt"))
        dep_dict[repo] = repo_dep = Module(repo)
        for dep in deps:
            #print("Processing", dep)
            for line in lines_of(open(dep)):
                if line.startswith("-e ."):
                    continue
                if line.startswith("-e git+git@github.com:bmlltech"):
                    #print("Extras on", dep)
                    _, line = line.split("=")
                repo_dep.add_dep(line)
    return dep_dict

if __name__ == "__main__":
    dep_dict = get_deps()
    for name, module in dep_dict.items():
        module.trans_deps

    #for repo in sorted(dep_dict):
        #print("===", repo, "===")
        #for dep in sorted(dep_dict[repo].deps):
            #print('\t', dep)
    
    
    for repo in sorted(dep_dict):
        print("===", repo, "===")
        for dep in sorted(dep_dict[repo]._deps):
            print('\t', dep)
    
    all_modules = set()
    for name, module in dep_dict.items():
        all_modules = all_modules.union(module.trans_deps)

    print("\n\n\n----- All  modules -----\n\n")
    for name in sorted(all_modules):
        print(name)
    print("Finished")