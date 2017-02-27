import pandas as pd
import sys,yaml,json
import os
import glob

# Read in aggscan file, and site column name
aggscanparmf=sys.argv[1]
sitecol=sys.argv[2]
opdir=sys.argv[3]
modality=sys.argv[4]

# BIDS Tag Order
tagorder=[
'ses-',
'task-',
'acq-',
'rec-',
'run-'
]

# Modality Suffices
modalities=[
'bold',
'T1w',
'dwi',
'T2w',
'FLAIR',
'PD',
'T1map',
'T2map'
'PDT2',
'inplaneT1',
'inplaneT2',
'angio',
'defacemask',
'SWImagandphase',
'phasediff'
]


if modality not in modalities:
    raise Exception('Modality specified must be one of (case sensitive): \n'+'\n'.join(modalities))



# Read in aggscan file and drop any rows and/or columns that are all NaN
aggscanparm=pd.read_csv(aggscanparmf)
aggscanparm=aggscanparm.dropna(axis=0,how='all')
aggscanparm=aggscanparm.dropna(axis=1,how='all')

if modality == 'bold' and 'TaskName' not in aggscanparm.columns:
    raise Exception('TaskName column must exist for bold scan sequence')


# Get list of sites to parse
sites=aggscanparm[sitecol].values

# Get list of task names if bold
if modality == 'bold':
    tasknames=aggscanparm['TaskName'].values
    # Create unique iterator
    unqit=zip(sites,tasknames)
else:
    unqit=zip(sites)

for ui in sorted(unqit):
    # Pull site from unique iterator
    site=ui[0]

    # Pull out sitename
    sitename='_'.join([sb for sb in site.split(' ') if '-' not in sb])

    # pull out tag metadata
    addparams=[sb for sb in site.split(' ') if '-' in sb]

    # Pair down aggscan file to site specific data
    if modality == 'bold':
        op=aggscanparm[(aggscanparm[sitecol] == site) & (aggscanparm['TaskName'] == ui[1])]
    else:
         op=aggscanparm[aggscanparm[sitecol] == site]

    if modality == 'bold':
        # Define task tag
        #scantask='task-'+str(op['Task'].values[0]).lower()
        scantask='task-'+ui[1]

    # Drop the site column, and any parameters that dont have values
    op.drop(sitecol,axis=1,inplace=True)
    op.dropna(axis=1,inplace=True)

    # Create list of dicts, and pull what should be the only dict out of it
    if len(op) == 1:
        op=op.to_dict(orient='records')[0]
    else:
        print op
        raise Exception('Incorrect number of rows in the final json, please check input')

    if 'SliceTiming' in op.keys():
        if op['SliceTiming'] == 'n/a':
            pass
        elif op['SliceTiming'] != 'n/a':
            try:
                op['SliceTiming']=map(float,op['SliceTiming'].split(','))
            except:
                raise Exception("Cannot process value in column 'SliceTiming' for ",ui)
        

    ## Setup specific op name
    if modality == 'bold':
        # Add task to parameters
        addparams=addparams+[scantask]
    # Order all parameters based on tag order from bids spec
    addparams=[ap for to in tagorder for ap in addparams if to in ap]
    # Construct opname
    if addparams:
        opname='_'.join(addparams)+'_'+modality+'.json'
    else:
        opname=modality+'.json'


    # Make full op path
    opdir_site=os.path.join(opdir,sitename)
    opnamesub=os.path.join(opdir,sitename,opname)
    opnamesub=opnamesub.replace(' ','_')

    print glob.glob(opnamesub)

    # It site subdir doesnt exist, create
    if not os.path.isdir(opdir_site):
        print 'making dir:', opdir_site
        os.makedirs(opdir_site)

    # Write output json
    print 'Writing file', opnamesub
    with open(opnamesub,'w') as opf:
        json.dump(op,opf,indent=2,sort_keys=True)