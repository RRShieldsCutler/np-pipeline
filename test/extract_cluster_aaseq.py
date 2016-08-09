#!/usr/bin/env python

# extract_cluster_aaseq.py - version 1.0
# Extract the amino acid sequence from the ***** output files of antiSMASH
# and return a txt file with only the concatenated sequence.

usage = 'python extract_cluster_aaseq.py *.gbk'

import sys
import os
import os.path
import re
	
def main():
	if len(sys.argv)<1: #only run if there are actually files that match
		print(usage)
		pass
	else:
		FileList= sys.argv[1:]
		Header = '>'
		#define the start of the sequence by the ORIGIN line
		aastart = 'CDS'
		sequence_begin = False
		FileNum=0
		# work through each file called by the command line
		for InfileName in FileList:
			if InfileName.endswith('final.gbk'):
				pass
			elif InfileName.endswith('.gbk'): #double check to only convert the right files
				FileNum += 1 #keep track of the number of cluster files converted
				if "cluster_aa_sequences" not in os.listdir("."):
					os.mkdir("cluster_aa_sequences")
				HeaderF = Header + InfileName.replace('.gbk','')
				OutFileName = 'aa_' + InfileName + '.txt'
				OutFileName = OutFileName.replace('.gbk','')
				OutFile = open(os.path.join('cluster_aa_sequences', OutFileName),'w')
				Infile = open(InfileName, 'r')
				for line in Infile:
					if sequence_begin: #only do this if CDS starts the line
						if line.startswith("                     /locus_tag"):
							p = re.compile(r"^(\s+)(/locus_tag=)\"(ctg)(\d_\w+)\"")
							m = p.search(line) # searches using the regex defined above
							OutfileM = ''.join(m.group(3,4))
							OutFile.write('\n' + HeaderF + '_') #use the filename to ID the file on the first line
							OutFile.write(OutfileM + '\n')
						if line.startswith('                     /translation'):
# 							OutFile.write(''.join([ch for ch in line if ch in set(('G,A,L,M,F,W,K,Q,E,S,P,V,I,C,Y,H,R,N,D,T'))]))
							aa_p = re.compile(r"^(\s+)(\/translation\=\")([A-Z]+)")
							aa_m = aa_p.search(line) # searches using the regex defined above
							Outaa = aa_m.group(3)
							OutFile.write(Outaa)
						if line.startswith('                     '):
							if line.startswith('                     /note="Glimmer'):
								pass
							else:
								OutFile.write(''.join([ch for ch in line if ch in set(('G,A,L,M,F,W,K,Q,E,S,P,V,I,C,Y,H,R,N,D,T'))]))

						else:
							if line.startswith('     CDS'):
								sequence_begin = True
							else:
								sequence_begin = False
					elif line.startswith('     CDS'):
						sequence_begin = True #identifies the line starting with ORIGIN as sequence start
			else:
				print(usage)
				Infile.close()
				OutFile.close()

	# print to screen the number of files converted
# 	sys.stderr.write("Converted %d file(s)\n" % FileNum)
		
if __name__ == '__main__':
	main()
