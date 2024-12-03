#!/usr/bin/env python3

import sys, json, pathlib, hashlib
tag = sys.argv[1]

with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if 'Xtensa' in i['full_arch']:
            with open("../git/linux-firmware/" + i['file_name'], 'rb') as shaf:
                try:
                    pathlib.Path.unlink("../data/txt/disassembly/linux-firmware-db-" + hashlib.sha256(shaf.read()).hexdigest() + '-disassembly.txt')
                except:
                    print("file not found")
            
    