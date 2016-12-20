#!/bin/bash
# Use in a directory with at least one *R1.fastq/*R2.fastq pair (or single read, for -SE mode)
# Must have shi7en environment sourced

mkdir truseq2
mkdir truseq3
mkdir truseq3-2
mkdir nextera
cd truseq2
shi7en --adaptor TruSeq2 --flash False --convert_fasta False --combine_fasta False -trim_l 50 -i ../ --debug
cd ../
cd truseq3
shi7en --adaptor TruSeq3 --flash False --convert_fasta False --combine_fasta False -trim_l 50 -i ../ --debug
cd ../
cd truseq3-2
shi7en --adaptor TruSeq3-2 --flash False --convert_fasta False --combine_fasta False -trim_l 50 -i ../ --debug
cd ../
cd nextera
shi7en --adaptor Nextera --flash False --convert_fasta False --combine_fasta False -trim_l 50 -i ../ --debug
cd ../
ls -l truseq2/temp/axe/
ls -l truseq3/temp/axe/
ls -l truseq3-2/temp/axe/
ls -l nextera/temp/axe/
echo "Which is the smallest?"