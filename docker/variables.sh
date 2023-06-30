#!/usr/bin/env bash

# =============================================================================
# Created on Wed Jun 07 2023 16:09:02
# Author: Mukai (Tom Notch) Yu
# Email: mukaiy@andrew.cmu.edu
# Affiliation: Carnegie Mellon University, Robotics Institute, the AirLab
#
# Copyright Ⓒ 2023 Mukai (Tom Notch) Yu
# =============================================================================

export XAUTH=/tmp/.docker.xauth
export AVAILABLE_CORES=$(($(nproc) - 1))

export DOCKER_USER=tomnotch
export IMAGE_NAME=bagx
export IMAGE_TAG=1.0

export CONTAINER_NAME=$IMAGE_NAME
export CONTAINER_HOME_FOLDER=/root

HOST_UID=$(id -u)
HOST_GID=$(id -g)
export HOST_UID
export HOST_GID

export DATASET_PATH="/home/$USER/bags" #! modify the dataset path with yours
