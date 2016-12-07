import pandas as pd
import sys,yaml
import os

aggphenof=sys.argv[1]
aggphenokeyf=sys.argv[2]
sitecol=sys.argv[3]
subcol=sys.argv[4]

opname=aggphenof.split('/')[-1].split('.')[0]+'.tsv'

aggpheno=pd.read_csv(aggphenof,dtype='str')




if os.path.isfile(aggphenokeyf):
    with open(aggphenokeyf,'rU') as ipf:
        phenokey=yaml.load(ipf)

    for k1 in phenokey.keys():
        if k1 in aggpheno.columns:
            print 'Changing data in column',k1,':',phenokey[k1]
            aggpheno[k1].replace(phenokey[k1],inplace=True)
else:
	print 'Phenotypic Key not specified or doesnt exist'

sites=set(aggpheno[sitecol].values)
collist=list(aggpheno.columns)
subcolind=collist.index(subcol)
collist[subcolind]='participant_id'
aggpheno.columns=collist

aggpheno.columns=map(str.lower,aggpheno.columns)



for site in sites:
    subdf=aggpheno[aggpheno[sitecol.lower()] ==site]
    subopname='participants_'+site+'_'+opname
    subopname=subopname.replace(' ','')
    print 'Writing file', subopname
    subdf.to_csv(subopname,index=False,sep='\t')
