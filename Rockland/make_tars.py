#!/usr/bin/env python
import tarfile
from glob import glob
import shutil
import os
import re
import subprocess
import sys
from CPAC.AWS import aws_utils, fetch_creds

remappings = {
    'ses-clg_A' : 'ses-CLGA' , \
    'ses-clg_2' : 'ses-CLG2' , \
    'ses-clg_2R' : 'ses-CLG2R' , \
    'ses-clg_4' : 'ses-CLG4' , \
    'ses-clg_4R' : 'ses-CLG4R' , \
    'ses-dsc_A' : 'ses-DSA' , \
    'ses-dsc_2' : 'ses-DS2' , \
    'ses-nfb_A' : 'ses-NFBA' , \
    'ses-nfb_2' : 'ses-NFB2' , \
    'ses-nfb_3' : 'ses-NFB3' , \
    'ses-nfb_2R' : 'ses-NFB2R' , \
    'task-breath_hold_1400_bold' : 'task-BREATHHOLD_acq-1400_bold' , \
    'task-breath_hold_bold' : 'task-BREATHHOLD_acq-1400_bold' , \
    'task-checkerboard_1400_bold' : 'task-CHECKERBOARD_acq-1400_bold' , \
    'task-checkerboard_645_bold' : 'task-CHECKERBOARD_acq-645_bold' , \
    'task-rest_1400_bold' : 'task-rest_acq-1400_bold' , \
    'task-rest_645_bold' : 'task-rest_acq-645_bold' , \
    'task-dmn_tracking_test_bold' : 'task-DMNTRACKINGTEST_bold' , \
    'task-dmn_tracking_train_bold' : 'task-DMNTRACKINGTRAIN_bold' , \
    'task-moral_dilemma_bold' : 'task-MORALDILEMMA_bold' , \
    'task-msit_bold' : 'task-MSIT_bold' , \
    'task-mask_bold' : 'task-MASK_bold' , \
    'task-peer1_bold' : 'task-PEER1_bold' , \
    'task-peer2_bold' : 'task-PEER2_bold' , \
    'task-pcasl_rest_bold' : 'task-rest_pcasl' , \
    'task-rest_cap_bold' : 'task-rest_acq-CAP_bold' }

releases = ['/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r1', '/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r2', '/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r3', '/home/data/Incoming/rockland_sample/DiscSci_R4/organized_symlinks', '/home/data/Incoming/rockland_sample/DiscSci_R5/anonymized_imaging_data/organized_symlinks', '/home/data/Incoming/rockland_sample/DiscSci_R6/organized_symlinks', '/home/data/Incoming/rockland_sample/DiscSci_R7/organized_symlinks', '/home/data/Incoming/rockland_sample/DiscSci_R8/organized_symlinks']


release_folders = {'/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r1' : 'Release_1', \
         '/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r2' : 'Release_2', \
         '/home/data/Incoming/rockland_sample/DiscSci_R1-3/organized_symlinks_r3' : 'Release_3', \
         '/home/data/Incoming/rockland_sample/DiscSci_R4/organized_symlinks' : 'Release_4', \
         '/home/data/Incoming/rockland_sample/DiscSci_R5/anonymized_imaging_data/organized_symlinks' : 'Release_5', \
         '/home/data/Incoming/rockland_sample/DiscSci_R6/organized_symlinks' : 'Release_6', \
         '/home/data/Incoming/rockland_sample/DiscSci_R7/organized_symlinks' : 'Release_7', \
         '/home/data/Incoming/rockland_sample/DiscSci_R8/organized_symlinks' : 'Release_8' }


release_files = {}
warehouse_dir = '/data2/bids_warehouse/Anonymized'
orphans = []
missing = {}

for release in releases:
    for filename in glob(os.path.join(release, '*/*/*/*')):
        oldfilename = filename
        newfilename = []
        if '.dcm' in filename:
            continue
        filename = re.sub(r"(A\d{8})/(.+)/mprage_siemens.*_defaced/mprage_siemens.*_defaced\.nii\.gz", r"sub-\1/ses-\2/anat/sub-\1_ses-\2_T1w.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/mprage_siemens.*_defaced/anat_defaced\.nii\.gz", r"sub-\1/ses-\2/anat/sub-\1_ses-\2_T1w.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/dmn_f.+/.+\.gz", r"sub-\1/ses-\2/anat/sub-\1_ses-\2_T1w.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(rest.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(dmn_t.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(moral.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(peer.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(msit)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(mask)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(fieldmap)/.+\.gz", r"sub-\1/ses-\2/fmap/sub-\1_ses-\2_magnitude1.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(breath.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(check.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/(pcasl.+)/.+\.gz", r"sub-\1/ses-\2/func/sub-\1_ses-\2_task-\3_bold.nii.gz", filename)
        filename = re.sub(r"(A\d{8})/(.+)/dti_137_ap/dti_137_ap\.(.+)", r"sub-\1/ses-\2/dwi/sub-\1_ses-\2_dwi.\3", filename)
        filename = re.sub(r"(A\d{8})/(.+)/diff_137_ap/diff_137_ap\.(.+)", r"sub-\1/ses-\2/dwi/sub-\1_ses-\2_dwi.\3", filename)
        filename = re.sub(r"(A\d{8})/(.+)/diff_137_ap/diff_137\.(.+)", r"sub-\1/ses-\2/dwi/sub-\1_ses-\2_dwi.\3", filename)
        filename = re.sub(r"(A\d{8})/(.+)/diff_137_ap/DIFF_137\.(.+)", r"sub-\1/ses-\2/dwi/sub-\1_ses-\2_dwi.\3", filename)

        if 'sub' not in filename:
            orphans.append(filename)
            continue
        newfilename = filename.replace(release, warehouse_dir)
        for k in remappings:
            if k in newfilename:
                newfilename = newfilename.replace(k, remappings[k])
        if release not in release_files.keys():
            release_files[release] = [newfilename]
        else:
            release_files[release].append(newfilename)
        if not os.path.isfile(newfilename):
            if oldfilename not in missing.keys():
                missing[oldfilename] = newfilename

print "Files that didn\'t match the regexes:"
print orphans

for f in missing:
    # Fieldmaps need to be fixed so we'll ignore this for now.
    if 'fmap' in missing[f]:
        continue
    print '%s is missing!' % missing[f]
    print 'Copying %s to %s' % (f, missing[f])
    if not os.path.exists(os.path.dirname(missing[f])):
            os.makedirs(os.path.dirname(missing[f]))
    shutil.copy(f, missing[f])
    # Denote niis.
    if '.nii' in missing[f]:
        cmd = '3drefit -denote %s' % missing[f]
        print 'Running %s' % cmd
        p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        print stdout
        print stderr

# Divide participants into groups of 3 for each release.

bucket = fetch_creds.return_bucket('/home/jpellman/jpellman-fcp-indi-keys_oldfmt.csv', 'fcp-indi')

for release in release_files:
    if release_folders[release] != 'Release_2':
        continue
    groups = {}
    outdir = os.path.join(warehouse_dir+'_Tars',release_folders[release])
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    perps = [re.findall('sub-A[\d]{8}', fname)[0] for fname in release_files[release]]
    perps = set(perps)
    group_idx = 0
    for idx, perp in enumerate(perps):
        if 'group_%d' % group_idx not in groups.keys():
            groups['group_%d' % group_idx] = []
        groups['group_%d' % group_idx].append(perp)
#        print groups['group_%d' % group_idx]
        if idx % 3 == 0:
            group_idx+=1
    for group in groups:
        groupfiles = []
        for perp in groups[group]:
            groupfiles.extend([fname for fname in release_files[release] if perp in fname])
        # Make relative paths in tar.
        os.chdir(warehouse_dir)
        for name in groupfiles:
            print '%s will be added to %s' % (name.replace(warehouse_dir+'/', './'), os.path.join(outdir, group+'.tar.gz'))
        if not os.path.isfile(os.path.join(outdir, group+'.tar.gz')):
            with tarfile.open(os.path.join(outdir, group+'.tar.gz'), "w:gz") as tgz:
                for name in groupfiles:
                    tgz.add(name.replace(warehouse_dir+'/', './'))
        aws_utils.s3_upload(bucket, [os.path.join(outdir, group+'.tar.gz')] , ['data/Projects/RocklandSample/RawDataTars/'+release_folders[release]+'/'+group+'.tar.gz'] , make_public=True)
        os.remove(os.path.join(outdir, group+'.tar.gz'))
