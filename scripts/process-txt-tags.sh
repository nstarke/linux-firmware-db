#!/bin/sh
cat ../data/txt/tags.txt \
| sort -u \
| python3 -c 'import json, csv, sys; print(json.dumps(sys.stdin.read().split("\n")[:-1]))' \
> ../data/json/tags.json