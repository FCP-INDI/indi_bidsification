import re
import nibabel as nb
import os
import numpy as np
import sys


def bvs_to_mat(ipfile):
    lines=[l.strip() for l in open(ipfile, 'rU')]
    newmat=np.array([re.findall(r"[-+]?\d+\.\d+",l) for l in lines])
    newbv='\n'.join([' '.join(map(str,n)) for n in newmat])

    return newbv

def writebvs(dwipath,valorvec):

    if not any(valorvec == x for x in ['bval','bvec']):
        raise Exception('input variable "valorvec" must be one of: bval, bvec') 

    valorvec='.'+valorvec

    bvfile=dwipath.replace('.nii.gz',valorvec)

    if not os.path.isfile(bvfile):
        raise Exception('This file does not have the requisite bval file')

    newbvs=bvs_to_mat(bvfile)

    oldbvs=open(bvfile,'rU').read()
    newbvfile=bvfile.replace(valorvec,'_corrected'+valorvec)

    if newbvs != oldbvs and os.path.isfile(newbvfile):
        print dwipath, 'corrected '+valorvec+' exists'
    elif newbvs != oldbvs and not os.path.isfile(newbvfile):
        print dwipath, 'corrected '+valorvec+' does not exist writing now'
        fo=open(newbvfile,'w')
        fo.write(newbvs)
        fo.close()
    elif newbvs == oldbvs:
        print dwipath, valorvec+' format already correct'


def correct_bvs(workingdir):
    for root, dirs, fs in os.walk(workingdir):
        for f in fs:
             if 'dwi.nii.gz' in f:
                 fpath=os.path.join(root,f)
                 writebvs(fpath,'bval')
                 writebvs(fpath,'bvec')

if __name__ == '__main__':

    workdir=sys.argv[1]
    correct_bvs(workdir)
