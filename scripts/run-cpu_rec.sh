#!/bin/sh

cd ../git/linux-firmware
find . -type f -not -path "./.git/*" | parallel -j $(nproc --all) python3 ../cpu_rec/cpu_rec.py {} \; > "../../data/txt/linux-firmware-db-$LATEST_TAG-cpu_rec.txt"