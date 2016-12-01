#!/usr/bin/env python3
import os

from io import StringIO
from subprocess import Popen, PIPE

import requirements

out = StringIO()
with Popen(["find", ".", "-name", "requirements*.txt"], stdout=PIPE) as proc:
    for line in proc.stdout.readlines():
        filename = line[:-1].decode("UTF-8")
        with open(filename) as f:
            for line in f:
                line = line.strip()
                p = line.find("#")
                if p >= 0:
                    line = line[:p].strip()
                if len(line) > 1:
                    print(line, filename, file=out)
out.seek(0)
for l in sorted((line[:-1] for line in out.readlines()), key=lambda s: s.lower()):
    rqt, filename = l.split(None, 1)
    req = next(requirements.parse(rqt))
    print(req.name, req.specs, req.extras, filename)
