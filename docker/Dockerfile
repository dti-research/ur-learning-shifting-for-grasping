# Copyright (c) 2020, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the GNU-style license found in the
# LICENSE file in the root directory of this source tree.
# 
# Original author: Nicolai Anton Lynnerup <nily@dti.dk>

FROM ubuntu:18.04

LABEL maintainer="Nicolai Anton Lynnerup nily@dti.dk"

# Set working directory

RUN mkdir -p /code
WORKDIR /code

################
# Dependencies #
################

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y --no-install-recommends \
        iproute2 \
		iputils-ping \
		mlocate \
		nano \
        net-tools \
        wget \
        python3-dev \
        python3-pip \
        python3-empy \
		python3-setuptools \
		build-essential \
        gnupg2 \
        software-properties-common

## Install Python 3.7
#RUN apt-get update && add-apt-repository ppa:deadsnakes/ppa && \
#    apt-get install -y --no-install-recommends \
#        python3.7 \
#        python3-pip \
#        python3-empy \
#		python3-setuptools && \
#    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1


RUN pip3 install "pybind11[global]" --upgrade pip

RUN pip install matplotlib \
	opencv-python \
	pyrealsense2

#RUN pip install --upgrade tensorflow==2.4.0

#####################
# Intel RealSense 2 #
#####################

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update \
	# Get lisence key
	&& apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE \
	&& apt-get install -y software-properties-common \
	# Add the repository 
	&& add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main" -u \
	# Install the librealsense, Development packages & and other needed packages
	&& apt-get install -y \
	librealsense2-dkms \
	librealsense2-utils \
	librealsense2-dev  \
	librealsense2-dbg \
	# Upgrade the local packages 
	&& apt-get update && apt-get --only-upgrade install -y librealsense2-utils librealsense2-dkms
