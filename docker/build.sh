#!/bin/sh

# If you build using STDIN (docker build - < somefile) without --build-context, there is no build context, so COPY can't be used.
# The build-context here is named bagx-config, and it is the parent directory of this script. use it by: COPY --from=bagx-config in a Dockerfile.
docker buildx build --build-context bagx-config=$(dirname "$0")/config -t $USER/bagx:1.0 - < $(dirname "$0")/Dockerfile
