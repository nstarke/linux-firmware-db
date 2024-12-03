#!/usr/bin/env python3

import json, hashlib, sys

tag = sys.argv[1]
results = []
with open("../data/json/linux-firmware-db-" +tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        try:
            with open("../git/linux-firmware/" + i['file_name'], 'rb') as shaf:
                i['sha256'] = hashlib.sha256(shaf.read()).hexdigest()
                results.append(i)
        except:
            i['sha256'] = ""
            results.append(i)

    print(json.dumps(results))

    