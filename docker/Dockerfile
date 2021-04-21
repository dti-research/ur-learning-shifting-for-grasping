# Copyright (c) 2021, Danish Technological Institute.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# Author: Nicolai Anton Lynnerup <nily@dti.dk>

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
        git \
        python3-dev \
        python3-pip \
        python3-empy \
        python3-setuptools \
        build-essential \
        gnupg2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

#####################
# Intel RealSense 2 #
#####################

RUN apt-get update \
    # Get lisence key
    && apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --keyserver-options http-proxy=${HTTP_PROXY} --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE \
    && apt-get install -y software-properties-common \
    # Add the repository
    && add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo $(lsb_release -cs) main" -u \
    # Install the librealsense, Development packages & and other needed packages
    && apt-get install -y \
    librealsense2-dkms \
    librealsense2-utils \
    librealsense2-dev

RUN pip install pyrealsense2

################
# pip packages #
################

RUN pip install matplotlib \
    opencv-python \
    imageio

RUN pip install --upgrade tensorflow==2.4.0
