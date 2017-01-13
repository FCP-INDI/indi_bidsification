import sys, os, glob
from CPAC.AWS import aws_utils, fetch_creds


# For checking file integrity between local and upload files Currently only unix compatible
# Local and uploaded directories must have same file structure
# Example: python s3md5sumcheck.py ~/keys-format.csv fcp-indi data/Projects/ABIDE2/RawData/ /home/data/Incoming/abide2/bids_conv/bidsorg/

awscreds=sys.argv[1]
bucketname=sys.argv[2]
bucketpath=sys.argv[3]
localpath=sys.argv[4]

bucket = fetch_creds.return_bucket(awscreds, bucketname)


for k in bucket.list(prefix=bucketpath):
    buckname=k.name
    localname=k.name.replace(bucketpath,localpath)
    if os.path.isfile(localname):
        localname=os.path.abspath(localname)
        while os.path.islink(localname):
            localname=os.readlink(localname)
        x=os.popen('md5sum '+localname).read()
        localmd5=str(x.split(' ')[0])
        etag=str(k.etag).replace('"','')
        if '-' in etag:
            numparts=int(etag.split('-')[-1])
            #print (os.stat(localname).st_size/(1024.0*1024.0))/numparts
            y=os.popen('bash s3etag.sh '+localname+' 8').read()
            localetag=y.strip().split(' ')[-1]
            if etag == localetag:
               pass#print 'all good',buckname
            elif etag != localetag:
                print 'no bueno', buckname, localetag, etag
        elif '-' not in etag and localmd5 == etag:
            pass#print 'all good',buckname
        elif '-' not in etag and localmd5 != etag:
            print 'no bueno', buckname, localmd5, etag
    else:
        print 'not found locally',buckname
