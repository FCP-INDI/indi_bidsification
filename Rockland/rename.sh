#!/bin/bash

mkdir renamed
for name in $(find . -type f)
do
    # Change session names
    newname=${name//ses-clg_A/ses-CLGA}
    newname=${newname//ses-clg_2/ses-CLG2}
    newname=${newname//ses-clg_2R/ses-CLG2R}
    newname=${newname//ses-clg_4/ses-CLG4}
    newname=${newname//ses-clg_4R/ses-CLG4R}
    newname=${newname//ses-dsc_A/ses-DSA}
    newname=${newname//ses-dsc_2/ses-DS2}
    newname=${newname//ses-nfb_A/ses-NFBA}
    newname=${newname//ses-nfb_2/ses-NFB2}
    newname=${newname//ses-nfb_2R/ses-NFB2R}
    # Change series newnames
    # Apparently one of the scans has this newname- unclear if 645 or 1400:
    # task-checkerboard_bold
    newname=${newname//task-breath_hold_1400_bold/task-BREATHHOLD_acq-1400_bold}
    newname=${newname//task-breath_hold_bold/task-BREATHHOLD_acq-1400_bold}
    newname=${newname//task-checkerboard_1400_bold/task-CHECKERBOARD_acq-1400_bold}
    newname=${newname//task-checkerboard_645_bold/task-CHECKERBOARD_acq-645_bold}
    newname=${newname//task-DMNTRACKINGTEST_bold}
    newname=${newname//task-DMNTRACKINGTRAIN_bold}
    newname=${newname//task-MORALDILEMMA_bold}
    newname=${newname//task-MSIT_bold}
    newname=${newname//task-PEER1_bold}
    newname=${newname//task-PEER2_bold}
    # The NFB3 scans in the current anonymized folder use 'REST' instead of 'rest'- this will need to be fixed.
    newname=${newname//task-rest_1400_bold/task-rest_acq-1400_bold}
    newname=${newname//task-rest_645_bold/task-rest_acq-645_bold}
    newname=${newname//task-rest_cap_bold/task-rest_acq-CAP_bold}
    newname=${newname//.\//}
    mkdir -p renamed/$(dirname ${newname})
    mv ${name} renamed/${newname}
done
