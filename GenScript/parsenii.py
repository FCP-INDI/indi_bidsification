import re
import nibabel as nb
import os
import numpy as np
import sys
import shutil
import collections
import pandas as pd
import dicom as dcm

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

def parseniihead(workingdir,modality,headfield,element):

    for root,dirs,fs in os.walk(workingdir):
        for f in fs:
            if '.nii' in f and modality in f:
                fpath=os.path.join(root,f)
                f=nb.Nifti1Image.load(fpath)
                print fpath
                if not headfield:
                    print f.header
                else:
                    print f.header[headfield]
                header=f.header
                header['pixdim'][4] = 1
                affine=f.affine
                data=f.dataobj
                opimg=nb.Nifti1Image(data,affine,header=header)
                #nb.save(opimg,fpath)



def agg_headers(ipdir,opname, datatype):

    df=pd.DataFrame(dtype='object')

    for root,dirs,fs in os.walk(ipdir):
        if datatype == '.nii.gz':
            for f in fs:
                if datatype in f:
                    fpath=os.path.join(root,f)
                    header=nb.Nifti1Image.load(fpath).get_header()
                    for k in header.keys():
                        #print k,header[k]
                        if isinstance(header[k],list):
                            value='x'.join(header[k])
                        elif isinstance(header[k],np.ndarray) and not any(t in str(header[k].dtype) for t in ['float','int','S']):
                            if len(header[k]) == 1:
                                value=header[k].astype('str')
                            elif len(header[k]) > 1:
                                value='x'.join(header[k].astype('str'))
                        elif isinstance(header[k],np.ndarray) and any(t in str(header[k].dtype) for t in ['float','int','S']):
                            value=str(header[k])
                        else:
                            value=header[k]
                        value=value.replace('\n','')
                        df.set_value(fpath,k,value)

        elif datatype == '.dcm':
            if len(dirs) == 0 and any('.dcm' in o for o in os.listdir(root)):
                print root,dirs,sorted(glob.glob(root+'/*.dcm'))[0]
                refdcm=dcm.read_file(sorted(glob.glob(root+'/*.dcm'))[0])
                for k in sorted(refdcm.keys()):
                    nums=[n for n in re.findall('\w+',str(k))]
                    nums=[int(str(n),base=16) for n in nums]
                    x=refdcm[nums[0],nums[1]]
                    #print x.name
                    df.set_value(root,str(x.name),str(x.value))




    if opname != '':
        df.to_csv(opname)

    return df

def philips_dti_fix(ipdir, numdirecs, numb0s):
    for root, dirs, fs in os.walk(ipdir):
        for f in fs:
            if 'dwi.nii.gz' in f:
                fpath=os.path.join(root,f)
                imgf=nb.Nifti1Image.load(fpath)
                header=imgf.header
                numvols=header['dim'][4]
                if numvols != (numdirecs+numb0s):
                    print fpath, numvols
                    olddata=imgf.get_data()
                    newimgdata=olddata[:,:,:,numvols-(numdirecs+numb0s):]
                    newderiv=olddata[:,:,:,-(numvols-(numdirecs+numb0s)):]
                    
                    newheader=header
                    newheader['dim'][4]=33
                    derivheader=header
                    derivheader['dim'][4]=1

                    affine=imgf.affine

                    newimg=nb.Nifti1Image(newimgdata, affine,header=newheader)
                    deriv=nb.Nifti1Image(newimgdata, affine,header=newheader)

                    derivpath=os.path.join(ipdir,'dervatives',root.replace(ipdir,''))
                    derivop=os.path.join(derivpath,f.replace('dwi.nii.gz','dwiadc.nii.gz'))
                    
                    if not os.path.isdir(derivpath):
                        os.makedirs(derivpath)
             
                    nb.save(newimg,fpath)
                    nb.save(deriv,derivop)

if __name__ == '__main__':

    workdir=sys.argv[1]
    correct_bvs(workdir)
