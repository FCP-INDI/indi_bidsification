#!/bin/bash

python pathmatcher.py -ri "(.+)/(\d{7})/session_(\d)/anat_(\d)/mprage.nii.gz" -ro "\1/sub-\2/anat/sub-\2_T1w.nii.gz" -i data/Projects/ABIDE_Initiative/RawData -o BIDS -c
python pathmatcher.py -ri "(.+)/(\d{7})/session_(\d)/rest_(\d)/rest.nii.gz" -ro "\1/sub-\2/func/sub-\2_task-rest_run-\4_bold.nii.gz" -i data/Projects/ABIDE_Initiative/RawData -o BIDS -c
