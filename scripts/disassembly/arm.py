#!/usr/bin/env python3

import sys, json, subprocess, os
tag = sys.argv[1]

with open("../data/json/linux-firmware-db-" + tag + "-cpu_rec.json", 'r') as f:
    j = json.loads(f.read())
    for i in j:
        if 'arm' in i['full_arch'].lower():
            e = i['full_arch'][-2:]
            endian = "-EB"
            if e == 'EL':
                endian = "-EL"
            elif e =='hf':
                endian = "-EL"
            if not os.path.isfile("../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt'):
                cmd_out = subprocess.check_output(['arm-none-eabi-objdump', "-m", "arm", "-b", "binary", "-D", endian, "../git/linux-firmware/" + i['file_name']]).decode('utf-8').strip()
                with open("../data/txt/disassembly/linux-firmware-db-" + i['sha256'] + '-disassembly.txt', 'w') as f:
                    f.write(cmd_out)