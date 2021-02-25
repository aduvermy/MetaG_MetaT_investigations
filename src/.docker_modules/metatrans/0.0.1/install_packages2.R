#!/usr/bin/env Rscript

install.packages("shortReads", repos = "http://cran.us.r-project.org")
BiocManager::install("GenomicRanges")
BiocManager::install("IRanges")
install.packages("DESeq2", repos = "http://cran.us.r-project.org")
