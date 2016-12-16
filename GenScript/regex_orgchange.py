from CPAC.AWS import aws_utils, fetch_creds
import tarfile, yaml
import os
import shutil
import re
import sys


def makeallpublic(bucket,fpath):
    for i,k in enumerate(bucket.list(prefix=fpath)):   
        print 'making public: ',k.name          
        k.set_acl('public-read')

def s3_match_and_move(keyspath, matchdct, ipdir, opdir, test):
    bucket = fetch_creds.return_bucket(keyspath, 'fcp-indi')
    
    
    srclist=[]
    
    files_converted=[]
    destlist_tot=[]
    
    for i,k in enumerate(bucket.list(prefix=ipdir)):
        srclist.append(k.name)
        print k.name
    
    srclist=sorted(srclist)
    
    
    for mk in sorted(matchdct.keys()):
        print mk
    
        srclist_filt=[]
        destlist=[]
    
    
        for sl in srclist:

            if 'include' in matchdct[mk].keys():

                if re.search(matchdct[mk]['match'][0],sl) and any(m in sl for m in matchdct[mk]['include']):
                    #print sl,re.sub(matchdct[mk][0],matchdct[mk][1],sl)
                    srclist_filt.append(sl)
                    destlist.append(re.sub(matchdct[mk]['match'][0],matchdct[mk]['match'][1],sl).replace(ipdir,opdir))
            else:

                if re.search(matchdct[mk]['match'][0],sl):
                    #print sl,re.sub(matchdct[mk][0],matchdct[mk][1],sl)
                    srclist_filt.append(sl)
                    destlist.append(re.sub(matchdct[mk]['match'][0],matchdct[mk]['match'][1],sl).replace(ipdir,opdir))
    
        if len(destlist) != len(set(destlist)):
            raise Exception('Duplicate Destination Filepaths exist')

        files_converted=files_converted+srclist_filt
        destlist_tot=destlist_tot+destlist
            
        if test == 'yes':
            for j,slf in enumerate(srclist_filt):
                print 'changing: ',srclist_filt[j],destlist[j]
        else:
            # Note might error with make_public=True, removing it stops error, unsure why error occurs
            aws_utils.s3_rename(bucket,srclist_filt,destlist,keep_old=False, make_public=True,overwrite=False)
    
    
    print 'num files pulled in:',len(files_converted),'num files produced',len(destlist_tot)
    
    if len(files_converted) != len(destlist_tot):
        raise Exception('There is a mismatch in the total files read in, and total files produced')
    
    #print 'The following files were not pulled in from the source directory',set(srclist)-set(files_converted)

def local_regex(matchdct,ipdir,opdir):
    srclist=[]
    files_converted=[]
    destlist_tot=[]
    
    for root,dirs,fs in os.walk(ipdir):
        for f in fs:
            fpath=os.path.join(root,f)
            srclist.append(fpath)
    
    for mk in sorted(matchdct.keys()):
        print mk
        srclist_filt=[s for s in srclist if re.search(matchdct[mk]['match'][0],s)]
        destlist=[re.sub(matchdct[mk]['match'][0],matchdct[mk]['match'][1],sf).replace(ipdir,opdir) for sf in srclist_filt]
        files_converted=files_converted+srclist_filt
        destlist_tot=destlist_tot+destlist
    
        if len(destlist) != len(set(destlist)):
            raise Exception('Duplicate Destination Filepaths exist')
    
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
                os.symlink(os.path.abspath(oldfile),newfile)
            else:
                pass #print 'File ',newfile,' already exists, please delete if a new file is needed'
    
    print 'num files pulled in:',len(files_converted),'num files produced',len(destlist_tot)
    
    if len(files_converted) != len(destlist_tot):
        raise Exception('There is a mismatch in the total files read in, and total files produced')
    
    print 'The following files were not pulled in from the source directory',set(srclist)-set(files_converted)

if __name__ == '__main__':

    keyspath=sys.argv[1]
    matchdct_fpath=sys.argv[2]
    ipdir=sys.argv[3]
    opdir=sys.argv[4]
    s3flag=sys.argv[5]
    test='no'
    
    #Be sure to put in the last forward slash as may act as wildcard otherwise
    #ipdir='data/Projects/CORR/RawData/'
    #opdir='data/Projects/CORR/RawDataBIDs/'
    
    try:
        s3flag=bool(s3flag)
    except:
        raise Exception('s3flag must be True or False')
    
    with open(matchdct_fpath) as mdf:
        matchdct=yaml.load(mdf)
    
    
    
    if s3flag == True:
        s3_match_and_move(keyspath, matchdct, ipdir, opdir, test)

    
    elif s3flag == False:
        local_regex(matchdct,ipdir,opdir)
                
    else:
        raise Exception('Must specify s3flag')
    