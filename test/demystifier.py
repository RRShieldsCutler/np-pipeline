#!/usr/bin/env python
import argparse
import sys
import os

from ninja_utils.parsers import FASTA
from ninja_dojo.database import RefSeqDatabase
from ninja_dojo.taxonomy import NCBITree

# The arg parser for this wrapper
def make_arg_parser():
	parser = argparse.ArgumentParser(description='Given one NCBI accession format, provide the NCBI tid  and organism')
	parser.add_argument('-a', '--assembly', help='Input is a GCF', default='-')
	parser.add_argument('-r', '--refseq', help='Input is the RefSeq Accession ID', default='-')
	parser.add_argument('-t', '--tid', help='Input is the ncbi tid', default='-')
	parser.add_argument('-o', '--output', help='If nothing is given, then stdout, else write to file', default='-')
	parser.add_argument('-v', '--verbose', help='Print extra statistics', action='store_true', default=False)
	return parser

usage = 'gcf_demystifier.py -i GCF_XXXXXXXXXX.X [-o] OUTPUT_FILE [-v]'

def main():
	parser = make_arg_parser()
	args = parser.parse_args()

	db = RefSeqDatabase()
	nt = NCBITree()
	# parse command line
	with open(args.output, 'w') if args.output != '-' else sys.stdout as outf:
		if args.assembly != '-':
			ncbi_tid = db.get_ncbi_tid_from_assembly_accession_version(args.assembly)[0]
		elif args.refseq != '-':
			ncbi_tid = db.get_ncbi_tid_from_refseq_accession(args.refseq)[0]
		elif args.tid != '-':
			ncbi_tid = int(args.tid)
		organism = nt.green_genes_lineage(ncbi_tid)
# 		genus_species = organism.split(';')[-1]
# 		genus_species = genus_species.replace('s__','')
		outf.write('>ncbi_tid|%d|organism|%s\n' % (ncbi_tid, organism))
		outf.write('\n')

if __name__ == '__main__':
    main()
