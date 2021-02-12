FROM python:2.7-alpine

RUN  apk --update add --virtual scipy-runtime python py-pip \
    && apk add --virtual scipy-build \
        build-base python-dev openblas-dev freetype-dev pkgconfig gfortran \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install --upgrade pip \
    && pip install --no-cache-dir scipy \
    && apk del scipy-build \
    && apk add --virtual scipy-runtime \
        freetype libgfortran libgcc libpng  libstdc++ musl openblas tcl tk \
    && rm -rf /var/cache/apk/*

RUN apk --update add --no-cache g++ make cmake zlib-dev \
    && apk add bash hdf5-dev hdf5-static --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

RUN  apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && pip install --upgrade Pillow \
    && pip install GroopM


RUN apk --upgrade add git autoconf automake make m4 libtool \
  && git clone https://github.com/Ecogenomics/BamM.git \
  && cd BamM/c \
  && cd ./libcfu-0.03 \
  && ./autogen.sh \
  && ./configure \
  && make \
  && make install \
  && make clean \
  && cd ../htslib-1.3.1 \
  && ./configure \
  &&  make \
  &&  make install \
  && cd ..

RUN git clone https://github.com/lh3/bwa.git \
  && cd bwa/ \
  && make \
  && cp bwa /usr/bin/ \
  && make clean \
  && cd ..

RUN cd BamM/c \
    && apk add --update curl curl-dev \
    && git clone https://github.com/samtools/htslib.git \
    && cd htslib/ \
    && apk add --upgrade zlib zlib-dev bzip2 bzip2-dev  \
    && rm -rf /var/cache/apk/* \
    && git submodule update --init --recursive \
    && autoheader \
    && autoconf \
    && ./configure --disable-lzma \
      && make \
    && make install \
    && cd .. \
    && git clone https://github.com/samtools/samtools.git \
    && cd samtools \
    && apk add --upgrade ncurses-libs ncurses-dev \
    && autoheader  \
    && autoconf -Wno-syntax  \
    && ./configure  \
    && make \
    && make install

RUN apk add --no-cache libbsd-dev gcc \
    && cd BamM \
    && python setup.py install \
    --with-libcfu-inc c/libcfu/src/ \
    --with-libhts-inc c/htslib/htslib
