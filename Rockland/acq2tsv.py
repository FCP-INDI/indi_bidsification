import os
import json
import pandas as pd
import bioread
from settings import ACQRELABELS, SERIESMAP

def physio_to_tsv(source, target, despiked_target, start_time = 0):
    '''
    Name: physio_to_tsv
    Description: A function to convert physiological data to
    BIDS style gzipped TSVs and JSONs.
    Arguments:
    -----------------------------------------------------------------------------
    source : string
        The path to the BIOPAC .acq file to be converted to a TSV.
    target : string
        The path to where the TSV should be stored.
    despiked_target : string
        The path to where the despiked TSV should be stored.
    start_time : int/float
        Override the start time value that is saved to the sidecar JSON.
    '''
    try:
        acq = bioread.read_file(source)
    except:
        return None

    # Create a dictionary to store metadata
    metadata_dict = {}

    # Store column names, timeseries, and despiked timeseries for each column.
    columns = []
    timeseries = []
    despiked_timeseries = []

    # Populate the columns and timeseries lists.
    for channel in range(len(acq.channels)):
        columns.append(acq.channels[channel].name)
        timeseries.append(acq.channels[channel].data)
        despiked_timeseries.append(despike(acq.channels[channel].data)[0])

    # Convert timeseries and despiked timeseries to pandas dataframe and save out.
    timeseries_df = pd.DataFrame(timeseries).T
    timeseries_df.to_csv(target,sep='\t', na_rep='n/a', header=False, index=False, compression='gzip')
    despiked_timeseries_df = pd.DataFrame(despiked_timeseries).T
    despiked_timeseries_df.to_csv(despiked_target,sep='\t', na_rep='n/a', header=False, index=False, compression='gzip')

    # Re-label columns to be human-readable for the JSON.
    for idx, column in enumerate(columns):
        for relabel in ACQRELABELS:
            if relabel in column:
                columns[idx] = ACQRELABELS[relabel]

    # Populate the metadata dictionary and save it out.
    metadata_dict["SamplingFrequency"] = acq.samples_per_second
    metadata_dict["StartTime"] = start_time
    metadata_dict["Columns"] = columns
    with open(target.replace('.tsv.gz','.json'),"w") as json_target:
        json.dump(metadata_dict, json_target)
    with open(despiked_target.replace('.tsv.gz','.json'),"w") as json_target:
        json.dump(metadata_dict, json_target)

    return timeseries_df

def despike(ts, fac=5):
    ts=list(ts)
    window=range(2,len(ts)-2)
    adiff1=[]
    adiff2=[]
    idx=[]
    for index in window:
        adiff1.append((abs(ts[index-2]-ts[index-1]) + abs(ts[index+1]-ts[index+2]))/2)
        adiff2.append((abs(ts[index-1]-ts[index]) + abs(ts[index]-ts[index+1]))/2)
        if adiff2[len(adiff2)-1] > (fac*adiff1[len(adiff1)-1]):
            idx.append(len(adiff1)-1+2)
    for index in idx:
        ts[index]=(ts[index+1]+ts[index-1])/2
    return ts, idx

def get_bids_path(filename):
    '''
    Desc:
        Takes in a BIOPAC filename of the form <URSI>_<VISIT>_<SERIES> and converts it to a BIDS filename.
        Displays an error for an unrecognized series or URSI.
    Input:
        filename (str) - The BIOPAC file name.
    '''
    flist = filename.split('_')
    ursi = flist[0]
    visit = flist[1]
    series = '_'.join(flist[2:]).replace('.acq','')
    if series in SERIESMAP.keys():
        series = SERIESMAP[series]
    else:
        raise Exception
    newfile = 'sub-%s_ses-%s_%s.tsv.gz' % (ursi, visit, series)
    if 'dwi' in newfile:
        newpath = os.path.join('sub-%s' % ursi ,'dwi',newfile)
    else:
        newpath = os.path.join('sub-%s' % ursi,'func',newfile)
    return newpath

if __name__ == '__main__':
    '''
    Takes in an input directory and converts to BIDS in a specified out directory.
    '''
    import sys
    if len(sys.argv) != 3:
        print 'Usage: python acq2tsv.py <input directory> <output directory>'
        sys.exit(1)
    indir = os.path.abspath(sys.argv[1])
    outdir = os.path.abspath(sys.argv[2])
   
    # Check if input and output dirs exist
    if not os.path.exists(indir):
        sys.exit(1)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    with open(os.path.join(outdir,'err.txt'), 'w') as err:
        for dirpath, dirnames, filenames in os.walk(indir): 
            for filename in filenames:
                if '.acq' in filename:
                    source = os.path.join(dirpath, filename)
                    try:
                        target = get_bids_path(filename)
                        despiked_target = target.replace('_physio','_recording-despiked_physio')
                        target = os.path.join(outdir, target)
                        despiked_target = os.path.join(outdir, 'derivatives', target)
                    except:
                        print 'Could not get BIDS file path for %s.\n' % source
                        print 'Correct filename / double check.'
                        err.write('%s\n' % source)
                        continue
                    print '%s : %s : %s' % (source, target, despiked_target)
                    
                    if not os.path.isfile(target):
                        if not os.path.exists(os.path.dirname(target)):
                            os.makedirs(os.path.dirname(target))
                        physio_to_tsv(source, target, despiked_target)

