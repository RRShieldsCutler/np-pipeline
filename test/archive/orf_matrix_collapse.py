#!/usr/bin/env Python

import argparse
import sys
import numpy as np
import pandas as pd
import re
import warnings
import csv
from collections import defaultdict
from ninja_utils.parsers import FASTA
from ninja_utils.utils import find_between
#from blastp_to_matrix import build_cluster_map

# >ncbi_tid|206672|ref|NC_004307.2_cluster004_ctg1_orf02030|organism|Bifidobacterium_longum|
# The arg parser
def make_arg_parser():
	parser = argparse.ArgumentParser(description='Build a dictionary to store the list of ORFs for clusters in each genome')
	parser.add_argument('-i', '--input', help='Input is the matrix csv.', default='-')
	parser.add_argument('-m', '--mpfa', help='Input is a multi-cluster FASTA file.', required=True)
	parser.add_argument('-b', '--bread', help='Where to find the header for the sequence (default="ref|,|")', default='ref|,|')
	parser.add_argument('-o', '--output', help='Where to save the output csv; default to screen', required=False, default='-')
	return parser

# define the dictionary function
# def build_cluster_map(inf, bread='ref|,|'):
# 	begin,end = bread.split(',')
# 	cluster_map = defaultdict(set)
# 	fasta_gen = FASTA(inf)
# 	for header, sequence in fasta_gen.read():
# 		if '.cluster' in header:
# 			header = header.replace('.cluster','_cluster')
# 		ref = find_between(header, begin, end)
# 		header_split = ref.split('_')
# 		key = '_'.join(header_split[:3])
# 		value = header_split[-1]
# 		cluster_map[key].add(value)
# 	return cluster_map


# def cluster_by_cluster():
# 	with open(args.mpfa, 'r') if args.mpfa != '-' else sys.stdin as inf:
# 		cluster_map = build_cluster_map(inf, bread=args.bread)
# 		print(list(cluster_map.keys()))



def main():
	parser = make_arg_parser()
	args = parser.parse_args()

	bread = args.bread
	inf = open(args.mpfa, 'r')
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
# 	return cluster_map

	incsv = open(args.input, 'r')
	mx = pd.read_csv(incsv, sep=',', header=0, index_col=0)
	j = mx.shape[1]
	i = mx.shape[0]
	collapse = pd.DataFrame()
	cluster_keys = list(cluster_map.keys())
	cluster_score = defaultdict(dict)
# 	print(cluster_keys)
	y=0
	for cluster in cluster_keys:
# 			p = re.compile(r'(\w+_[\w+\d+]*\.\d)(_\w+\d\d\d)(_ctg\d_orf\d+)')
# 			m = p.search(cluster)
# 			print(cluster)
# 			cluster_id = ''.join(m.group(1, 2))
		y += 1
		mx_csub = mx.filter(like=cluster)
		a = []
		rowind = []
# 		print('-'.join([cluster,'COLUMN',str(y)]))
		for cluster2 in cluster_keys:
			mx_dubsub = mx_csub.filter(like=cluster2, axis=0)
			cc_mean = np.nanmean(mx_dubsub.values.flatten(), dtype='float64')
# 			print(cc_mean)
# 			a.append(cc_mean)
			cluster_score[cluster][cluster2] = cc_mean
	print(list(cluster_score.keys()))
	print(list(cluster_score.values()))
	score_mean = pd.DataFrame.from_dict(cluster_score, orient='columns', dtype=float)
	#score_mean = pd.DataFrame(score_mean.values, index=cluster_keys, columns=score_mean.columns)
	score_mean.sort_index(axis=0)
	score_mean.sort_index(axis=1)
	# Check if a matrix is symmetric
	# arr = df.values
	# print((arr.transpose() == -arr).all())
	if args.output == '-':
		print(score_mean)
	else:
		score_mean.to_csv(args.output)

# 	return collapse
# 	print(mx_csub[1,1])

	# parse command line
# 	with open(args.mpfa, 'r') if args.mpfa != '-' else sys.stdin as inf:
# 		cluster_map = build_cluster_map(inf, bread=args.bread)
# 		# how many clusters there are
# 		# print(len(list(cluster_map.keys())))
# 		print(list(cluster_map.keys()))
# 		# how many ORFs per cluster for all clusters
# 		# print([len(value) for value in cluster_map.values()])
# 		# list all ORFs in a particular cluster
# 		# print(cluster_map['NC_000000.0_cluster000])
# 		# how many ORFs in a particular cluster
# 		# print(len(cluster_map['NC_000000.0_cluster000]))
# 	with open(args.mpfa, 'r') if args.mpfa != '-' else sys.stdin as inf:
# 		cluster_map = build_cluster_map(inf, bread=args.bread)

if __name__ == '__main__':
	with warnings.catch_warnings():
		warnings.filterwarnings('ignore', r'Mean of empty slice')
		main()

