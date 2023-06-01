FROM nvcr.io/nvidia/deepstream:6.2-base
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

RUN apt install -y tzdata \
    && ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

RUN apt install -y --no-install-recommends \
    apt-utils \
    software-properties-common

# install some goodies
RUN apt install ncdu git less screen tmux tree net-tools vim nano emacs htop curl wget zsh build-essential ffmpeg -y

RUN apt install python3-pip python3-gi python3-dev python3-gst-1.0 -y

# install ROS Noetic
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' \
    && apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 \
    && apt update -o Acquire::Check-Valid-Until=false -o Acquire::AllowInsecureRepositories=true -o Acquire::AllowDowngradeToInsecureRepositories=true \
    && apt install -y ros-noetic-desktop-full \
    && apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool ros-noetic-rosmon \
    && rosdep init \
    && rosdep update

RUN apt update \
    && apt full-upgrade -y \
    && apt autoremove -y \
    && apt autoclean -y \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    pyyaml \
    opencv-python \
    numpy \
    tqdm

# set default python version to 3 (3.8)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 2 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python2 1 \
    && update-alternatives --set python /usr/bin/python3

# install zsh, Oh-My-Zsh, and plugins
RUN sh -c "$(curl -L https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -a "bindkey -M emacs '^[[3;5~' kill-word" \
    -a "bindkey '^H' backward-kill-word" \
    -a "source /opt/ros/noetic/setup.zsh"

RUN chsh -s $(which zsh)

WORKDIR /root

# Entrypoint command
ENTRYPOINT [ "/bin/zsh" ]
