for i in *.json;do mv -nv $i ${i/_adhd200_scan_params/};done 

for i in *anat*.json;do mv -nv $i ${i/anat/T1w};done
for i in *rest*.json;do mv -nv $i ${i/rest./task-rest_func.};done

mv -nv Peking_3a_T1w.json Peking_3_T1w_acq-1.json
mv -nv Peking_3b_T1w.json Peking_3_T1w_acq-2.json
mv -nv Peking_3c_T1w.json Peking_3_T1w_acq-3.json
mv -nv Peking_3d_T1w.json Peking_3_T1w_acq-4.json
mv -nv Peking_3e_T1w.json Peking_3_T1w_acq-5.json

mv -nv WashU_1_task-rest_func.json WashU_task-reststudy1_func.json
mv -nv WashU_2_task-rest_func.json WashU_task-reststudy2_func.json
mv -nv WashU_3_task-rest_func.json WashU_task-reststudy3_func.json