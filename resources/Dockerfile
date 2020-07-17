FROM ubuntu:16.04

# Install CellProfiler dependencies
RUN   apt-get -y update &&                                          \
      apt-get -y install                                            \
        python3 python3-dev \
	python3-pip python3-venv python3-wheel python3-setuptools 	   \
	build-essential    \
        cython             \
        git                \
        libmysqlclient-dev \
        libhdf5-dev        \
        libxml2-dev        \
        libxslt-dev       \
        openjdk-8-jdk      \
        python-dev         \
        python-pip         \
        python-h5py        \
        python-matplotlib  \
        python-mysqldb     \
        python-scipy       \
        python-numpy       \
        python-wxgtk3.0    \
        python-zmq

WORKDIR /usr/local/src

# Install CellProfiler
RUN git clone https://github.com/CellProfiler/CellProfiler.git

WORKDIR /usr/local/src/CellProfiler

ARG version=3.1.5

RUN git fetch -a

RUN git pull

RUN git checkout tags/v$version

RUN pip install --upgrade pip

RUN pip install natsort==5.3.3

RUN pip install Pillow

RUN pip install matplotlib==2.2.2

RUN pip install pytest

RUN pip install --ignore-installed centrosome==1.1.6

RUN pip install --ignore-installed pyzmq

RUN pip install --ignore-installed docutils==0.15

RUN pip install --upgrade numpy==1.15.4

RUN pip install h5py==2.7.1
RUN pip install -e .


# Fix init and zombie process reaping problems using s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v1.21.2.2/s6-overlay-amd64.tar.gz /tmp/

RUN tar -xzf /tmp/s6-overlay-amd64.tar.gz -C /
