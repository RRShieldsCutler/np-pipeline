#!/usr/bin/env python

import argparse
import os
import csv
import pandas as pd
import numpy as np
from collections import defaultdict


def make_arg_parser():
	parser = argparse.ArgumentParser(description='Get least common ancestor for alignments in unsorted BAM/SAM file')
	parser.add_argument('-i', '--input', help='The blast output file to process.', required=True, type=str)
	parser.add_argument('-o', '--output', help='Where to put the output CSV', required=True, type=str)
	return parser

def main():
	parser = make_arg_parser()
	args = parser.parse_args()

	sparse_blast_id_dict = defaultdict(dict)
	with open(args.input) as blast_inf:
		next(blast_inf)
		blast_tsv = csv.reader(blast_inf, delimiter='\t')
		for line in blast_tsv:
			# line[0] qname, line[1] = rname, line[2] = %match
			sparse_blast_id_dict[line[0]][line[1]] = np.float(line[2])

	df = pd.DataFrame.from_dict(sparse_blast_id_dict)
	df.sort_index(axis=0)
	df.sort_index(axis=1)
	# Check if a matrix is symmetric
	# arr = df.values
	# print((arr.transpose() == -arr).all())
	df.to_csv(args.output)


if __name__ == '__main__':
	main()
