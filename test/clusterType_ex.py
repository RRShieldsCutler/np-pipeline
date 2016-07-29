#!/usr/bin/env python
import os
import pandas as pd

for file in os.listdir('txt'):
	if file.endswith('_BGC.txt'):
		BGCt = pd.read_csv(os.path.join('txt',file),delimiter='\t',header=0,usecols=[0,1,3])
		BGCtablename = "abbrev_" + file
		BGCof = open(os.path.join('cluster_sequences',BGCtablename),'w')
		BGCof.write(' ')
		BGCof.close()
		BGCt.to_csv(os.path.join('cluster_sequences', BGCtablename),sep='\t',index=False)