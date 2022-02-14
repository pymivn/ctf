#!/usr/bin/env python3

import sys
import os
try:
    dirname = sys.argv[1]
except IndexError:
    exit(f"Usage {sys.argv[0]} directory")

for fn in os.listdir(sys.argv[1]):
    if fn != "README.md" and fn.endswith(".md"):
        with open(os.path.join(sys.argv[1], fn)) as f:
            title = f.readline().strip().strip("#").strip()

            for line in f:
                if line.startswith("tags:"):
                    tags = line.strip().split("tags:")[1].split(",")

        tags = ", ".join([f"#{t.strip()}" for t in tags])
        print(f"- [{title}]({fn}) {tags}")
