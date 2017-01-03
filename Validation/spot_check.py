#!/usr/bin/env python
from CPAC.AWS import aws_utils, fetch_creds
import os
import sys
import shutil
import commands
import smtplib
from email.mime.text import MIMEText

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

tmp = os.path.join(tmp, s3_prefix.split('/')[-2])

# Fetch 4 participants from the BIDS dataset and download to a temporary directory.
# Start by fetching all keys.
bucket = fetch_creds.return_bucket(creds, 'fcp-indi')
key_list=[]
for i,k in enumerate(bucket.list(prefix=s3_prefix)):
    key_list.append(str(k.name).replace(s3_prefix,''))

# Fetch all unique participant codes.
participants = [k.split('/')[0] for k in key_list if 'sub-' in k]
participants = sorted(list(set(participants)))
participants = participants[0:4]

downloads_list = [os.path.join(s3_prefix,k) for k in key_list if ('sub-' in k and k.split('/')[0] in participants) or ('sub-' not in k)]

# Download the files.
aws_utils.s3_download(bucket, downloads_list, tmp, bucket_prefix=s3_prefix)

# Run the BIDS validator- save the output to a file that is based off the last 'subdirectory'
# in the prefix.
validator_output = commands.getoutput('bids-validator %s' % tmp)
shutil.rmtree(tmp)

# E-mail the output to me and Dave.
email_list = ['john.pellman@childmind.org']
msg = MIMEText(validator_output)
msg['Subject'] = 'BIDS validation results for %s' % (s3_prefix)
msg['From'] = 'dcm_srv@ned.childmind.org'
msg['To'] = '; '.join(email_list)

s = smtplib.SMTP('localhost')
s.sendmail('dcm_srv@ned.childmind.org', email_list, msg.as_string())
s.quit()
