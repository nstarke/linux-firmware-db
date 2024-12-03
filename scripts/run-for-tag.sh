#!/bin/bash

START=$HOME/firmware/linux/linux-firmware-db/scripts

cd $START

source ../.venv/bin/activate

touch /tmp/.lfwdb-running
export LATEST_TAG="$1"
echo "$LATEST_TAG" >> ../data/txt/tags.txt
cd ../git/linux-firmware
git checkout "$LATEST_TAG"

cd $START
sh ./run-cpu_rec.sh
cd $START
sh ./process-txt-results.sh
cd $START
sh ./process-csv-results.sh
cd $START
sh ./process-txt-tags.sh
cd $START
sh ./disassemble-for-tag.sh $LATEST_TAG
cd $START
rm /tmp/.lfwdb-running