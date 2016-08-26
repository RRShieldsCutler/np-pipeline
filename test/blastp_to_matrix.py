#!/usr/bin/env python
#
# Robin Shields-Cutler
# August 2016
# takes standard blast output TSV (outfmt 6-- *.b6 or *.txt, etc) and stores entries in dictionary,
# then writes to dataframe and exports as CSV

usage='blastp_to_matrix.py -i BLASTOUT.b6 -s SCORE_METHOD -t THRESHOLD -o OUTFILE.csv'

import argparse
import os
import csv
import pandas as pd
import numpy as np
import re
from collections import defaultdict


def make_arg_parser():
	parser = argparse.ArgumentParser(description='Get least common ancestor for alignments in unsorted BAM/SAM file')
	parser.add_argument('-i', '--input', help='The blast output file to process.', required=True, type=str)
	parser.add_argument('-s', '--score', help='Which score to enter into matrix: "pident", "evalue", or "bitscore"', required=False, type=str, default='bitscore')
	parser.add_argument('-t', '--threshold', help='The threshold (float) for entry into matrix.', required=False, type=float, default=1)
	parser.add_argument('-o', '--output', help='Where to put the output CSV', required=True, type=str)
	return parser

def main():
	parser = make_arg_parser()
	args = parser.parse_args()

	sparse_blast_id_dict = defaultdict(dict)
	with open(args.input) as blast_inf:
# 		next(blast_inf)
		blast_tsv = csv.reader(blast_inf, delimiter='\t')
	# line[0] qname, line[1] = rname, line[2] = %match, line[10] = evalue, line[11] = bitscore
		if args.score == 'bitscore':
			for line in blast_tsv:
				p = re.compile(r'(\w+\_(\w+\d+)*\.\d)')
				m = p.search(line[0])
				n = p.search(line[1])
				mref = m.group(1)
				nref = n.group(1)
				if mref == nref:
					pass
				else:
					bvalue = np.float(line[11])
					if bvalue > args.threshold:
						sparse_blast_id_dict[line[0]][line[1]] = bvalue
		elif args.score == 'evalue':
			for line in blast_tsv:
				p = re.compile(r'(\w+\_(\w+\d+)*\.\d)')
				m = p.search(line[0])
				n = p.search(line[1])
				mref = m.group(1)
				nref = n.group(1)
				if mref == nref:
					pass
				else:
					evalue = np.float(line[10])
					if evalue < args.threshold:
						sparse_blast_id_dict[line[0]][line[1]] = evalue
		elif args.score == 'pident':
			for line in blast_tsv:
				p = re.compile(r'(\w+\_(\w+\d+)*\.\d)')
				m = p.search(line[0])
				n = p.search(line[1])
				mref = m.group(1)
				nref = n.group(1)
				if mref == nref:
					pass
				else:
					ivalue = np.float(line[2])
					if ivalue > args.threshold:
						sparse_blast_id_dict[line[0]][line[1]] = ivalue

	df = pd.DataFrame.from_dict(sparse_blast_id_dict)
	df.sort_index(axis=0)
	df.sort_index(axis=1)
	# Check if a matrix is symmetric
	# arr = df.values
	# print((arr.transpose() == -arr).all())
	df.to_csv(args.output)


if __name__ == '__main__':
	main()
