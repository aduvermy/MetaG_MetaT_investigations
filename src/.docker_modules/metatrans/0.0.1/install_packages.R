#!/usr/bin/env Rscript


##install_packages for docker image

install.packages("R.utils",repos = "http://cran.us.r-project.org")
install.packages("RColorBrewer",repos = "http://cran.us.r-project.org")
install.packages("gplots",repos = "http://cran.us.r-project.org")
install.packages("ggplot2",repos = "http://cran.us.r-project.org")

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager",repos = "http://cran.us.r-project.org")
