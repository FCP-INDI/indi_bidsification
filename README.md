# indi_bidsification
Scripts related to the process of converting INDI datasets into BIDS format.

### Study Folders:
ABIDE, ABIDE2, CORR, ADHD200, ACPI, Rockland

### Subfolders:
- participants_tsvs	-> Phenotypic files in tsv format broken out by subject, and session where suitable
- phenotypic_files -> All phenotypic data in csv format
- scan_jsons -> MRI Acquisition parameters in json formatsessions option for parse pheno 3 months ago

### Validation Folder
- Two scripts, one to download subsets of datasets on S3 and run the bids validator, and one to download and fix tsv files with NaNs instead of NAs

### GenScript Folder
- checkperm.py -> script to check permissions of s3 bucket objects versions
- counts.py -> basic count script for bucket
- niftiheadcheck.py -> script for looking at the dim_info field in nii headers, using bit-shifting
- parsenii.py - > script for interacting with and changing nii headers
- parsepheno.py -> turns one big spreadsheet into participant and session tsvs for BIDs
- parsescanparams.py -> Turns a site level mri acq params spreadsheet into scan jsons for each modality listed
- regex_orgchange.py -> reformats file structures based on regular expressions, locally and on S3
- s3etag.sh -> Figures out file md5sum based on AWS etag
- s3md5sumcheck.py -> Can compare md5sums of s3 objects and local ones to figure out inconsistencies
- s3tar.py -> downloads data from s3, tars and reuploads
- slice_timing_calc.py -> generates slice times for each slice in fMRI data based on TR, number of slices, slice acquisition method and manufacturer
