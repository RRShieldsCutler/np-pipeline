#!/usr/bin/env python

# extract_gbkcluster_seq.py - version 1.0
# Extract the DNA sequence from the *.gbk output files of antiSMASH
# and return a txt file with only the concatenated sequence.

usage = 'python extract_gbkcluster_seq.py *.gbk'

import sys
import os
# import shutil
import os.path
# make folder within current dir to store new txt files
# if "cluster_sequences" not in os.listdir("."):
# 	os.mkdir("cluster_sequences")
	
def main():
	if len(sys.argv)<1: #only run if there are actually files that match
		print(usage)
		pass
	else:
		FileList= sys.argv[1:]
		Header = '>cluster sequence from '
		#define the start of the sequence by the ORIGIN line
		seqstart = 'ORIGIN'
		sequence_begin = False
		FileNum=0
		# work through each file called by the command line
		for InfileName in FileList:
			if InfileName.endswith('final.gbk'):
				pass
			elif InfileName.endswith('.gbk'): #double check to only convert the right files
				if "cluster_sequences" not in os.listdir("."):
					os.mkdir("cluster_sequences")
				FileNum += 1 #keep track of the number of cluster files converted
				HeaderF = Header + InfileName
				OutFileName = 'seq_' + InfileName + '.txt'
				OutFileName = OutFileName.replace('.gbk','')
				OutFile = open(os.path.join('cluster_sequences', OutFileName),'w')
				OutFile.write(HeaderF + '\n') #use the filename to ID the file on the first line
				Infile = open(InfileName, 'r')
				for line in Infile:
					if sequence_begin: #only do this if ORIGIN starts the line
						#joins together only the characters on the line in the set atcg
						OutFile.write(''.join([ch for ch in line if ch in set(('a','t','c','g'))]))
					elif line.startswith('ORIGIN'):
						sequence_begin = True #identifies the line starting with ORIGIN as sequence start
			else:
				print(usage)
				Infile.close()
				OutFile.close()
##this section below not needed after fixing the os.path.join function above
	# after each file is processed in the current working dir,
	# move all the new files into the cluster_sequences folder
# 	for newfile in os.listdir('.'):
# 		if newfile.startswith('seq_'):
# 			shutil.move(newfile, os.path.join('cluster_sequences'))
	
	# print to screen the number of files converted
# 	sys.stderr.write("Converted %d file(s)\n" % FileNum)
		
if __name__ == '__main__':
	main()
