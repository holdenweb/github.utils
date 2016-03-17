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
from itertools import zip_longest

repo_names = [line.strip() for line in open("repos.txt") if line!='\n']

class Module:
    dep_dict = {}
    def __init__(self, name):
        self.name = name
        self._deps = set()       # Direct dependencies
        self._trans_deps = set() # Their dependencies, and theirs ...
        self.trans_done = False
        Module.dep_dict[name] = self
    def add_dep(self, dep):
        self._deps.add(dep)
    @property
    def trans_deps(self):
        if not self.trans_done:
            print("+++ Computing transitive dependencies for", self.name)
            for dep in self._deps:
                if dep in Module.dep_dict:
                    module = Module.dep_dict[dep]
                    print("Adding dependencies from", module.name, "to", self.name, ":\n", ", ".join(sorted(module.trans_deps)))
                    self._trans_deps |= module._deps
            self.trans_done = True
            print(self.name, "transitive dependencies done")
        return self._trans_deps
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
    for repo_name in repo_names:
        print("+++ Recording dependencies for repo", repo_name)
        dep_files = glob(os.path.join("repos", repo_name, "requirements*.txt"))
        repo_dep = Module.dep_dict[repo_name] = Module(repo_name)
        for dep_file in dep_files:
            print("--- Processing", dep_file)
            for line in lines_of(open(dep_file)):
                if line.startswith("-e ."):
                    continue
                if line.startswith("-e git+git@github.com:bmlltech"):
                    #print("Extras on", line)
                    _, line = line.split("=")
                print("   Adding direct dependency", line)
                repo_dep.add_dep(line)
    return Module.dep_dict

if __name__ == "__main__":
    get_deps()
    for name, module in Module.dep_dict.items():
        print("### Computing transitive dependencies for", name)
        deps = module.trans_deps

    #for repo in sorted(dep_dict):
        #print("===", repo, "===")
        #for dep in sorted(dep_dict[repo].deps):
            #print('\t', dep)
    
    fline = "{:28s} {:28s} {:28s}".format
    for repo in sorted(Module.dep_dict):
        print("\n\n===", repo, "===")
        print(fline("", "Provided as", ""))
        print(fline("Module dependecies", "transitive dependencies", "Leaving"))
        print(fline(*("-"*25, )*3))
        module = Module.dep_dict[repo]
        excludables = module._deps & module.trans_deps
        for mdep, tdep, xdep in zip_longest(sorted(module._deps),
                                            sorted(excludables),
                                            sorted(module._deps - excludables),
                                            fillvalue=""):
            print(fline(mdep, tdep, xdep))
    
    all_modules = set()
    for name, module in Module.dep_dict.items():
        all_modules = all_modules.union(module.trans_deps)
        for dep in module._deps:
            if dep not in Module.dep_dict:
                all_modules.add(dep)

    print("\n\n\n----- All external dependencies -----\n\n")
    for name in sorted(all_modules):
        print(name)
    print("\n\n\nFinished")