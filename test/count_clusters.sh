#!/bin/bash

for DIR in GCF*; do
	ls -l $DIR/cluster_sequences/seq* | wc -l
done