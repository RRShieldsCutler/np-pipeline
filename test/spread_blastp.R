#!/usr/bin/env Rscript

## Create a matrix form of the blastp results, with bitscore chosen here.
## To normalize the bitscores, run this through the python script blastp_to_matrix with the -j flag

library(dplyr)
library(tidyr)

args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("input file must be supplied (blastp table output, tsv file)", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "bitscore_output.csv"
}

# setwd('/Users/Robin/Box\ Sync/knights_box/np-pipeline/data/blastp_tests/2016-08-24_blastp_tests/')
longdf = read.delim(args[1], sep = '\t', header = FALSE)
bitscore = c('V1', 'V2', 'V12')
longbit = longdf[bitscore]
widebit = spread(longbit, V2, V12)
write.csv(widebit, file = args[2], quote = FALSE, row.names = FALSE, na = '')

