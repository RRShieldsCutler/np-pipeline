library(dplyr)
library(ggplot2)
install.packages('ggdendro')
library(ggdendro)
library(ape)

df = read.csv('47refset_bitscore_combine.csv', header = TRUE, row.names = 1)
df[is.na(df)] = 0
disdf = dist(df)
hcl = hclust(disdf)
hcl = hclust(dist(df))
par(cex=0.2, pin=c(10.5,8), mar=c(4,5,4,3)+1)
plot(hcl, hang=-1, xlab = '', ylab = '', sub = '', main = '', axes=FALSE, ylim=c(0,4000))
par(cex=1)
title(xlab = 'BGC', ylab = 'distance', sub = '', main = 'bitscore-based hierarchically clustered clusters')
axis(2)

hgrp = cutree(hcl, h=500)
names(hgrp) = colnames(df)
cluster_df = data.frame(BGC=names(hgrp), cluster_ID=hgrp, row.names=NULL)
arrange(cluster_df, cluster_ID)
cluster_df

pdf(file = 'Hclust_47refset_bitscore.pdf', width = 2000, height = 2000)
mypalette = c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
op = par(bg = "#CCCCCC")
plot(as.phylo(hcl), type = "fan", cex = 1, tip.color=mypalette[hgrp])
dev.off()



"cluster.by.threshold" <- function(d, threshold=.5){
  hc <- hclust(d)
  res <- cutree(hc,h=1-threshold)
  names(res) <- colnames(x)
  return(res)
}

dg = as.dendrogram(hcl)
p = ggdendrogram(hcl, rotate = TRUE, size = 1) + coord_flip()
p = p + theme(axis.text.x = element_text(size = rel(1))) + theme(axis.text.y = element_text(size = rel(0.1)))
p

ddata <- dendro_data(hcl, type = "triangle")
p = ggplot(segment(ddata)) + geom_segment(aes(x=x, y=y, xend = xend, yend = yend)) + coord_flip() + 
scale_y_reverse(expand = c(0.2, 0)) + theme_dendro()
p

ggsave("47_bitscore_dendro.png", width=5, height=15, dpi = 1200)

source("http://addictedtor.free.fr/packages/A2R/lastVersion/R/code.R")
op = par(bg = "#EFEFEF")
A2Rplot(hcl, k = 352, boxes = FALSE, lty.up = 1, col.up = "gray50", col.down = rainbow(352), show.labels = FALSE)
?rainbow


