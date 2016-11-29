from CPAC.AWS import aws_utils, fetch_creds
import tarfile, yaml
import os
import shutil
import re
import sys

keyspath=sys.argv[1]
matchdct_fpath=sys.argv[2]
ipdir=sys.argv[3]
opdir=sys.argv[4]
s3flag=sys.argv[5]


#Be sure to put in the last forward slash as may act as wildcard otherwise
#ipdir='data/Projects/CORR/RawData/'
#opdir='data/Projects/CORR/RawDataBIDs/'

with open(matchdct_fpath) as mdf:
    matchdct=yaml.load(mdf)


if s3flag == True:
    bucket = fetch_creds.return_bucket(keyspath, 'fcp-indi')


    srclist=[]
    for i,k in enumerate(bucket.list(prefix=ipdir)):
        srclist.append(k.name)
        print k.name

    srclist=sorted(srclist)


    for mk in sorted(matchdct.keys()):
        print mk

        srclist_filt=[]
        destlist=[]

        for sl in sorted(srclist):
            if re.match(matchdct[mk][0],sl):
                #print sl,re.sub(matchdct[mk][0],matchdct[mk][1],sl)
                srclist_filt.append(sl)
                destlist.append(re.sub(matchdct[mk][0],matchdct[mk][1],sl).replace(ipdir,opdir))


        # Note might error with make_public=True, removing it stops error, unsure why error occurs
        aws_utils.s3_rename(bucket,srclist_filt,destlist,keep_old=True)#,make_public=True)

else:
    srclist=[]

    for root,dirs,fs in os.walk(ipdir):
        for f in fs:
            fpath=os.path.join(root,f)
            srclist.append(fpath)

    for mk in sorted(matchdct.keys()):
        print mk
        srclist_filt=[s for s in srclist if re.match(matchdct[mk][0],s)]
        destlist=[re.sub(matchdct[mk][0],matchdct[mk][1],sf).replace(ipdir,opdir) for sf in srclist_filt]

        changekey=zip(srclist_filt,destlist)

        for elem in changekey:
            oldfile=elem[0]
            newfile=elem[1]
            newdir=os.path.dirname(newfile)

            if not os.path.isdir(newdir):
                print 'Making Directory ',newdir
                os.makedirs(newdir)

            if not os.path.isfile(newfile) and not os.path.islink(newfile):
                print 'Linking ',oldfile,' to ',newfile
                os.symlink(oldfile,newfile)
            else:
                pass #print 'File ',newfile,' already exists, please delete if a new file is needed'
            
