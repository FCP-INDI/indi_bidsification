#!/usr/bin/env python
import os, sys
import pandas as pd

codes = { 'Site' : { 1 : 'Peking University' , \
        2 : 'Bradley Hospital/Brown University' , \
        3 : 'Kennedy Krieger Institute' , \
        4 : 'NeuroIMAGE Sample' , \
        5 : 'New York University Child Study Center' , \
        6 : 'Oregon Health & Science University' , \
        7 : 'University of Pittsburgh' , \
        8 : 'Washington University in St. Louis' } , \
        'Gender' : { 0 : 'Female', 1 : 'Male' } , \
        'Handedness' : { '0' : 'Left', '1' : 'Right', '2' : 'Ambidextrous' } , \
        'DX' : { 0 : 'Typically Developing Children', 1 : 'ADHD-Combined', \
        2 : 'ADHD-Hyperactive/Impulsive', 3 : 'ADHD-Inattentive' } , \
        'Secondar Dx' : { 0 : 'Typically Developing Children', 1 : 'ADHD-Combined', \
        2 : 'ADHD-Hyperactive/Impulsive', 3 : 'ADHD-Inattentive' } , \
        'ADHD Measure' : { 1 : 'ADHD Rating Scale IV (ADHD-RS)', 2 : 'Conners\' Parent Rating Scale-Revised, Long version (CPRS-LV)', \
        3 : 'Connors\' Rating Scale-3rd Edition' }, \
        'IQ Measure' :  { 1 : 'Wechsler Intelligence Scale for Children, Fourth Edition (WISC-IV)', \
                    2 : 'Wechsler Abbreviated Scale of Intelligence (WASI)' , \
                    3 : 'Wechsler Intelligence Scale for Chinese Children-Revised (WISCC-R)' , \
                    4 : 'Two subtest WASI' , \
                    5 : 'Two subtest WISC or WAIS - Block Design and Vocabulary' } , \
        'Med Status' : { 1 : 'Medication Naive', 2 : 'Not Medication Naive' } , \
        'QC_Rest_1' : { 0 : 'Questionable', 1 : 'Pass' } , \
        'QC_Rest_2' : { 0 : 'Questionable', 1 : 'Pass' } , \
        'QC_Rest_3' : { 0 : 'Questionable', 1 : 'Pass' } , \
        'QC_Rest_4' : { 0 : 'Questionable', 1 : 'Pass' } , \
        'QC_Anatomical_1' : { 0 : 'Questionable', 1 : 'Pass' } , \
        'QC_Anatomical_2' : { 0 : 'Questionable', 1 : 'Pass' } }

pheno_dir = os.path.abspath(sys.argv[1])
out_dir = os.path.abspath(sys.argv[2])
pheno_file = os.path.join(pheno_dir, 'allSubs_testSet_phenotypic_dx.csv')
pheno_file_fix = os.path.join(pheno_dir, 'ADHD-200.PhenotypicFix.csv')
# Read in phenotypic csv as data frame.
pheno = pd.read_csv(pheno_file,na_values=['-999','N/A', 'pending'])
fix = pd.read_csv(pheno_file,na_values=['-999','N/A', 'pending'])
fix = fix.rename(columns = {'ScanDir ID':'ID'})
pheno = pd.concat([pheno, fix])

# Rename 'subid' to BIDS standard 'participant_id'
pheno = pheno.rename(columns = {'ID':'participant_id'})
# Make participants.tsv files for all sites separately.
for site in pheno['Site'].unique():
    # Get Site name and set up output path.
    site_dir=os.path.join(out_dir,codes['Site'][site].replace(' ','_').replace('/','-'))

    if not os.path.exists(site_dir):
        os.makedirs(site_dir)
    target = os.path.join(site_dir,'participants.tsv')
    site_df = pheno[pheno['Site']==site].drop('Site',1)
    # Remove empty columns
    for col in site_df.columns:
        if sum(site_df[col].isnull()) == len(site_df[col]):
            site_df = site_df.drop(col,1)
    # Make column values more verbose
    site_df = site_df.replace(codes)
    # Make columns lowercase and remove spaces.
    site_df.columns = map(str.lower, site_df.columns)
    site_df.columns = [col.replace(' ','_') for col in site_df.columns]
    # NYU CSC didn't do categorical handedness
    if site == 5:
        site_df['handedness'] = site_df['handedness'].replace('Right','1')
    # Move disclaimer to the last column if present.
    if 'disclaimer' in site_df.columns:
        cols = site_df.columns.tolist()
        cols.remove('disclaimer')
        cols.append('disclaimer')
        site_df = site_df[cols]
    # Save out.
    site_df.to_csv(target,sep='\t',na_rep='n/a',header=True,index=False)
