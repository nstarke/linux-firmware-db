#!/usr/bin/env python3

import sys, json, pathlib, hashlib
tag = sys.argv[1]
results = []

def find_all(i, sub):
    start = 0
    cnt = 0
    while True:
        start = i.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) 
        cnt = cnt + 1

with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if float(i['shannon_entropy'] >= 7.0):
            continue
        if "text" in i['file_type'].lower():
            continue
        if "source" in i['file_type'].lower():
            continue
        if "None" in i['chunk_arch']:
            continue
        if (i['full_arch'] != "None") and (i['full_arch'] != i['chunk_arch']):
            continue

        results.append(i)
    
    print(json.dumps(results))