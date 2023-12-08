#!/usr/bin/env python3

import sys, json, os, r2pipe
tag = sys.argv[1]
check_file = True
if len(sys.argv) == 3:
    print("Skipping file check")
    check_file = False

with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if 'mips' in i['full_arch'].lower() or 'mips' in i['chunk_arch'].lower():
            e = i['full_arch'][-2:]
            endian = None
            if e == 'eb' or e == 'EB':
                endian = "true"
            if not os.path.isfile("../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt') or not check_file:
                try:
                    R2 = r2pipe.open("../git/linux-firmware/" + i['file_name'])
                    if endian:
                        R2.cmd("e cfg.bigendian = " + endian)
                    R2.cmd("e asm.arch = mips")
                    R2.cmd("aaaa")
                    R2.cmd('pdr @@f > ' + "../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt')
                except:
                    pass
    