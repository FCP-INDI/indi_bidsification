#!/usr/bin/env python
import os, sys
from glob import glob
import pandas as pd

codes = {'SJTYP' : {1 : 'MTA Randomized Trial Subject', 2 : 'Local Normative Comparison Group (LNCG) Subject' } , \
    'MJUser' : { 0 : 'No', 1 : 'Yes' } , \
    'GROUP' : { 1 : 'ADHD Substance User (used Marijuana once per month or more)', \
        2 : 'ADHD Non-Substance User (used Marijuana less than 4x/past year)', \
        3 : 'LNCG Substance User (used Marijuana once per month or more)', \
        4 : 'LNCG Non-Substance User (used Marijuana less than 4x/past year)' } , \
    'SEXMF' : { 'M' : 'Male', 'F' : 'Female' } , \
    'ETHNIC' : { 1 : 'Caucasian' , \
        2 : 'Black' , \
        3 : 'Non-black Hispanic' , \
        4 : 'Black Hispanic' , \
        5 : 'Asian' , \
        6 : 'Native American Indian' , \
        7 : 'Mixed' , \
        8 : 'Other' } ,\
    'HANDEDNESS' : { 1 : 'Right', \
        2 : 'Left' , \
        3 : 'Ambidextrous' } , \
    'EDUC' : { 1 : 'No degree or certificate', \
        2 : 'High School Diploma',\
        3 : 'GED',\
        4 : 'Certificate from a technical school or equivalent',\
        5 : 'Associates Degree',\
        6 : 'Bachelor Degree'} , \
    'ADHDMEDS' : { 1 : 'No', \
        2 : 'Yes, some of the time' , \
        3 : 'Yes, most of the time' } , \
    'SMOKER' : { 0 : 'No' , 1 : 'Yes' } }

pheno_dir = os.path.abspath(sys.argv[1])
out_dir = os.path.abspath(sys.argv[2])

pheno_file = os.path.join(pheno_dir, 'mta_1_phenotypic_data.csv')
# Get site name and set up output path.
site = 'mta_1'
if not os.path.exists(os.path.join(out_dir,site)):
        os.makedirs(os.path.join(out_dir,site))
target = os.path.join(out_dir,site,'participants.tsv')
# Read in phenotypic csv as data frame.
pheno = pd.read_csv(pheno_file,na_values=['.',-1, '#'])
# Make column values more verbose
pheno = pheno.replace(codes)
# Make columns lowercase.
pheno.columns = map(str.lower, pheno.columns)
# Rename 'sub_id' to BIDS standard 'participant_id'
pheno = pheno.rename(columns = {'subid':'participant_id'})
# Save out.
pheno.to_csv(target,sep='\t',na_rep='n/a',header=True,index=False)
