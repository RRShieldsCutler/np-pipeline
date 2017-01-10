#!/usr/bin/env Python

import os
import os.path

usage = "execute from antismash_results directory to compile each genome's cluster into one .faa file"


def compile_seq(cdir, outfile):
	for file in os.listdir(os.path.join(cdir, 'cluster_dna_sequences/')):
		if file.endswith('.txt'):
			with open(os.path.join(cdir, 'cluster_dna_sequences/', file), 'r') as infile:
				for line in infile:
					outfile.write(line)
	return outfile


def main():
	if "compiled_cluster_dna_seqs" not in os.listdir('.'):
		os.mkdir("compiled_cluster_dna_seqs")
	for cdir in os.listdir('.'):
		if cdir.startswith('GCF'):
			if "cluster_sequences" not in os.listdir(cdir):
				pass
			else:
				fname = cdir.strip('_genomic')
				outfilename = fname + '_cluster_seqs.fna'
				outfile = open(os.path.join("compiled_cluster_dna_seqs", outfilename), 'w')
				compile_seq(cdir, outfile)
				outfile.close()
		else:
			pass


if __name__ == '__main__':
	main()

