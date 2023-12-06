#!/usr/bin/env python3

import sys, json, subprocess, os
tag = sys.argv[1]

with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if 'Xtensa' in i['full_arch']:
            e = i['full_arch'][-2:]
            endian = "-EL"
            if e == 'EB':
                endian = "-EB"
            cmd_out = subprocess.check_output(['xtensa-lx106-elf-objdump', "-m", "xtensa", "-b", "binary", "-D", endian, "../git/linux-firmware/" + i['file_name']]).decode('utf-8').strip()
            if not os.path.isfile("../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt'):
                with open("../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt', 'w') as f:
                    f.write(cmd_out)
    