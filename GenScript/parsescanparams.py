import pandas as pd
import sys,yaml,json
import os


# Read in aggscan file, and site column name
aggscanparmf=sys.argv[1]
sitecol=sys.argv[2]

# Setup general op name
opname=aggscanparmf.split('/')[-1].split('.')[0]+'.json'

# Read in aggscan file and drop any rows and/or columns that are all NaN
aggscanparm=pd.read_csv(aggscanparmf)
aggscanparm=aggscanparm.dropna(axis=0,how='all')
aggscanparm=aggscanparm.dropna(axis=1,how='all')

# Get list of sites to parse
sites=set(aggscanparm[sitecol].values)

for site in sites:

    # Pair down aggscan file to site specific data
    op=aggscanparm[aggscanparm[sitecol] == site]

    # Drop the site column, and any parameters that dont have values
    op.drop(sitecol,axis=1,inplace=True)
    op.dropna(axis=1,inplace=True)

    # Create dict
    op=op.to_dict(orient='records')

    # Setup site specific op name
    opnamesub=site+'_'+opname
    opnamesub=opnamesub.replace(' ','_')

    # Write output json
    print 'Writing file', opnamesub
    with open(opnamesub,'w') as opf:
        json.dump(op,opf,indent=2,sort_keys=True)