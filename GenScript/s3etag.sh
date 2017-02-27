#!/bin/bash

# From https://gist.github.com/emersonf/7413337 
# 12/01/17 Minor edits for ubuntu compatilibility by DaveOC90

if [ $# -ne 2 ]; then
    echo "Usage: $0 file partSizeInMb";
    exit 0;
fi

file=$1

if [ ! -f $file ]; then
    echo "Error: $file not found." 
    exit 1;
fi

partSizeInMb=$2

fileSizeInMb=$(du -m $file | cut -f 1)

parts=$(($fileSizeInMb / $partSizeInMb))

if [[ $(($fileSizeInMb % $partSizeInMb)) -gt 0 ]]; then
    parts=$(($parts + 1));
fi

checksumFile=$(mktemp -t s3md5.XXX)

for part in $(seq 0 $(($parts-1)));do

    skip=$(($partSizeInMb * $part))

    $(dd bs=1M count=$partSizeInMb skip=$skip if=$file 2>/dev/null | md5sum | awk '{print $1}' >>$checksumFile)

done


echo $(xxd -r -p $checksumFile | md5sum  | awk '{print $1}')-$parts
rm $checksumFile
