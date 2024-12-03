#!/bin/sh
while read url ; do
    ret=$(curl -I -s "$url" -o /dev/null -w "%{http_code}\n")
    ((ret!=200)) && echo "$url" 
done < ../data/txt/forks.txt