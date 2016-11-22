#!/usr/bin/env python
import os, sys
import pandas as pd

codes = { 
        'SEX' : { 1: 'Female', 2: 'Male'} , \
        'HANDEDNESS' : {  1: 'Left', 2: 'Right', 3: 'Ambidextrous' } , \
        'VISUAL_STIMULATION_CONDITION' : {1: 'Fixation', 2: 'Blank Screen', 3: 'Word', 4:'Eyes closed', 5: 'Other' } , \
        'TIME_OF_DAY' : { 0 : '0-3:59', 1 : '4:00-7:59', 2 : '8:00-11:59', 3 : '12:00-15:59', 4 : '16-19:59', 5 :'20:00-23:59' } , \
        'SEASON' : {  0: 'Winter', 1: 'Spring', 2: 'Summer', 3: 'Fall' } , \
        'SMOKER' : { 0 : 'No' , 1 : 'Yes' } , \
        'EDUCATION_LEVEL' : { \
            1 : 'Eighth grade or less' , \
            2 : 'Some high school' , \
            3 : 'High School graduate or GED' , \
            4 : 'Some college or post high school' , \
            5 : 'College Graduate' , \
            6 : 'Advanced graduate or professional degree' } }

pheno_dir = os.path.abspath(sys.argv[1])
out_dir = os.path.abspath(sys.argv[2])

pheno_file = os.path.join(pheno_dir, 'nyu_1_phenotypic_data.csv')
# Get site name and set up output path.
site = 'nyu_1'
if not os.path.exists(os.path.join(out_dir,site)):
        os.makedirs(os.path.join(out_dir,site))
target = os.path.join(out_dir,site,'participants.tsv')
# Read in phenotypic csv as data frame.
pheno = pd.read_csv(pheno_file,na_values=['n/a',-1, '#'])
# Make column values more verbose
pheno = pheno.replace(codes)
# Make columns lowercase.
pheno.columns = map(str.lower, pheno.columns)
# Remove columns with no data.
for col in pheno.columns:
    if sum(pheno[col].isnull()) == len(pheno[col]):
        pheno = pheno.drop(col,1)
pheno = pheno.drop('session',1)
# Rename 'sub_id' to BIDS standard 'participant_id'
pheno = pheno.rename(columns = {'sub_id':'participant_id'})
# Save out.
pheno.to_csv(target,sep='\t',na_rep='n/a',header=True,index=False)
