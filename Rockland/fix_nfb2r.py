from CPAC.AWS import aws_utils, fetch_creds

creds = '/home/johnpellman/Documents/SysAdmin_IT/NKI/Credentials/AWS/Access_Keys/fcp-indi-new/jpellman-fcp-indi-keys_oldfmt.csv'
bucket = fetch_creds.return_bucket(creds, 'fcp-indi')

perps=['sub-A00028185','sub-A00033747','sub-A00037511','sub-A00034854']
srclist=[]
for perp in perps:
    for i,k in enumerate(bucket.list(prefix='data/Projects/RocklandSample/RawDataBIDS/%s' % perp)):
        if 'NFB2' in k.name and ('NFB2R' not in k.name or 'NFB2REP' in k.name):
            srclist.append(k.name)
            print k.name

srclist=sorted(srclist)
destlist=[perp.replace('NFB2','NFB2R').replace('NFB2RREP','NFB2R') for perp in srclist]

for i,k in enumerate(srclist):
    print '%s to %s' % (srclist[i], destlist[i])

aws_utils.s3_rename(bucket,srclist,destlist,keep_old=False,make_public=True)
