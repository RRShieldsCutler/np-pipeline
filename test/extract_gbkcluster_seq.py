#!/usr/bin/env python

Usage = """
ExtractSeqs2.py - version 1.0
Extract the DNA sequence from the *.gbk output files of antiSMASH
and return a txt file with only the concatenated sequence.
Usage:
  ExtractSeq3.py *.gbk
"""
usage = 'ExtractSeqs3.py *.gbk ===== extract sequence from each gbk file'

import sys
import os
import shutil
import os.path
# make folder within current dir to store new txt files
if "cluster_sequences" not in os.listdir("."):
	os.mkdir("cluster_sequences")
	
def main():
	if len(sys.argv)<1: #only run if there are actually files that match
		print Usage	
	else:
		FileList= sys.argv[1:]
		Header = 'cluster sequence from '
		#define the start of the sequence by the ORIGIN line
		seqstart = 'ORIGIN'
		sequence_begin = False
		FileNum=0
		# work through each file called by the command line
		for InfileName in FileList:
			if InfileName.endswith('final.gbk'):
				pass
			elif InfileName.endswith('.gbk'): #double check to only convert the right files
				FileNum += 1 #keep track of the number of cluster files converted
				HeaderF = Header + InfileName
				OutFileName = 'sequence_' + InfileName + '.txt'
				OutFile = open(OutFileName,'w')
				OutFile.write(HeaderF + '\n') #use the filename to ID the file on the first line
				Infile = open(InfileName, 'r')

				for line in Infile:
					if sequence_begin: #only do this if ORIGIN starts the line
						#joins together only the characters on the line in the set atcg
						OutFile.write(''.join([ch for ch in line if ch in set(('a','t','c','g'))]))
					elif line.startswith('ORIGIN'):
						sequence_begin = True #identifies the line starting with ORIGIN as sequence start
			else:
				print usage
			Infile.close()
			OutFile.close()
	# after each file is processed in the current working dir,
	# move all the new files into the cluster_sequences folder
	for newfile in os.listdir('.'):
		if newfile.startswith('sequence'):
			shutil.move(newfile, os.path.join('cluster_sequences'))
	# print to screen the number of files converted
	sys.stderr.write("Converted %d file(s)\n" % FileNum)
	
	
if __name__ == '__main__':
	main()
