#!/usr/bin/env python
'''
bidsify_nfb_logs.py
Usage: bidsify_nfb_logs.py <datadir> <outdir> <taskname>
'''
import os, sys
import pandas as pd
import shutil
import re
import commands

if not len(sys.argv) == 4:
    print "Usage: %s <datadir> <outdir> <taskname>" % sys.argv[0]
    sys.exit(1)

datadir = sys.argv[1]
outdir = os.path.abspath(sys.argv[2])
taskname = str(sys.argv[3])

files = [os.path.join(datadir, f) for f in os.listdir(datadir) if os.path.isfile(os.path.join(datadir, f))]

for f in files:
    print "Currently BIDSifying %s" % f
    ursi = re.findall("NFB_[0-9]{5}", f)
    ursi.extend(re.findall("NFB[0-9]{5}", f))
    ursi.extend(re.findall("M109[0-9]{5}", f))
    if ursi:
        ursi = ursi[0]
        ursi = ursi.replace("NFB_", "M109")
        ursi = ursi.replace("NFB", "M109")
    else:
        continue
    fdir = os.path.join(outdir, 'sub-%s/ses-NFB3/func' % ursi)
    if not os.path.exists(fdir):
        os.makedirs(fdir)
    root, ext = os.path.splitext(f)
    if 'csv' in ext:
        target = os.path.join(fdir, 'sub-%s_ses-NFB3_task-%s_bold.csv' % (ursi, taskname))
        # Save to another file and reconcile manually.
        if os.path.isfile(target):
            target = os.path.join(fdir, 'sub-%s_ses-NFB3_task-%s_bold_dup-%s' % (ursi, taskname, os.path.basename(f)))
            print "File with BIDS name already copied for %s" % f
        try:
            df = pd.read_csv(f)
        except Exception as e:
            print "Couldn't read %s" % f
            print e
            continue
        if 'participant' in df.columns.tolist():
            df = df.drop('participant', 1)
            #df.participant = ursi
        # Remove PHI
        if 'date' in df.columns.tolist():
            df = df.drop('date', 1)
        df.to_csv(target, index=False)
    elif 'log' in ext or 'txt' in ext:
        paradigm_count = commands.getoutput(r'egrep -c "#PARADIGM" "%s"' % f).strip()
        if int(paradigm_count) == 0 and taskname == 'DMNTRACKINGTEST' and 'txt' in ext:
            continue
        msec_count = commands.getoutput(r'egrep -c "16 msec" "%s"' % f).strip()
        if int(msec_count) != 0:
            continue
        target = os.path.join(fdir, 'sub-%s_ses-NFB3_task-%s_bold%s' % (ursi, taskname, ext))
        # Save to another file and reconcile manually.
        if os.path.isfile(target):
            print "File with BIDS name already copied for %s" % f
            target = os.path.join(fdir, 'sub-%s_ses-NFB3_task-%s_bold_dup-%s' % (ursi, taskname, os.path.basename(f)))
        shutil.copy(f, target)
    # TODO psydat files?
#    elif 'psydat' in ext:
#        continue
