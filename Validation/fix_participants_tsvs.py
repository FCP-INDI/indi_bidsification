#!/usr/bin/env python
from CPAC.AWS import aws_utils, fetch_creds
import os, sys
import pandas as pd

# Define the S3 prefix where the BIDS base dir is.
if not len(sys.argv) == 4:
    print 'Usage: %s <path to AWS creds> <temporary directory> <S3 prefix to BIDS base>' % sys.argv[0]
    sys.exit(1)
creds = sys.argv[1]
tmp = sys.argv[2]
s3_prefix = sys.argv[3]

# Assumes last character in s3_prefix is a slash.
if s3_prefix[-1] != '/':
    s3_prefix+='/'

fixed = os.path.join(tmp, 'fixed', s3_prefix.split('/')[-2])
orig = os.path.join(tmp, 'orig', s3_prefix.split('/')[-2])

if not os.path.exists(fixed):
    os.makedirs(fixed)
if not os.path.exists(orig):
    os.makedirs(orig)

# Fetch 4 participants from the BIDS dataset and download to a temporary directory.
# Start by fetching all keys.
bucket = fetch_creds.return_bucket(creds, 'fcp-indi')
key_list=[]
for i,k in enumerate(bucket.list(prefix=s3_prefix)):
    if 'participants.tsv' in str(k.name):
        key_list.append(str(k.name))

# Download the files.
aws_utils.s3_download(bucket, key_list, orig, bucket_prefix=s3_prefix)

# Change NaNs to 'n/a'.
df = pd.read_csv(os.path.join(orig,'participants.tsv'), sep='\t')
df.to_csv(os.path.join(fixed,'participants.tsv'),sep='\t',na_rep='n/a',header=True,index=False)
aws_utils.s3_upload(bucket,[os.path.join(fixed,'participants.tsv')], ['/'.join([s3_prefix, 'participants.tsv'])], make_public=True, overwrite=True)
