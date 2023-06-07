#!/bin/sh

DATA_PATH="/home/$USER/bags" #! modify this to your own data path!

xhost +local:root
XAUTH=/tmp/.docker.xauth
AVAILABLE_CORES=$(($(nproc) - 1))

if [ ! -f $XAUTH ]
then
    touch $XAUTH
    xauth_list=$(xauth nlist :0 | sed -e 's/^..../ffff/')
    if [ ! -z "$xauth_list" ]
    then
        echo $xauth_list | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi

docker run --name BagX \
           -h bagx \
           --privileged \
           --cpus $AVAILABLE_CORES \
           --gpus all \
           --network host \
           -e "DISPLAY=$DISPLAY" \
           -e "QT_X11_NO_MITSHM=1" \
           -e "XAUTHORITY=$XAUTH" \
           -e "ROS_MASTER_URI=http://localhost:11311" \
           -v $XAUTH:$XAUTH \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v $(dirname "$0")/../:/root/BagX/ \
           -v "$DATA_PATH:/root/data" \
           --rm \
           -itd tomnotch/bagx:1.0
