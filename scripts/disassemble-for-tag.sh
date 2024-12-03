#!/bin/bash

START=$HOME/firmware/linux/linux-firmware-db/scripts

export LATEST_TAG="$1"

cd ../git/linux-firmware
git checkout $LATEST_TAG

cd $START

python3 ./diassembly/6502.py $LATEST_TAG
python3 ./disassembly/avr.py $LATEST_TAG
python3 ./disassembly/superh.py $LATEST_TAG
python3 ./disassembly/mips.py $LATEST_TAG
python3 ./disassembly/8051.py $LATEST_TAG
python3 ./disassembly/arc.py $LATEST_TAG
python3 ./disassembly/x86.py $LATEST_TAG
python3 ./disassembly/arm.py $LATEST_TAG