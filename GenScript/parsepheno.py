import pandas as pd
import sys,yaml

aggphenof=sys.argv[1]
aggphenokeyf=sys.argv[2]
sitecol=sys.argv[3]
subcol=sys.argv[4]



aggpheno=pd.read_csv(aggphenof)

sites=aggpheno[sitecol].values

with open(aggphenokeyf,'rU') as ipf:
	phenokey=yaml.load(ipf)


for k1 in phenokey.keys():
    print k1
    if k1 in aggpheno.columns:
        print k1
        aggpheno[k1].replace(phenokey[k1],inplace=True)


collist=list(aggpheno.columns)
subcolind=collist.index(subcol)
collist[subcolind]='participant_id'
aggpheno.columns=collist

aggpheno.columns=map(str.lower,aggpheno.columns)



for site in sites:
    subdf=aggpheno[aggpheno[sitecol.lower()] ==site]
    subdf.to_csv('participants_'+site+'_'+aggphenof.split('/')[-1],index=False)
