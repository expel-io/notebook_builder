FROM centos:centos7

ENV LANG=en_US.UTF-8

WORKDIR /app

COPY . /app

RUN yum install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion libXext libSM \
    libXrender openssh-server

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-2019.10-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

ENV PATH /opt/conda/bin:$PATH
RUN conda update -n base conda
RUN conda update --all --y
RUN /opt/conda/bin/pip install -r requirements.txt
RUN conda install -c conda-forge widgetsnbextension
RUN conda install -c conda-forge jupyter_contrib_nbextensions

RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension
RUN jupyter nbextension enable --py --sys-prefix qgrid
RUN jupyter nbextension enable table_beautifier/main
RUN jupyter nbextension enable move_selected_cells/main
RUN jupyter nbextension enable init_cell/main
RUN jupyter nbextension enable hide_input_all/main
RUN jupyter nbextension enable varInspector/main
RUN jupyter nbextension enable toc2/main
RUN jupyter nbextension enable highlighter/highlighter
RUN jupyter nbextension enable codefolding/main
RUN jupyter nbextension enable toggle_all_line_numbers/main
RUN jupyter nbextension enable spellchecker/main
RUN jupyter nbextension enable runtools/main
RUN jupyter nbextension enable code_prettify/code_prettify

RUN mkdir -p /opt/notebooks

CMD ["/opt/conda/bin/python", "/app/notebook_builder.py"]