#!/bin/bash/

# execute from inside the 'antismash_results' directory
# goes through each genome and runs the cluster type extraction script

# i=0
for DIR in GCF*/; do
	cd $DIR/
	python /project/flatiron/robin/projects/np_project/np-pipeline/test/clusterType_ex.py *.gbk;
	let i++
	cd ../
done
# echo 'finished with $i genomes'
exit