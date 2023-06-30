#!/bin/sh

# =============================================================================
# Created on Wed Jun 07 2023 16:09:02
# Author: Mukai (Tom Notch) Yu
# Email: mukaiy@andrew.cmu.edu
# Affiliation: Carnegie Mellon University, Robotics Institute, the AirLab
#
# Copyright Ⓒ 2023 Mukai (Tom Notch) Yu
# =============================================================================

. "$(dirname "$0")"/variables.sh

docker pull "$DOCKER_USER"/"$IMAGE_NAME":"$IMAGE_TAG"
