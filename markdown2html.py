#!/usr/bin/python3 

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    if not os.path.isfile("README.md"):
        sys.stderr.write("Missing README.md\n")
        sys.exit(1)

    sys.exit(0)


