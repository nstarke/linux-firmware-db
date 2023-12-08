#!/bin/sh

cd ../git/linux-firmware
for FORK in $(cat ../../data/txt/forks.txt); do
    FORK_HASH=$(echo $FORK | sha256sum | awk -F' ' '{print $1}')
    echo "$FORK_HASH - $FORK"
    git remote add $FORK_HASH "$FORK"
done

git fetch --all