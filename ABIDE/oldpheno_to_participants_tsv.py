#!/usr/bin/env python
import os, sys
from glob import glob
import pandas as pd

pheno_dir = os.path.abspath(sys.argv[1])
out_dir = os.path.abspath(sys.argv[2])

for pheno_file in glob(os.path.join(pheno_dir,'*')):
    # Get site name and set up output path.
    site = os.path.basename(pheno_file).split('_')[1].lower().replace('.csv','')
    if not os.path.exists(os.path.join(out_dir,site)):
            os.makedirs(os.path.join(out_dir,site))
    target = os.path.join(out_dir,site,'participants.tsv')
    print target
    # Read in phenotypic csv as data frame.
    pheno = pd.read_csv(pheno_file,na_values=[-9999])
    # Remove site id column and columns with no data.
    pheno = pheno.drop('SITE_ID',1)
    for col in pheno.columns:
        if sum(pheno[col].isnull()) == len(pheno[col]):
            pheno = pheno.drop(col,1)
    pheno.columns = map(str.lower, pheno.columns)
    # Rename 'sub_id' to BIDS standard 'participant_id'
    pheno = pheno.rename(columns = {'sub_id':'participant_id'})
    # Save out.
    pheno.to_csv(target,sep='\t',na_rep='n/a',header=True,index=False)
