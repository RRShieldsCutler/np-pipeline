#!/usr/bin/env python
#####################################
## By Robin Shields-Cutler ##
## Why is this useful? When you run SHOGUN,
## you will get rows labeled with k__[kingdom];p__[phylum];...etc. If you want to
## compare at a certain level of taxonomy, it's convenient to collapse the table
## down and summarize the counts at a given depth, or level. This script does that
## for a given level (1 = Kingdom, 2 = Phylum, etc down to 7 = species). It is similar
## to the "summarize_taxa" script in QIIME, but that script won't run on Shogun's output
## taxon_counts. So use this.
##
## So if you had 5 counts of E.coli UTI89 and 10 of E.coli MG1655, this script
## would summarize to E.coli with 15 counts. It's quick and easy, and works
## on the taxon_table.csv files fresh outta Shogun.
##
## You could also use as a template if you need to collapse further down. Also
## check out the summarize_taxa.py script in qiime if you have fancier needs.
##
## Pro tip: run this bash command to do all levels:
##
## for l in $(seq 1 1 7); do summarize_shogun_taxa.py -i taxon_counts.csv -o summarized_taxon_counts_L${l}.csv -L $l; done
##


import argparse
import sys
import os
import csv
import pandas as pd


# The arg parser for this wrapper
def make_arg_parser():
	parser = argparse.ArgumentParser(description='Collapse the SHOGUN output taxon_table.csv to a specified taxonomic level:\nsummarize_shogun_taxa.py -i [taxon_table.csv] -o [output] -L [1-7]. Make sure your file is in the correct format: Column 1 = organisms (no header label, no spaces!), Columns 2+ = samples with counts, header = sample name')
	parser.add_argument('-i', '--input', help='Input is a CSV taxon_table from SHOGUN', default='-')
	parser.add_argument('-o', '--output', help='If nothing is given, then stdout, otherwise write to a specified CSV output file', default='-')
	parser.add_argument('-L', '--level', help='Specify the level at which to collapse: 1 = Kingdom; 2 = Phylum; 3 = Class; 4 = Order; 5 = Family; 6 = Genus; 7 = Species', required=True)
	return parser


def to_species(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';t__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def to_genus(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';s__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def to_family(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';g__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def to_order(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';f__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def to_class(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';o__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def to_phylum(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';c__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def to_kingdom(inf):
	df = pd.read_csv(inf, header=0)
	df_s = df.iloc[:,0].apply(lambda x: pd.Series(str(x).split(';p__')))
	df_s.drop([1], axis=1, inplace=True)
	df_counts = df.drop('Unnamed: 0', axis=1)
	df_full = df_s.join(df_counts)
	return df_full


def merge_strains(inf2, inf, level):
	df = pd.read_csv(inf2, header=0, index_col=1)
	odf = pd.read_csv(inf, header=0, index_col=0)
	df = df.drop('Unnamed: 0', axis=1)
	samples = list(df.columns)
	odf_ind = list(odf.index)
	odf_newind = []

	if level == 6:
		for tax in odf_ind:
			str(tax)
			if ';g__;' in tax:
				tax = tax.replace('g__;', 'g__None;')
			else:
				pass
			odf_newind.append(tax)

	elif level == 5:
		for tax in odf_ind:
			str(tax)
			if ';f__;' in tax:
				tax = tax.replace('f__;', 'f__None;')
			else:
				pass
			odf_newind.append(tax)

	elif level == 4:
		for tax in odf_ind:
			str(tax)
			if ';o__;' in tax:
				tax = tax.replace('o__;', 'o__None;')
			else:
				pass
			odf_newind.append(tax)

	elif level == 3:
		for tax in odf_ind:
			str(tax)
			if ';c__;' in tax:
				tax = tax.replace('c__;', 'c__None;')
			else:
				pass
			odf_newind.append(tax)
			
	elif level == 2:
		for tax in odf_ind:
			str(tax)
			if ';p__;' in tax:
				tax = tax.replace('p__;', 'p__None;')
			else:
				pass
			odf_newind.append(tax)

	elif level == 1:
		for tax in odf_ind:
			str(tax)
			if 'k__;' in tax:
				tax = tax.replace('k__;', 'k__None;')
			else:
				pass
			odf_newind.append(tax)

	else:
		pass
	if odf_newind:
		odf.index = odf_newind
	orgs = list(df.index)
	n_orgs = []
	for org in orgs:
		if org.endswith('__'):
			org = ''.join([org, 'None'])
		n_orgs.append(org)
	df.index = n_orgs
	u_orgs = list(set(n_orgs))
# 	DEBUG:
# 	print(u_orgs)
	finaldf = pd.DataFrame(index=samples)
	for bug in u_orgs:
		n = []
		bug = str(bug)
		subdf = odf.filter(like=bug, axis=0)
		sumcounts = pd.DataFrame(subdf.sum(axis=0))
		n.append(bug)
# 		DEBUG:
# 		print(n)
		sumcounts.columns = n
		finaldf = finaldf.join(sumcounts)
	finaldf = finaldf.T
	return finaldf


def main():
	parser = make_arg_parser()
	args = parser.parse_args()
	# parse command line
	with open(args.input, 'r') if args.input != '-' else sys.stdin as infcheck:
		havespace = csv.reader(infcheck, delimiter='\t')
		for i, row in enumerate(havespace):
			if i == 2:
				name_style = row[0]
				if '; p__' in name_style:
					print('\nPlease remove spaces (find and replace) from taxonomy names before running this script.\n\nYou should also make sure column 1 has organisms names and no header label.\nColumns 2+ should be labeled with the sample name in the header row, and then contain counts (or other numbers)\n')
					sys.exit()
	with open(args.input, 'r') if args.input != '-' else sys.stdin as inf:
	# Run the appropriate function for the specified level
		level = int(args.level)
		if level == 7:
			with open('temp.csv', 'w') as outf:
				df_full = to_species(inf)
				df_full.to_csv(outf)

		elif level == 6:
			with open('temp.csv', 'w') as outf:
				df_full = to_genus(inf)
				df_full.to_csv(outf)

		elif level == 5:
			with open('temp.csv', 'w') as outf:
				df_full = to_family(inf)
				df_full.to_csv(outf)

		elif level == 4:
			with open('temp.csv', 'w') as outf:
				df_full = to_order(inf)
				df_full.to_csv(outf)

		elif level == 3:
			with open('temp.csv', 'w') as outf:
				df_full = to_class(inf)
				df_full.to_csv(outf)

		elif level == 2:
			with open('temp.csv', 'w') as outf:
				df_full = to_phylum(inf)
				df_full.to_csv(outf)

		elif level == 1:
			with open('temp.csv', 'w') as outf:
				df_full = to_kingdom(inf)
				df_full.to_csv(outf)

		else:
			print('\nMust specify an appropriate taxonomic level, 1-7. Try again.')
			sys.exit()

	# Write the output file
	with open(args.output, 'w') if args.output != '-' else sys.stdout as outf2:
		with open('temp.csv', 'r') as inf2:
			with open(args.input,'r') as inf:
				final_df = merge_strains(inf2, inf, level)
				final_df.to_csv(outf2)
	print('\nDone working, cleaning up...\n')
	os.remove('temp.csv')

if __name__ == '__main__':
	main()