library(tidyverse)


dta = read_tsv("Haruko_takeyama_lab/res_assembly_CAMI.csv" ,col_names  =TRUE)
data_complexity = factor(dta$complexity, levels = c("low","medium","high"))
p <- ggplot(data = dta, aes(x = data_complexity, y = value, fill = pipeline)) +
  geom_bar(stat = "identity", position='dodge') + facet_wrap(~metrics, scales = "free_y")


png(file="hist_slide_reu_jap.png", width = 1000, height = 500)
p +  theme(axis.text.x = element_text(angle = 60, vjust = 1, hjust = 1, size=25),
           axis.title.x = element_blank(),
           axis.title.y = element_blank(),
           legend.text = element_text(size= 17),
           legend.spacing.x = unit(0.5, 'cm'),
           legend.title=element_blank(),
           legend.key.size = unit(3, 'lines'),
           strip.text.x = element_text(size = 20))
dev.off()

