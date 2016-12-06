#!/usr/bin/env python
import os, sys
from glob import glob
import pandas as pd
import shutil
import re

datadir=sys.argv[1]
outdir=os.path.abspath(sys.argv[2])

for f in glob(os.path.join(datadir,"*")):
    print "Currently BIDSifying %s" % f
    ursi = re.findall("NFB_[0-9]{5}", f)
    if ursi:
        ursi = ursi[0]
        ursi = ursi.replace("NFB_", "M109")
    else:
        continue
    fdir = os.path.join(outdir,'sub-%s/ses-NFB3/func' % ursi)
    if not os.path.exists(fdir):
        os.makedirs(fdir)
    root, ext = os.path.splitext(f)
    if 'csv' in ext:
        target = os.path.join(fdir, 'sub-%s_ses-NFB3_task-MORALDILEMMA_bold.csv' % ursi)
        # Ignore if already copied.
        if os.path.isfile(target):
            continue
        df = pd.read_csv(f)
        # Remove PHI
        if 'date' in df.columns.tolist():
            df = df.drop('date', 1)
            df.participant = ursi
            df.to_csv(target, index=False)
    elif 'log' in ext:
        target = os.path.join(fdir, 'sub-%s_ses-NFB3_task-MORALDILEMMA_bold.log' % ursi)
        # Ignore if already copied.
        if os.path.isfile(target):
            continue
        shutil.copy(f, target)
    # TODO psydat files?
#    elif 'psydat' in ext:
#        continue
