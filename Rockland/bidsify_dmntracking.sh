#!/bin/bash

datadir=$1
outdir=$2

for f in "${datadir}"/*.txt
do
    ursi=$(echo ${f} | egrep -o NFB_[0-9]{5})
    ursi=${ursi/NFB_/M109}
    if [ ! -z ${ursi} ]
    then
        mkdir -p ${outdir}/sub-${ursi}/ses-NFB3/func
        cp "${f}" ${outdir}/sub-${ursi}/ses-NFB3/func/sub-${ursi}_ses-NFB3_task-DMNTRACKINGTEST_bold.txt
    fi
done
