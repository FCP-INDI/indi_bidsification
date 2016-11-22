from CPAC.AWS import aws_utils, fetch_creds
import tarfile
import os
import shutil
import re
import sys

keyspath=sys.argv[1]

bucket = fetch_creds.return_bucket(keyspath, 'fcp-indi')


srclist=[]
for i,k in enumerate(bucket.list(prefix='data/Projects/CORR/RawData')):
    srclist.append(k.name)
    print k.name

srclist=sorted(srclist)

matchdct={
'anat' : 
["(.+)/([0-9]+)/session_([0-9]{1,2})/anat_([0-9]{1,2})/anat.nii.gz" ,
r"\1/sub-\2/ses-\3/anat/sub-\2_ses-\3_run-\4_T1w.nii.gz"],

'mpi_anat_comp': 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/anat_([0-9]{1,2})/anat_([a-z12\_]+).nii.gz" , 
r"\1/sub-\2/ses-\3/anat/sub-\2_ses-\3_acq-\5_run-\4_T1w.nii.gz"],

'dti' : 
 [r"(.+)/([0-9]+)/session_([0-9]{1,2})/dti_([0-9]{1,2})/dti.nii.gz" , 
r"\1/sub-\2/ses-\3/dwi/sub-\2_ses-\3_run-\4_dwi.nii.gz"],

'func_rest' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/rest_([0-9]{1,2})/rest.nii.gz" , 
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-\4_func.nii.gz"], 

'func_rest_mb' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/rest_([0-9]{3,4})_([0-9]{1,2})/rest.nii.gz" ,
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_acq-tr\4ms_run-\5_func.nii.gz"],

'func_rest_pref' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/rest_([0-9]{1,2})_([a-z]+)/rest.nii.gz" , 
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_acq-fov\5_run-\4_func.nii.gz"],

'func_msit' : 
["(.+)/([0-9]+)/session_([0-9]{1,2})/msit_([0-9]{1,2})/msit.nii.gz" , 
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-msit_run-\4_func.nii.gz"],

'func_eyetracker' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/eyemovement_([0-9]{3,4})_([0-9]{1,2})/eyemovement.+.nii.gz" , 
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-eyemovement_acq-tr\4ms_run-\5_func.nii.gz"],

'func_breathhold' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/breathhold_([0-9]{3,4})_([0-9]{1,2})/breathhold.+.nii.gz" , 
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-breathhold_acq-tr\4ms_run-\5_func.nii.gz"],

'func_checker' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/checkerboard_([0-9]{3,4})_([0-9]{1,2})/checkerboard.+.nii.gz" , 
r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-checkerboard_acq-tr\4ms_run-\5_func.nii.gz"],

'dti' : 
[r"(.+)/([0-9]+)/session_([0-9]{1,2})/dti_([0-9]{1,2})/dti(.+)" , 
r"\1/sub-\2/ses-\3/dwi/sub-\2_ses-\3_run-\4_dwi\5"]

}


for mk in matchdct.keys():
    print mk

    srclist_filt=[]
    destlist=[]

    for sl in sorted(srclist):
        if re.match(matchdct['dti'][0],sl):
            print sl,re.sub(matchdct['dti'][0],matchdct['dti'][1],sl)
            srclist_filt.append(sl)
            destlist.append(re.sub(matchdct['dti'][0],matchdct['dti'][1],sl))


    # Note might error with make_public=True, removing it stops error, unsure why error occurs
    aws_utils.s3_rename(bucket,srclist_filt,destlist,keep_old=True,make_public=True)


r"""
# All Anats
# MPG MP2RAGE T1 Weighted Component Images
# Fix new name of inversion phase components to remove underscore
#for i in $(find Organized_Data_BIDs/mpg_1/ -iname '*inv*phs*T1w*');do mv -nv $i ${i/_phs/phs};done

# Funcs not containing reference to TR (NKI) or Shortened Number of Slices (MPG)

# Pulls in NKI rest Data with reference to TR

# Pulls in MPG data with reference to Prefrontal acquisition

# Breath Hold Checkerboard eyemovement MSIT

# DTI
"(.+)/([0-9]+)/session_([0-9]{1,2})/dti_([0-9]{1,2})/dti.nii.gz" , "\1/sub-\2/ses-\3/dwi/sub-\2_ses-\3_run-\4_dwi.nii.gz"
"(.+)/([0-9]+)/session_([0-9]{1,2})/dti_([0-9]{1,2})/dti.bval" , "\1/sub-\2/ses-\3/dwi/sub-\2_ses-\3_run-\4_dwi.bval"
"(.+)/([0-9]+)/session_([0-9]{1,2})/dti_([0-9]{1,2})/dti.bvec" , "\1/sub-\2/ses-\3/dwi/sub-\2_ses-\3_run-\4_dwi.bvec"

# Fieldmaps
"(.+)/([0-9]+)/session_([0-9]{1,2})/fieldmap_([0-9]{1,2})/fieldmap_magnitude.nii.gz" , "\1/sub-\2/ses-\3/fmap/sub-\2_ses-\3_run-\4_magnitude.nii.gz"
"(.+)/([0-9]+)/session_([0-9]{1,2})/fieldmap_([0-9]{1,2})/fieldmap_phase.nii.gz" , "\1/sub-\2/ses-\3/fmap/sub-\2_ses-\3_run-\4_phasediff.nii.gz"
"(.+)/([0-9]+)/session_([0-9]{1,2})/FieldMap/magnitude([12]).nii.gz" , "\1/sub-\2/ses-\3/fmap/sub-\2_ses-\3_magnitude\4.nii.gz"
"(.+)/([0-9]+)/session_([0-9]{1,2})/FieldMap/phase.nii.gz" , "\1/sub-\2/ses-\3/fmap/sub-\2_ses-\3_phasediff.nii.gz"

# CBF
"(.+)/([0-9]+)/session_([0-9]{1,2})/cbf_([0-9]{1,2})/cbf.nii.gz" , "\1/sub-\2/ses-\3/cbf/sub-\2_ses-\3_task-rest_run-\4_cbf.nii.gz"

# ASL
"(.+)/([0-9]+)/session_([0-9]{1,2})/asl_([0-9]{1,2})/asl.nii.gz" , "\1/sub-\2/ses-\3/asl/sub-\2_ses-\3_run-\4_asl.nii.gz"

# Physio
# UTAH
# .mat Physio Files with run number in original filename
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/Physio_scan_([0-9]{1,2}).mat" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-\4_recording-physio.mat"
# EPI log .resp/.puls Files with run number in original filename
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/EPIlog_scan_([0-9]{1,2}).([a-z]{4})" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-\4_recording-\5.\5"
# resp/puls text Files with run number in original filename
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/([a-z]{4})_scan_([0-9]{1,2}).txt" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-\5_recording-\4.txt"
# EPI/PMU log .resp/.puls Files with run number in original filename
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/.+_rest([0-9]{1}).([a-z]{4})" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-\4_recording-\5.\5"
# no phys available text files
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/no_physio_available.txt" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_no_physio_available.txt"
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/NoPhysio_Scan2" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_no_physio_available.txt"

# EPI/PMU log .resp/.puls Files WITHOUT run number in original filename
"(.+)/([0-9]+)/session_([0-9]{1,2})/[Pp]hysio/.+_rest.([a-z]{4})" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-1_recording-\4.\4"

# IBA MSIT Behavioural
"(.+)/([0-9]+)/session_([0-9]{1,2})/msit_([1-9]{1})/behavior.txt" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-msit_run-\4_behavior.txt"
"(.+)/([0-9]+)/session_([0-9]{1,2})/msit_([1-9]{1})/logfile.txt" , "\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-msit_run-\4_logfile.txt"

"""
