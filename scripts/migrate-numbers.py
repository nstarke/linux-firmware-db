#!/usr/bin/env python3
import json, subprocess

results = []
with open('../data/json/linux-firmware-db-20231111-cpu_rec.json') as f:
    j = json.loads(f.read())
    for res in j:
        try:
            res['full_length'] = int(res['full_length'])
            res['chunk_length'] = int(res['chunk_length'])
            res['chunk_count'] = int(res['chunk_count'])
        except:
            pass
        results.append(res)
    print(json.dumps(results))