#!/bin/bash

START=$HOME/firmware/linux/linux-firmware-db/scripts

cd $START

source ../.venv/bin/activate

if [ -f /tmp/.lfwdb-running ]; then
    echo "Manual Job Running, exiting"
    exit 0
fi

cd ../git
if [ -d linux-firmware ]; then
    echo "Linux-firmware found, pulling"
    cd linux-firmware
    git checkout main
    git pull origin main
else
    echo "No Linux Firmware, Cloning now"
    git clone "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git"
fi

export LATEST_TAG=$(git tag | tail -n 1)

git checkout "$LATEST_TAG"

CURRENT_TAG=$(cat ../../data/.current_tag)
if [[ "$CURRENT_TAG" == "$LATEST_TAG" ]]; then
    echo "No New Tag, exiting"
    exit 0
else 
    echo $LATEST_TAG > ../../data/.current_tag
    echo $LATEST_TAG >> ../../data/txt/tags.txt
fi


cd $START
sh ./get-cpu_rec.sh
cd $START
sh ./run-cpu_rec.sh
cd $START
sh ./process-txt-results.sh
cd $START
sh ./process-csv-results.sh
cd $START
sh ./process-txt-tags.sh
cd $START
sh ./push-results.sh
cd $START
sh ./disassemble-for-tag.sh $LATEST_TAG
