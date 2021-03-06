"""
Evaluate project dependencies recursively.

First, enumerate all the direct requirements of each project, so we know which
dependencies it provides.

By accumulating a list of the dependencies *provided* by those dependecies, we
can then eliminate the dependencies that will be transitively provided.

Ultimately the goal is to reduce the requirements files of projects in size.

In order to do this effectively it may be necessary to split dependencies into
groups (some are required only for development, some only for testing, and so on).
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
        #print("Adding direct dependency", dep, "to", self.name)
        self._deps.add(dep)
    def trans_deps(self):
        if not self.trans_done:
            #print("+++ Computing transitive dependencies for", self.name)
            for dep in self._deps:
                if dep in Module.dep_dict:
                    module = Module.dep_dict[dep]
                    #print("Adding dependencies from", module.name, "to", self.name, ":\n", ", ".join(sorted(module.trans_deps)))
                    self._trans_deps |= module._deps | module.trans_deps
            self.trans_done = True
            print(self.name, "transitive dependencies done:", *self.trans_deps())
        return self._trans_deps

def lines_of(f):
    for line in f:
        if line == "\n" or line.startswith("#"):
            continue
        yield line.strip()

def get_deps():
    for repo_name in repo_names:
        #print("+++ Recording dependencies for repo", repo_name)
        dep_files = glob(os.path.join("repos", repo_name, "requirements*.txt"))
        repo_dep = Module.dep_dict[repo_name] = Module(repo_name)
        for dep_file in dep_files:
            #print("--- Processing", dep_file)
            for line in lines_of(open(dep_file)):
                if line.startswith("-e ."):
                    continue
                if line.startswith("-e git+git@github.com:bmlltech"):
                    #print("Extras on", line)
                    _, line = line.split("=")
                repo_dep.add_dep(line)
    return Module.dep_dict

if __name__ == "__main__":
    get_deps()
    for name, module in Module.dep_dict.items():
        deps = module.trans_deps()

    fline = "{:28s} {:28s} {:28s}".format
    for repo in sorted(Module.dep_dict):
        print("\n\n===", repo, "===")
        print(fline("", "Provided as", ""))
        print(fline("Module dependecies", "transitive dependencies", "Leaving"))
        print(fline(*("-"*25, )*3))
        module = Module.dep_dict[repo]
<<<<<<< Updated upstream
        excludables = module._deps & module.trans_deps
        necessaries = module._deps - excludables
        for mdep, tdep, xdep in zip_longest(sorted(m for m in module._deps if m in Module.dep_dict),
                                            sorted(e for e in excludables if e in Module.dep_dict),
                                            sorted(n for n in necessaries if n in Module.dep_dict),
=======
        excludables = module._deps & module.trans_deps()
        for mdep, tdep, xdep in zip_longest(sorted(module._deps),
                                            sorted(excludables),
                                            sorted(module._deps - excludables),
>>>>>>> Stashed changes
                                            fillvalue=""):
            print(fline(mdep, tdep, xdep))
    
    all_modules = set()
    for name, module in Module.dep_dict.items():
        all_modules = all_modules.union(module.trans_deps())
        for dep in module._deps:
            if dep not in Module.dep_dict:
                all_modules.add(dep)

    print("\n\n\n----- All external dependencies -----\n")
    for name in sorted(all_modules):
        if name not in Module.dep_dict:
            print(name)
    print("\n\n\nFinished")
