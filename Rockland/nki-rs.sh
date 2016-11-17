#!/bin/bash

#releases=(/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r1 /home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r2 /home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r3 /home/data/Incoming/rockland_sample/DiscSci_R4/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R5/anonymized_imaging_data/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R6/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R7/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R8/organized_symlinks)
releases=(/home/data/Incoming/rockland_sample/DiscSci_R4/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R5/anonymized_imaging_data/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R6/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R7/organized_symlinks /home/data/Incoming/rockland_sample/DiscSci_R8/organized_symlinks)

for release in ${releases[@]}
do
    python pathmatcher.py -ri "(A\d{8})/(.+)/mprage_siemens_defaced/mprage_siemens_defaced\.nii\.gz" -ro "sub-\1/ses-\2/anat/sub-\1_ses-\2_T1w.nii.gz" -i ${release} -o /data2/bids_warehouse/NITRC -c -y
    python pathmatcher.py -ri "(A\d{8})/(.+)/(rest.+)/.+\.gz" -ro "sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz" -i ${release} -o /data2/bids_warehouse/NITRC -c -y
    python pathmatcher.py -ri "(A\d{8})/(.+)/(breath.+)/.+\.gz" -ro "sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz" -i ${release} -o /data2/bids_warehouse/NITRC -c -y
    python pathmatcher.py -ri "(A\d{8})/(.+)/(check.+)/.+\.gz" -ro "sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz" -i ${release} -o /data2/bids_warehouse/NITRC -c -y
    python pathmatcher.py -ri "(A\d{8})/(.+)/dti_137_ap/dti_137_ap\.(.+)" -ro "sub-\1/ses-\2/dwi/sub-\1_ses-\2_dwi.\3" -i ${release} -o /data2/bids_warehouse/NITRC -c -y
done
