FROM continuumio/miniconda3

LABEL version=0.6.1.dev0
ARG XCUBE_VERSION=0.6.0
LABEL name=xcube
LABEL maintainer=helge.dzierzon@brockmann-consult.de

SHELL ["/bin/bash", "-c"]

RUN git clone https://github.com/dcs4cop/xcube /xcube
WORKDIR /xcube
RUN conda env update -n base
RUN source activate base && conda install -c conda-forge oauthlib requests_oauthlib
RUN source activate base && python setup.py install

RUN git clone https://github.com/dcs4cop/xcube-sh /xcube-sh
WORKDIR /xcube-sh
RUN git checkout dzelge_dask_distributed_not_working
RUN source activate base && python setup.py install
