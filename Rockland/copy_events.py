#!/usr/bin/env python
'''
copy_events.py
A script to copy breath hold, peer and checkerboard events tsvs to participants who
are missing them in the Rockland Sample directory on S3.  These TSVs are identical
across participants.
'''
import boto3
import botocore
from indi_aws import fetch_creds
from tqdm import *

dryrun = True

# Prefixes for reference files to copy from.
peerone='data/Projects/RocklandSample/RawDataBIDS/sub-A00064081/ses-NFB3/func/sub-A00064081_ses-NFB3_task-PEER1_events.tsv'
peertwo='data/Projects/RocklandSample/RawDataBIDS/sub-A00064081/ses-NFB3/func/sub-A00064081_ses-NFB3_task-PEER2_events.tsv'
checkerboardone='data/Projects/RocklandSample/RawDataBIDS/sub-A00064416/ses-DSA/func/sub-A00064416_ses-DSA_task-CHECKERBOARD_acq-1400_events.tsv'
checkerboardtwo='data/Projects/RocklandSample/RawDataBIDS/sub-A00064416/ses-DSA/func/sub-A00064416_ses-DSA_task-CHECKERBOARD_acq-645_events.tsv'
breathhold='data/Projects/RocklandSample/RawDataBIDS/sub-A00064416/ses-DSA/func/sub-A00064416_ses-DSA_task-BREATHHOLD_acq-1400_events.tsv'

# Create bucket object
s3_bucket_name = 'fcp-indi'
s3_prefix = 'data/Projects/RocklandSample/RawDataBIDS'
s3 = boto3.resource('s3')
s3_creds_path = '/path/to/jpellman-fcp-indi-keys.csv'
bucket = fetch_creds.return_bucket(s3_creds_path, s3_bucket_name)
s3_keys = bucket.objects.filter(Prefix=s3_prefix)

# Get the keys for NifTIs without events TSVs.
keylist = [key.key for key in s3_keys]
peerone_keylist = [key for key in keylist if 'PEER1' in key and '.nii.gz' in key and key.replace('_bold.nii.gz','_events.tsv') not in keylist]
peertwo_keylist = [key for key in keylist if 'PEER2' in key and '.nii.gz' in key and key.replace('_bold.nii.gz','_events.tsv') not in keylist]
checkerboardone_keylist = [key for key in keylist if 'CHECKERBOARD_acq-1400' in key and '.nii.gz' in key and key.replace('_bold.nii.gz','_events.tsv') not in keylist]
checkerboardtwo_keylist = [key for key in keylist if 'CHECKERBOARD_acq-645' in key and '.nii.gz' in key and key.replace('_bold.nii.gz','_events.tsv') not in keylist]
breathhold_keylist = [key for key in keylist if 'BREATHHOLD' in key and '.nii.gz' in key and key.replace('_bold.nii.gz','_events.tsv') not in keylist]

# Make dicts.
all_keys = { peerone : peerone_keylist, \
             peertwo : peertwo_keylist, \
             checkerboardone : checkerboardone_keylist, \
             checkerboardtwo : checkerboardtwo_keylist, \
             breathhold : breathhold_keylist }

# Copy the files.
with open('copying.log', 'w') as copylog:
    for tsv in all_keys.keys():
        print 'Making copies of %s' % tsv
        for new in tqdm(all_keys[tsv]):
            new = new.replace('_bold.nii.gz','_events.tsv')
            copylog.write('Source: %s\n' % tsv)
            copylog.write('Destination: %s\n\n' % new)
            if not dryrun:
                dst_obj = bucket.Object(key=new)
                dst_obj.copy_from(CopySource=s3_bucket_name + '/' + tsv, ACL='public-read')
