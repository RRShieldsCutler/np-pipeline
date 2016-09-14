#!/usr/bin/env Rscript

library(dplyr)
library(tidyr)
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied (blastp results input file)", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "trimmed_results.txt"
}
blastout = read.delim(args[1], header=FALSE) # reads file which has no header yet
# blastout = read.delim("GCF_001281305_result.txt", header=FALSE)
colnames(blastout) = c('query','subject','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore')
blastout = blastout %>% separate(query, c("query_id", "query_orf"), "_ctg1_") # splits 
blastout[1] = lapply(blastout[1], gsub, pattern = ".clu", replacement = "_clu", fixed=TRUE)
blastout = filter(blastout, as.character(query_id) != as.character(subject))
blastout$query = paste(blastout$query_id,blastout$query_orf,sep="_")
blastout = blastout %>% select(-query_id,-query_orf)
blastout = blastout %>% select(query, everything())
write.table(blastout, file=args[2], quote=FALSE, sep='\t', row.names=FALSE)
# write.table(blastout, file="result3.txt", quote=FALSE, sep='\t', row.names=FALSE)

