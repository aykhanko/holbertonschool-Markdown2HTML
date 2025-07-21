#!/usr/bin/python3 

import sys 

arg1 = "README.md"
arg2 = "README.html"
count = len(sys.argv)

def missing_arg(arg):
    if arg not in sys.argv:
        print(f"Missing {arg}")
        sys.exit(1)

if __name__ == "__main__":
    missing_arg(arg1)
    missing_arg(arg2)
    sys.exit(0)