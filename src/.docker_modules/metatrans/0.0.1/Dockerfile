FROM lbmc/r-base:3.6.2

## copy files
COPY install_packages.R /usr/bin/

RUN chmod +x /usr/bin/*.R &&\
Rscript /usr/bin/install_packages.R  ## install R-packages

COPY install_packages2.R /usr/bin/

RUN Rscript /usr/bin/install_packages2.R

RUN apk add  --update --no-cache bash \
  && apk add openjdk7-jre-base

RUN  wget https://drive5.com/downloads/usearch5.2.236_i86osx32.gz \
    && gunzip usearch5.2.236_i86osx32.gz \
    && chmod +x ./usearch5.2.236_i86osx32 \
    && ln -s ./usearch5.2.236_i86osx32 usearch \
    && dir=$(pwd) \
    && export PATH=$dir/usearch:$PATH

RUN apk add gawk \
    && apk add --no-cache dash


CMD ["bash"]
