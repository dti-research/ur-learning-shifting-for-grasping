# Reproducible Robot Learning of Shifting Objects for Grasping in Cluttered Environments with UR and Intel RealSense

This repository contains a *replication* of the paper *Robot Learning of Shifting Objects for Grasping in Cluttered Environments* presented at IROS 2019 in Macau. All dependencies are contained in a Docker image available from Docker Hub: [dtiresearch/ur-learning-shifting-for-grasping](https://hub.docker.com/repository/docker/dtiresearch/ur-learning-shifting-for-grasping) to allow for easy reproduction.

<div align="center">
  <img height="250" src="https://raw.githubusercontent.com/dti-research/ur-learning-shifting-for-grasping/master/resources/IMG_0091.jpeg?token=AL2CCR6RZDUMD2IMCQ2ILSK74HBQW">
  <img height="250" src="https://raw.githubusercontent.com/dti-research/ur-learning-shifting-for-grasping/master/resources/IMG_0092.jpeg?token=AL2CCR6RZDUMD2IMCQ2ILSK74HBQW">
</div>

In contrast to the original approach we implement the program flow inside the Universal Robot's Polyscope, which is their programming interface for integrators on the teach pendant (TP). Thus allowing for a higher degree of maintainability and ease of use for non-experts within reinforcement learning (RL). In addition to the robot we have a compute box (running Ubuntu 20.04 with Docker 19.03.14, build 5eb3275d40) which is connected to the UR5 (e-series) through TCP/IP and the Intel RealSense (D435) camera through USB3.1 gen 2.



## Hardware

- Universal Robots&trade; [UR5 e-series](https://www.universal-robots.com/products/ur5-robot/) ([SW 5.9.1.1031110](https://s3-eu-west-1.amazonaws.com/ur-support-site/88180/update-5.9.1.1031110.urup))
- ROBOTIQ&trade; [Hand-E](https://robotiq.com/products/hand-e-adaptive-robot-gripper) Adaptive Gripper ([GD1-1.3.16](https://assets.robotiq.com/website-assets/support_documents/document/Update_20Firmware_20Hand-E_20190916.zip?_ga=2.47184997.337818148.1608549310-377652996.1608549310))
- Intel&reg; RealSense&trade; [D435](https://www.intelrealsense.com/depth-camera-d435/) Depth Camera

### Models

- CAD-models of the gripper fingers, camera mount, and box mounts are located in the `cad-models` directory


## Software

### Installation on UR Controller

- Install the ROBOTIQ URCap ([UCG-1.8.6](https://robotiq.com/support/hand-e-adaptive-robot-gripper/)) on the UR5
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
