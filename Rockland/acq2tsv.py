import json
import pandas as pd
import bioread
from settings import ACQRELABELS

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


