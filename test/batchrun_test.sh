#!/bin/bash/

# runs antismash iteratively on a set of fna files in a single
# directory, and generates a folder for each output file

echo "Please confirm that there is no existing 'antismash_results' directory here"
read -p "...and that you are in the directory containing your .fna files? (type 'y' if you wanna antiSMASH!)" -n 1 -r
echo    
if [[ $REPLY =~ ^[Yy]$ ]]
then
# run antismash script on each .fna genome file
# should be in format 'GCF_000020425.1_ASM2042v1_genomic.fna'
# puts each results set into a new directory named by the accession number without the '.1'
	mkdir antismash_results/
	i=0
	for FILE in *.fna; do
		FILENAME=${FILE%.*}
		python /project/flatiron/robin/antismash/run_antismash.py -c 48 \
		./$FILE \
		--outputfolder ./antismash_results/$FILENAME/ \
		--inclusive --disable-BioSQL --disable-svg --disable-embl --disable-write_metabolicmodel \
		--disable-xls --disable-html --disable-BiosynML;
	# after running antismash, extract the sequences from the .gbk files and put into new directory
		let i++
	done
fi
cd ./antismash_results/
for DIR in ./; do
	cd ./DIR
	python /project/flatiron/robin/projects/np_project/np-pipeline/test/extract_gbkcluster_seq.py \
	*.gbk;
	cd ..
done
echo ' '
echo "finally finished antiSMASHing" $i "genomes."
echo ' '
exit