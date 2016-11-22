from CPAC.AWS import aws_utils, fetch_creds
import os
import re

bucket = fetch_creds.return_bucket('/home/jpellman/jpellman-fcp-indi-keys_oldfmt.csv', 'fcp-indi')

srclist=[]
for i,k in enumerate(bucket.list(prefix='data/Projects/ADHD200/RawData')):
    srclist.append(k.name)
    print k.name

srclist=sorted(srclist)
#niis = [os.path.basename(src) for src in srclist if '.nii.gz' in src]
#print set(niis)

matchdct={  
    "anat" : [r"(.+)/([0-9]+)/session_([0-9]+)/anat_([0-9]{1,2})/mprage.nii.gz" , r"\1/sub-\2/ses-\3/anat/sub-\2_ses-\3_run-\4_T1w.nii.gz"] , \
    "func" : [r"(.+)/([0-9]+)/session_([0-9]+)/rest_([0-9]{1,2})/rest.nii.gz" , r"\1/sub-\2/ses-\3/func/sub-\2_ses-\3_task-rest_run-\4_bold.nii.gz"] \
}

srclist_filt=[]
destlist=[]

for sl in sorted(srclist):
    if re.match(matchdct['anat'][0],sl):
        subbed = re.sub(matchdct['anat'][0],matchdct['anat'][1],sl)
    elif re.match(matchdct['func'][0],sl):
        subbed = re.sub(matchdct['func'][0],matchdct['func'][1],sl)
    else:
        continue
    subbed = subbed.replace('RawData','RawDataBIDS')
    print sl, subbed
    srclist_filt.append(sl)
    destlist.append(subbed)

aws_utils.s3_rename(bucket,srclist_filt,destlist,keep_old=True,make_public=True)
