import pandas as pd
import sys,yaml
import os



def split_df_varying(df, colstodrop, basecol):

    if len(colstodrop) != 0:
        ipdf=df.drop(colstodrop,axis=1).copy()
    else:
        ipdf=df.copy()     

    nonvary=[]
    vary=[]

    for i in ipdf.columns:
         if i != basecol:
             subdata=ipdf[[basecol,i]].copy()
             subshape=subdata[~subdata.duplicated()].shape
             if subshape[0] != len(ipdf[basecol].unique()):
                 #print 'varies',i,subshape
                 vary.append(i)
             else:
                 #print 'same',i,subshape
                 nonvary.append(i)
    
    #print vary,nonvary

    vdf=ipdf[[basecol]+vary]
    nvdf=ipdf[[basecol]+nonvary]

    return (vdf, nvdf)

if __name__ == '__main__':

    aggphenof=sys.argv[1]
    aggphenokeyf=sys.argv[2]
    sitecol=sys.argv[3]
    subcol=sys.argv[4]
    dropzerocolsrows=sys.argv[5]
    opdir=sys.argv[6]
    sescol=sys.argv[7]
    tsv_type=sys.argv[8]

    # Example python parsepheno.py ../CORR/CoRR_AggregatedPhenotypicData_zeropad_sesrename.csv ../CORR/CorrDataLegend.yml SITE SUBID True ../CORR/participant_tsvs/ SESSION session

    tsv_type_list=[
    'participant',
    'session']


    if tsv_type not in tsv_type_list:
        raise Exception('tsv type must be one of:\n'+'\n'.join(tsv_type_list))

    aggpheno=pd.read_csv(aggphenof,dtype='str')



    if not any(dropzerocolsrows == x for x in ['True','False']):
        raise Exception('dropzerocolsrows must be True or False')

    if dropzerocolsrows == 'True':
        aggpheno=aggpheno.dropna(axis=0,how='all')
        aggpheno=aggpheno.dropna(axis=1,how='all')


    if os.path.isfile(aggphenokeyf):
        with open(aggphenokeyf,'rU') as ipf:
            phenokey=yaml.load(ipf)

        for k1 in phenokey.keys():
            if k1 in aggpheno.columns:
                print 'Changing data in column',k1,':',phenokey[k1]
                aggpheno[k1].replace(phenokey[k1],inplace=True)
    else:
    	print 'Phenotypic Key not specified or doesnt exist'

    print aggpheno.columns

    sites=set(aggpheno[sitecol].values)

    collist=list(aggpheno.columns)

    subcolind=collist.index(subcol)
    collist[subcolind]='participant_id'

    sescolind=collist.index(sescol)
    collist[sescolind]='session_id'

    aggpheno.columns=collist

    aggpheno.columns=map(str.lower,aggpheno.columns)


    if tsv_type == 'participant':
        for site in sites:
            subdf=aggpheno[aggpheno[sitecol.lower()] == site]
            subopname=os.path.join(opdir,site,'participants.tsv')
            subopdir=os.path.join(opdir,site)
            if not os.path.isdir(subopdir):
                os.makedirs(subopdir)
            subdf.drop(sitecol.lower(),axis=1,inplace=True)
            print 'Writing file', subopname
            subdf.to_csv(subopname,index=False,sep='\t')

    elif tsv_type == 'session':
        for site in sites:

            sitedf=aggpheno[aggpheno[sitecol.lower()] == site].copy()

            sesdf, sitedf = split_df_varying(sitedf,[sitecol.lower()],'participant_id')

            sitedf=sitedf.drop_duplicates()
            siteopname=os.path.join(opdir,site,'participants.tsv')
            siteopdir=os.path.join(opdir,site)

            if not os.path.isdir(siteopdir):
                os.makedirs(siteopdir)

            #sitedf.drop(sitecol.lower(),axis=1,inplace=True)
            print 'Writing file', siteopname
            sitedf.to_csv(siteopname,index=False,sep='\t')

            subs=set(aggpheno['participant_id'][aggpheno[sitecol.lower()] == site].values)
            for sub in subs:
                subdf=sesdf[sesdf['participant_id'] == sub].copy()
                subject_id='sub-'+sub
                subopname=os.path.join(opdir,site,subject_id,subject_id+'_sessions.tsv')
                subopdir=os.path.join(opdir,site,subject_id)
                if not os.path.isdir(subopdir):
                    os.makedirs(subopdir)
                #subdf.drop(sitecol.lower(),axis=1,inplace=True)
                print 'Writing file', subopname
                subdf.to_csv(subopname,index=False,sep='\t')
