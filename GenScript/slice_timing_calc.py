import sys, os
import numpy as np
import pandas as pd

#TR=2
#sequence='seq+'
#numslices=34
#manufacturer='Siemens'
#software='vb17'

sequence_list={
'siemens': ['int+','int-','seq+','seq-'],
'philips': ['int+','int-','seq+','seq-'], # Default, Central
'ge': ['int+','int-','seq+','seq-']}

manuf_list=['philips','siemens','ge']



def calculate_slice_times(TR,sequence,numslices,manufacturer):

    manufacturer=manufacturer.lower()

    if manufacturer not in manuf_list:
        raise Exception('Manufacturer specified must be one of: '+'\n'.join(manuf_list))

    if sequence not in sequence_list[manufacturer]:
        raise Exception('Sequence specified must be one of: '+'\n'.join(sequence_list[manufacturer]))

    if manufacturer == 'siemens':

        if sequence == 'seq+':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000

        elif sequence == 'seq-':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=slice_times[::-1]
        
        elif sequence == 'int+' and (numslices % 2):
            x=np.arange(0,TR,float(TR)/numslices)*1000
            y1=x[:(len(x)/2)+1]
            y2=x[(len(x)/2)+1:]
            slice_times=np.hstack([np.array([y1[i],y2[i]]) for i in range(0,len(x)/2)])
            slice_times=np.hstack(np.array((slice_times,y1[-1])))

        elif sequence == 'int+' and not (numslices % 2):
            x=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=np.hstack([np.array([x[(len(x)/2):][i],x[:(len(x)/2)][i]]) for i in range(0,len(x)/2)])

        elif sequence == 'int-':
            raise Exception('Siemens interleaved acquisition are always interleaved ascending')

    elif manufacturer == 'philips':

        if sequence == 'seq+':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000

        elif sequence == 'seq-':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=slice_times[::-1]
        
        elif sequence == 'int+':
            raise Exception('Philips int+ not coded yet')

        elif sequence == 'int-':
            raise Exception('Philips int- not coded yet')

    elif manufacturer == 'ge':
        if sequence == 'seq+':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000

        elif sequence == 'seq-':
            slice_times=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=slice_times[::-1]
        
        elif sequence == 'int+' and not numslices % 2:
            x=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=np.hstack([np.array([x[:(len(x)/2)][i],x[(len(x)/2):][i]]) for i in range(0,len(x)/2)])

        elif sequence == 'int+' and numslices % 2:
            x=np.arange(0,TR,float(TR)/numslices)*1000
            y1=x[:(len(x)/2)+1]
            y2=x[(len(x)/2)+1:]
            slice_times=np.hstack([np.array([y1[i],y2[i]]) for i in range(0,len(x)/2)])
            slice_times=np.hstack(np.array((slice_times,y1[-1])))

        elif sequence == 'int-' and not numslices % 2:
            x=np.arange(0,TR,float(TR)/numslices)*1000
            slice_times=np.hstack([np.array([x[(len(x)/2):][i],x[:(len(x)/2)][i]]) for i in range(0,len(x)/2)])
            slice_times=slice_times[::-1]

        elif sequence == 'int-' and numslices % 2:
            x=np.arange(0,TR,float(TR)/numslices)*1000
            y1=x[:(len(x)/2)+1]
            y2=x[(len(x)/2)+1:]
            slice_times=np.hstack([np.array([y1[i],y2[i]]) for i in range(0,len(x)/2)])
            slice_times=np.hstack(np.array((slice_times,y1[-1])))
            slice_times=slice_times[::-1]

    return slice_times

def round2(x):
    return round(x,2)

def add_slicetime_to_csv(ipcsv):
    df=pd.read_csv(ipcsv)

    needed_cols=['Manufacturer','RepetitionTime','SliceAcquisitionOrder','NumberOfSlices','Site']

    if not all(x in df.columns for x in needed_cols):
        raise Exception('For slice timing information to be calculated the following columns are needed:'+' '.join(needed_cols))

    sites=df.Site

    df['SliceTiming']=map(str,np.zeros(df.shape[0]))

    for site in sites:
        site_TR=df[df.Site == site]['RepetitionTime'].values[0]
        site_Man=df[df.Site == site]['Manufacturer'].values[0]
        site_Nslice=df[df.Site == site]['NumberOfSlices'].values[0]
        site_AcqOrd=df[df.Site == site]['SliceAcquisitionOrder'].values[0]
        site_TE=df[df.Site == site]['EchoTime'].values[0]

        print site, site_TR, site_AcqOrd, site_Nslice, site_Man

        try:
            slice_times=calculate_slice_times(site_TR, site_AcqOrd, site_Nslice, site_Man)
            slice_times=map(round2, slice_times)
            slice_times=map(str,slice_times)
            slice_times=','.join(slice_times)
        except :
            slice_times='n/a'

        
        df['SliceTiming'][df.Site == site] = slice_times

    df.to_csv(ipcsv.replace('.csv','_slicetimes.csv'),index=False)
