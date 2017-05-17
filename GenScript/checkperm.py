import boto
import sys
import boto3
import botocore
import os
import urllib2


ipkey=sys.argv[1]

bpath=sys.argv[2]
                                                  
botoversion=2

_id,key=[l.strip() for l in open(ipkey,'rU')][1].split(',')[1:]


if botoversion == 2:
	
    c=boto.connect_s3(aws_access_key_id=_id, aws_secret_access_key=key) 
    bucket=c.get_bucket('fcp-indi')

    #for k in bucket.list('data/Projects/CORR/RawDataBIDS/IPCAS_1/'):
    for k in bucket.list(bpath):
        print k.key
        vers=[v for v in bucket.list_versions(k.key)] 
        if len(vers) > 0:
            #print k.key, len(vers)#, vers[-1].version_id

            for i,ver in enumerate(vers):
                vid=ver.version_id
                dl='http://fcp-indi.s3.amazonaws.com/'+k.key+'?versionId='+vid
                request=urllib2.Request(dl)
                request.get_method = lambda : 'HEAD'
                try:
                    response = urllib2.urlopen(request)
                    #print response.info()
                except urllib2.HTTPError as e:
                    if e.code == 403:
                        print e, k.key, vid, [g.permission for g in ver.get_acl().acl.grants],bucket.get_acl(key_name=k.key,version_id=vid)
                        #print dl
                        #bucket.set_acl('public-read',key_name=k.key,version_id=vid)
                        #k.set_acl('public-read')
                        #ver.set_acl('public-read')
                    elif e.code == 405:
                        print e,k.key,vid
                    else:
                        raise 
                    #fo=open('accessissues.txt','a')
                    #fo.write(dl+','+str(e.code)+','+str(i+1)+'/'+str(len(vers))+'\n')
                    #fo.close()

            #os.system('wget '+dl)
        #for v in vers:
    	#    try:
        #        for grant in v.get_acl().acl.grants:
        #    	    if 'sub-0003032_ses-1_run-1_T1w.nii.gz' in k.key and v.version_id == 'MKZ.2lEzN9WGgP8S5VRYa_axzNNJRbhX':#grant.permission != 'FULL_CONTROL' and
        #                print k.key
        #                print grant.permission, grant.id, v.version_id
        #                v.set_acl('public-read')

                    #print k.generate_url(30,version_id=v.version_id)
        #    except AttributeError as e:
        #        print e

if botoversion == 3:

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('fcp-indi')

    for k in bucket.objects.filter(Prefix='data/Projects/CORR/RawDataBIDS/BMB_1/sub-0003032/ses-1/anat/sub-0003032_ses-1_run-1_T1w.nii.gz'):
            versions = bucket.object_versions.filter(Prefix=k.key)
            for v in versions:
                print v



### Web stuff + Notes
# urllib https://docs.python.org/2/library/urllib.html
# check if s3 url exists http://stackoverflow.com/questions/25983093/check-if-an-s3-url-exists
# Using urllib 2 to check head of file rather than downloading http://stackoverflow.com/questions/4421170/making-http-head-request-with-urllib2-from-python-2
# handling url errors http://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python
# s3 permissions http://stackoverflow.com/questions/40518642/setting-specific-permission-in-amazon-s3-boto-bucket
# s3 delete markers (405?) http://docs.aws.amazon.com/AmazonS3/latest/dev/DeleteMarker.html
# s3 error responses http://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html
# Need to check set permissions in bucket obeject, key object, and version object
# Boto3 http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Object.Acl
