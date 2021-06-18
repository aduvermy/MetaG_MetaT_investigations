library(tidyverse)
library(DESeq2)
library(gridExtra)


### READS PER PROTEIN
##load design table
design<- read_tsv("~/Haruko_takeyama_lab/TPM/design.csv" , col_names  =TRUE )
design


dtf <-  design$path %>%
  set_names(design$sample) %>%
  map_dfr(~ read_tsv(. , col_names = c("prot","counts")), .id = "Run", path=sampleInfo$Run)

#table_counts <- as.data.frame(table(dtf$prot))
#good_prot <- table_counts[table_counts$Freq == 6,]


#dtf <- dtf[dtf$prot %in% good_prot$Var1,]

##convert dtf 2 matrix
dtf2matrix <- function(dtf){ ##convert dataframe 2 matrix
  matrice<-reshape2::dcast(dtf, prot ~ Run, value.var= "counts")
  rownames(matrice) <- matrice$prot
  matrice <- matrice[, -1] ##suppr colonne GeneID
  matrice <- matrice %>% replace(is.na(.), 0)
  return(matrice)
}

matrice <- dtf %>% dtf2matrix()
matrice

matrix2deseq <- function(matrice, sampleInfo){
  DESeqDataSetFromMatrix (countData = matrice,
                          colData = sampleInfo ,
                          design = ~condition)
}


getDESeq <- function(mat, design_exp){
  print('Convert matrice 2 Deseq object')
  fun <- function(x){
    return(x+1)
  }
  matrice <- mat %>% mutate_all(fun) 
  rownames(matrice) <- rownames(mat)
  ds <- matrix2deseq(matrice,design_exp)
  ds <- estimateSizeFactors(ds)
  return(ds)
}

design
matrice

deseq_obj<- getDESeq(matrice, design)

deseq_obj 
#res_tableOE_unshrunken <- results(deseq_obj, alpha = 0.05)
dds<-DESeq(deseq_obj)
resultsNames(dds) # lists the coefficients
res <- results(dds, name="condition_HIGH_vs_AMBIANT")
# or to shrink log fold changes association with condition:
#BiocManager::install('ashr')
#contrast_oe <- c("sampletype", "MOV10_overexpression", "control")
res_tableOE <- lfcShrink(dds, res=res, type= 'ashr')
plotMA(res, ylim=c(-2,2))


match('UniRef90_A0A2B4RHS0',rownames(res_tableOE %>% data.frame()%>% filter(padj < 0.05)))
res_tableOE %>% data.frame() %>% filter(rownames(.)== "UniRef90_A0A2B4RHS0")
matrice_padj<- matrice %>% filter(rownames(.) %in% rownames(res_tableOE %>% data.frame() %>% filter(padj < 0.01)))
deseq_obj <- getDESeq(matrice_padj, design)
dta <- varianceStabilizingTransformation(deseq_obj, blind = FALSE)
P <- plotPCA(dta, intgroup= c("condition")) #+ geom_point(aes(text = paste("Run:", colnames(dta))))
nudge <- position_nudge(y = 1)
P 


P1<- P + scale_color_manual(values=c("AMBIANT"= "blue", "HIGH"= "red"))  + geom_text(aes(label = name), position = nudge)
P1

ggsave(file="~/Haruko_takeyama_lab/fig/ACP_reads_per_prot_padj.svg", plot=P1, width=7, height=4)


write.table(matrice_padj, "Haruko_takeyama_lab/TPM/res/matrice_candidats.tsv", sep='\t',row.names = TRUE)
write.table(res_tableOE %>% data.frame() %>% filter(padj < 0.01), "Haruko_takeyama_lab/TPM/res/results_analysis_diff_candidats.tsv", sep = '\t', row.names = TRUE)

