#!/bin/sh

if [ -z "$LATEST_TAG" ]; then
    LATEST_TAG="$1"
fi

cat "../data/csv/linux-firmware-db-$LATEST_TAG-cpu_rec.csv" \
 | sort \
 | python3 process-csv.py \
 > "../data/json/linux-firmware-db-$LATEST_TAG-cpu_rec.json"