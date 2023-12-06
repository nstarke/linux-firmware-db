#!/usr/bin/env python3

import sys

i = sys.argv[1]
try:
    i = int(i, 16)
    if isinstance(i, int):
        print(int(i))
    else:
        print("0")
except:
    print("0")