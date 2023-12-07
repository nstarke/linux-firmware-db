#!/bin/sh

if [ -z "$LATEST_TAG" ]; then
    LATEST_TAG="$1"
fi

if ! [ -f "../data/csv/linux-firmware-db-$LATEST_TAG-cpu_rec.csv" ]; then
    touch "../data/csv/linux-firmware-db-$LATEST_TAG-cpu_rec.csv"
fi

echo "tag,filename,full,chunk,full_length,chunk_length,chunk_count,file_type,sha256,shannon_entropy"  >> "../data/csv/linux-firmware-db-$LATEST_TAG-cpu_rec.csv"
while read LINE;
do
    PARTS=$( for PART in "$LINE"; do echo $PART; done )
    FILE_NAME=$(echo $PARTS | awk -F' ' '{print $1}')
    FULL_LENGTH=$(echo $PARTS | awk -F' ' '{print $2}' | sed -r 's/full\(|\)//g')
    FULL_LENGTH=$(python3 check-int.py "$FULL_LENGTH")
    CHUNK_FULL=$(echo $PARTS | awk -F' ' '{print $4}' | sed -r 's/chunk\(|\)//g')
    CHUNK_LENGTH=$(echo $CHUNK_FULL | cut -d ';' -f 1 )
    CHUNK_LENGTH=$(python3 check-int.py "$CHUNK_LENGTH")
    CHUNK_COUNT_TMP=$(echo $CHUNK_FULL | cut -d ';' -f 2 )
    CHUNK_COUNT=$(python3 check-int.py "$CHUNK_COUNT_TMP")
    FULL_ARCH=$(echo -n $PARTS | awk -F' ' '{print $3}')
    CHUNK_ARCH=$(echo -n $PARTS | awk -F' ' '{print $5}')
    FILE_TYPE=$(file -b ../git/linux-firmware/$FILE_NAME | tr -d '"' | tr -d '\\')
    SHA256=$(sha256sum ../git/linux-firmware/$FILE_NAME | awk -F' ' '{print $1}')
    ENT=$(ent ../git/linux-firmware/$FILE_NAME | head -n 1 | awk -F' ' '{print $3}')
    echo "\"$LATEST_TAG\",\"$FILE_NAME\",\"$FULL_ARCH\",\"$CHUNK_ARCH\",\"$FULL_LENGTH\",\"$CHUNK_LENGTH\",\"$CHUNK_COUNT\",\"$FILE_TYPE\",\"$SHA256\",\"$ENT\"" >> "../data/csv/linux-firmware-db-$LATEST_TAG-cpu_rec.csv"
    
done < "../data/txt/linux-firmware-db-$LATEST_TAG-cpu_rec.txt"