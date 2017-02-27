for i in *.json;do mv -nv $i ${i/_corr_scan_params/};done 

for i in *anat*.json;do mv -nv $i ${i/anat/T1w};done
for i in *rest*.json;do mv -nv $i ${i/rest/task-rest_func};done
for i in *dti*.json;do mv -nv $i ${i/dti/dwi};done


mv -nv NKI_1_645_task-rest_func.json NKI_1_task-rest_acq-tr645ms_func.json
mv -nv NKI_1_1400_task-rest_func.json NKI_1_task-rest_acq-tr1400ms_func.json
mv -nv NKI_1_2500_task-rest_func.json NKI_1_task-rest_acq-tr2500ms_func.json

for i in *IBATRT*.json;do mv -nv $i ${i/IBATRT/IBA_TRT};done
for i in *IACAS_1*.json;do mv -nv $i ${i/IACAS_1/IACAS};done 
for i in *JHNU_1*.json;do mv -nv $i ${i/JHNU_1/JHNU};done 
for i in *MRN_1*.json;do mv -nv $i ${i/MRN_1/MRN};done 
for i in *NKI_1*.json;do mv -nv $i ${i/NKI_1/NKI_TRT};done 
for i in *UM_1*.json;do mv -nv $i ${i/UM_1/UM};done 
for i in *UWM_1*.json;do mv -nv $i ${i/UWM_1/UWM};done 
for i in *XHCUMS_1*.json;do mv -nv $i ${i/XHCUMS_1/XHCUMS};done 