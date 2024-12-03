#!/usr/bin/env python3

import sys, json, os, r2pipe
tag = sys.argv[1]

with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if '8051' in i['full_arch'] or '8051' in i['chunk_arch']:
            if not os.path.isfile("../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt'):
                try:
                    R2 = r2pipe.open("../git/linux-firmware/" + i['file_name'])
                    R2.cmd("e asm.arch = 8051")
                    R2.cmd("aaaa")
                    R2.cmd('pdr @@f > ' + "../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt')
                except:
                    pass