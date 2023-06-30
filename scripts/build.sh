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

# If you build using STDIN (docker build - < somefile) without --build-context, there is no build context, so COPY can't be used.
# The build-context here is named bagx-config, and it is the parent directory of this script. use it by: COPY --from=bagx-config in a Dockerfile.
docker buildx build --platform=linux/amd64 \
                    --build-context bagx-config="$(dirname "$0")"/../docker/config \
                    -t "$DOCKER_USER"/"$IMAGE_NAME":"$IMAGE_TAG" \
                    - < "$(dirname "$0")"/../docker/"$IMAGE_TAG".dockerfile
