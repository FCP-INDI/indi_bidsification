import numpy as np
import nibabel as nb
import glob, os


for site in glob.glob('*'):
    lst=[]
    for root,dirs,fs in os.walk(site):
                 for f in fs:    
                     fpath=os.path.join(root,f)    
                     if 'dwi.nii' in fpath:    
                         imf=nb.Nifti1Image.load(fpath)    
                         h=imf.get_header()    
                         lst.append(str(h['dim_info']))
    print site, set(lst)

    dim_info_set=set(lst)

    if len(dim_info_set) > 1:
        raise Exception('More than one value for dim_info in this dataset')

    for s in dim_info_set:
        print return_diminfo_cats(bin(int(s))) 


def return_diminfo_cats(binstr):

    """
    Takes in a bit array in str format and interprets the first (last?) size bits
    as if they encode three directions, as specified here:
    https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/dim_info.html
    """

     opdct={}

     opdct['freqdir']=int(binstr,2) & int(bin(3),2)
     opdct['phasedir']=int(binstr,2) >> 2 & int(bin(3),2)
     opdct['slicedir']=int(binstr,2) >> 4 & int(bin(3),2)

     return opdct