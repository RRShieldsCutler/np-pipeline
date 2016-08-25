#!/usr/bin/env Rscript

library(dplyr)
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied (blastp results input file)", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "trimmed_results.txt"
}
blastout = read.delim(args[1], header=FALSE)
colnames(blastout) = c('query','subject','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore')
blastout = filter(blastout, as.character(query) != as.character(subject)) # removes self-self match rows
# blastout = filter(blastout, bitscore > 50)
write.table(blastout, file=args[2], quote=FALSE, sep='\t', row.names=FALSE)
