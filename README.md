# Reproducible Robot Learning of Shifting Objects for Grasping in Cluttered Environments with UR and Intel RealSense

This repository contains a *replication* of the paper [Robot Learning of Shifting Objects for Grasping in Cluttered Environments](https://arxiv.org/abs/1907.11035) presented at IROS 2019 in Macau. All dependencies are contained in a Docker image available from Docker Hub: [dtiresearch/ur-learning-shifting-for-grasping](https://hub.docker.com/repository/docker/dtiresearch/ur-learning-shifting-for-grasping) to allow for easy reproduction.

<div align="center">
  <img height="350" src="https://raw.githubusercontent.com/dti-research/ur-learning-shifting-for-grasping/master/resources/IMG_20210308_115623.jpg?token=AL2CCR6RZDUMD2IMCQ2ILSK74HBQW">
  <img height="350" src="https://raw.githubusercontent.com/dti-research/ur-learning-shifting-for-grasping/master/resources/IMG_20210308_115635.jpg?token=AL2CCR6RZDUMD2IMCQ2ILSK74HBQW">
</div>

In contrast to the original approach we implement the program flow inside the Universal Robot's Polyscope. Thus allowing for a higher degree of maintainability and ease of use for non-experts within Python/C++ and reinforcement learning (RL). In addition to the robot we have a compute box (running Ubuntu 20.04 with Docker 19.03.14, build 5eb3275d40) which is connected to (1) the UR5 (e-series) through TCP/IP and (2) the Intel RealSense (D435) camera through USB3.1 gen 2.



## Hardware

- Universal Robots&trade; [UR5 e-series](https://www.universal-robots.com/products/ur5-robot/) ([SW 5.9.1.1031110](https://s3-eu-west-1.amazonaws.com/ur-support-site/88180/update-5.9.1.1031110.urup))
- Schunk&reg; [EGI](https://schunk.com/dk_en/gripping-systems/series/egi/) Gripper
- Intel&reg; RealSense&trade; [D435](https://www.intelrealsense.com/depth-camera-d435/) Depth Camera

### Models

- CAD-models of the gripper fingers, camera mount, and box mounts are located in the `cad-models` directory


## Software

### Installation on UR Controller

- Install the Schunk EGI URCap ([v.1.0.1](https://github.com/dti-research/ur-learning-shifting-for-grasping/blob/master/ur/urcaps/egh-schunk-1.0.1.urcap?raw=true)) on the UR5
- Install the DTI UR Libraries URCap ([v.0.3.0](https://github.com/dti-research/ur-learning-shifting-for-grasping/blob/master/ur/urcaps/dtiurlibs-0.3.0.urcap?raw=true))
- Copy the content of the [ur/](ur/) folder in this repo onto an empty USB. Insert the USB in the robot's TP and the files will automatically be copied to the controller ready to be run.

### Installation on Compute Box

Only prerequisite is that you have Docker installed

- Pull down our Docker image

```
docker pull dtiresearch/ur-learning-shifting-for-grasping
```

### Running the Demo

- Start the container on the compute box

```
docker run -it --rm --net=host --privileged \
           dtiresearch/ur-learning-shifting-for-grasping
```

> **_NOTE:_** The docker container requires priveleged rights in order to communicate with the camera through USB and access to the host' network to communicate with the robot.

- Start the XML-RPC servers

```
TO DO
```

### Models

 - The trained models is available in the `models` directory
