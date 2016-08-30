#!/usr/bin/env Python

import argparse
import sys
import os
from collections import defaultdict

from ninja_utils.parsers import FASTA
from ninja_utils.utils import find_between

# >ncbi_tid|206672|ref|NC_004307.2_cluster004_ctg1_orf02030|organism|Bifidobacterium_longum|
# The arg parser for this wrapper
def make_arg_parser():
	parser = argparse.ArgumentParser(description='Reformat multi-fasta file header to include refseq id, ncbi_tid, and Genus_species')
	parser.add_argument('-i', '--input', help='Input is a multi-cluster FASTA file.', default='-')
	parser.add_argument('-b', '--bread', help='Where to find the header for the sequence (default="ref|,|")', default='ref|,|')
	return parser

def build_cluster_map(inf, bread='ref|,|'):
	begin,end = bread.split(',')
	cluster_map = defaultdict(set)
	fasta_gen = FASTA(inf)
	for header, sequence in fasta_gen.read():
		if '.cluster' in header:
			header = header.replace('.cluster','_cluster')
		ref = find_between(header, begin, end)
		header_split = ref.split('_')
		key = '_'.join(header_split[:3])
		value = header_split[-1]
		cluster_map[key].add(value)
	return cluster_map

def main():
	parser = make_arg_parser()
	args = parser.parse_args()

	# parse command line
	with open(args.input, 'r') if args.input != '-' else sys.stdin as inf:
		cluster_map = build_cluster_map(inf, bread=args.bread)
		# how many clusters there are
		print(len(list(cluster_map.keys())))
		# how many ORFs per cluster for all clusters
		print([len(value) for value in cluster_map.values()])

if __name__ == '__main__':
	main()

