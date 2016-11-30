import pandas as pd
import sys,yaml,json
import os

aggscanparmf=sys.argv[1]
sitecol=sys.argv[2]


opname=aggscanparmf.split('/')[-1].split('.')[0]+'.json'

aggscanparm=pd.read_csv(aggscanparmf)
aggscanparm=aggscanparm.dropna(axis=0,how='all')
aggscanparm=aggscanparm.dropna(axis=1,how='all')
sites=set(aggscanparm[sitecol].values)

for site in sites:
    op=aggscanparm[aggscanparm[sitecol] == site].to_dict(orient='records')
    opnamesub=site+'_'+opname
    print 'Writing file', opnamesub
    with open(opnamesub,'w') as opf:
        json.dump(op,opf,indent=2,sort_keys=True)