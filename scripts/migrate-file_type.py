#!/usr/bin/env python3
import json, subprocess

results = []
with open('../data/json/linux-firmware-db-20231111-cpu_rec.json') as f:
    j = json.loads(f.read())
    for res in j:
        cmd = '../git/linux-firmware/' + res['file_name']
        res['file_type'] = subprocess.check_output(['file', '-b', cmd]).decode('utf-8').strip()
        results.append(res)
    print(json.dumps(results))