for i in *.json;do mv -nv $i ${i/_acpi_bids_scan_params/};done 

for i in *anat*.json;do mv -nv $i ${i/anat/T1w};done
for i in *rest*.json;do mv -nv $i ${i/rest/task-rest_func};done

for i in *.json;do mv -nv $i $(echo $i | tr '[:upper:]' '[:lower:]'); done