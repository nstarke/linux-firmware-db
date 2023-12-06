#!/bin/sh
cd ../git
if [ -d cpu_rec ]; then
    cd cpu_rec
    git reset --hard
    git clean -df
    git pull
else 
    git clone https://github.com/airbus-seclab/cpu_rec
    cd cpu_rec
fi

cd cpu_rec_corpus
unxz *
