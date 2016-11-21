#!/usr/bin/env python
import os, sys
from glob import glob
import pandas as pd

pheno_dir = os.path.abspath(sys.argv[1])
out_dir = os.path.abspath(sys.argv[2])

codes = { 'dx_group' : { 1 : 'Autism', 2 : 'Control'} , \
        'dsm_iv_tr' :  { 0 : 'Control', 1 : 'Autism', 2 : 'Aspergers', 3 : 'PDD-NOSE', 4 : 'Aspergers or PDD-NOS' } , \
        'sex' : { 1 : 'Male', 2 : 'Female' } , \
        'adi_r_rsrch_reliable' : { 0 : 'Not Research Reliable', 1 : 'Research Reliable' } , \
        'ados_rsrch_reliable' : { 0 : 'Not Research Reliable', 1 : 'Research Reliable' } , \
        'srs_version' : { 1 : 'Child', 2 : 'Adult' } , \
        'current_med_status' : { 0 : 'Not Taking Medication' , 1 : 'Taking Medication' } , \
        'off_stimulants_at_scan' : { 0 : 'No',  1 : 'Yes' } , \
        'vineland_informant' : { 1 : 'Parent', 2 : 'Self' } , \
        'eye_status_at_scan' : { 1 : 'Open', 2 : 'Closed' } }

for pheno_file in glob(os.path.join(pheno_dir,'*')):
    # Get site name and set up output path.
    site = os.path.basename(pheno_file).split('_')[1].lower().replace('.csv','')
    if not os.path.exists(os.path.join(out_dir,site)):
            os.makedirs(os.path.join(out_dir,site))
    target = os.path.join(out_dir,site,'participants.tsv')
    # Read in phenotypic csv as data frame.
    pheno = pd.read_csv(pheno_file,na_values=[-9999])
    # Remove site id column and columns with no data. Make columns lowercase.
    pheno = pheno.drop('SITE_ID',1)
    pheno.columns = map(str.lower, pheno.columns)
    for col in pheno.columns:
        if sum(pheno[col].isnull()) == len(pheno[col]):
            pheno = pheno.drop(col,1)
    pheno = pheno.replace(codes)
    # Rename 'sub_id' to BIDS standard 'participant_id'
    pheno = pheno.rename(columns = {'sub_id':'participant_id'})
    # Save out.
    pheno.to_csv(target,sep='\t',na_rep='n/a',header=True,index=False)   
