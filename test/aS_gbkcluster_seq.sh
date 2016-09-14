#!/bin/bash/

# runs antismash iteratively on a set of fna files in a single
# directory, and generates a folder for each output file
echo " "
read -p "Are you in the 'antismash_results' directory? Type 'y' or 'n':" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	i=0
	for DIR in GCF*/; do
		cd $DIR/
		python /project/flatiron/robin/projects/np_project/np-pipeline/test/extract_gbkcluster_seq.py \
		*.gbk;
		let i++
		cd ../
	done
fi
echo " "
echo "Extracted cluster sequences from" $i "genomes."
exit
