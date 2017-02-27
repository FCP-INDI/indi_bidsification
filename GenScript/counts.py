from CPAC.AWS import fetch_creds,aws_utils

paths=[l.strip() for l in open('./filepaths.txt','rU')]


bucket=fetch_creds.return_bucket('/Users/david.oconner/awscreds/keys_new_indi-fcp/doconnor-fcp-indi-keys-clarkformat.csv','fcp-indi')

tott1w=0
totfmri=0
totdwi=0
totsubs=0
for path in paths:
    srclist=[]
    print path
    for i,k in enumerate(bucket.list(prefix=path)):
        srclist.append(k.name)
        #print k.name
    print "no of T1w:",len([s for s in srclist if '_T1w.nii' in s])
    print "no of fMRI:",len([s for s in srclist if '_bold.nii' in s])
    print "no of DWI:",len([s for s in srclist if '_dwi.nii' in s])
    print "no of subs",len(set([t for s in srclist for t in s.split('/') if 'sub-' in t and '.' not in t]))

    tott1w=tott1w+len([s for s in srclist if '_T1w.nii' in s])
    totfmri=totfmri+len([s for s in srclist if '_bold.nii' in s])
    totdwi=totdwi+len([s for s in srclist if '_dwi.nii' in s])
    totsubs=totsubs+len(set([t for s in srclist for t in s.split('/') if 'sub-' in t and '.' not in t]))

print 'TOTALS'
print "total no of T1w:",tott1w
print "total no of fMRI:",totfmri
print "total no of DWI:",totdwi
print "total no of subs",totsubs