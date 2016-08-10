#!/usr/bin/env python

usage = "execute from antismash results directory to compile each genome's cluster into one .faa file"

import os, os.path

def compile_aa():
	if "compiled_cluster_aa_seqs" not in os.listdir('.'):
		os.mkdir("compiled_cluster_aa_seqs")
	for dir in os.listdir('.'):
		if dir.startswith('GCF'):
			if "cluster_aa_sequences" not in os.listdir(dir):
				pass
			else:
				fname = dir.strip('_genomic')
				outfilename = fname + '_cluster_aa_seqs.mpfa'
				outfile = open(os.path.join("compiled_cluster_aa_seqs", outfilename), 'w')
				for file in os.listdir(os.path.join(dir,'cluster_aa_sequences/')):
					if file.endswith('.mpfa'):
						with open(os.path.join(dir,'cluster_aa_sequences/',file), 'r') as infile:
							for line in infile:
								outfile.write(line)
				outfile.close()
		else:
			pass
if __name__ == '__main__':
	compile_aa()