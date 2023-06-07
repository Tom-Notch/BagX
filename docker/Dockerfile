 # =============================================================================
 # Created on Wed Jun 07 2023 16:09:02
 # Author: Mukai (Tom Notch) Yu
 # Email: mukaiy@andrew.cmu.edu
 # Affiliation: Carnegie Mellon University, Robotics Institute, the AirLab
 #
 # Copyright Ⓒ 2023 Mukai (Tom Notch) Yu
 # =============================================================================


FROM nvcr.io/nvidia/deepstream:6.2-base
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

RUN apt update && \
    apt full-upgrade -y && \
    apt autoremove -y && \
    apt autoclean -y

# install some goodies
RUN apt install apt-utils software-properties-common ncdu git less screen tmux tree net-tools vim nano emacs htop curl wget build-essential ffmpeg -y
# RUN apt install nvtop -y #! quarantined for compatibility issues

# copy oh-my-zsh powerlevel10k theme config
COPY --from=bagx-config ./.p10k.zsh /root/

# install zsh, Oh-My-Zsh, and plugins
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -p https://github.com/CraigCarey/gstreamer-tab \
    -a "[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh" \
    -a "bindkey -M emacs '^[[3;5~' kill-word" \
    -a "bindkey '^H' backward-kill-word" \
    -a "autoload -U compinit && compinit"

# change default shell in the image building process for extra environment safety
RUN chsh -s $(which zsh)

# Set the default shell to zsh
SHELL ["/bin/zsh", "-c"]

RUN apt install python3-pip python3-gi python3-dev python3-gst-1.0 -y

# set default python version to 3 (3.8)
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 2 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python2 1 && \
    update-alternatives --set python /usr/bin/python3

RUN apt install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# install ROS Noetic
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
    apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
    apt update -o Acquire::Check-Valid-Until=false -o Acquire::AllowInsecureRepositories=true -o Acquire::AllowDowngradeToInsecureRepositories=true && \
    apt install -y ros-noetic-desktop-full && \
    apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool ros-noetic-rosmon && \
    rosdep init && \
    rosdep update && \
    echo "source /opt/ros/noetic/setup.zsh" >> ~/.zshrc && \
    echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc #! required if we do not change shell using chsh $(which zsh)

# end of apt installs
RUN apt clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    pyyaml \
    opencv-python \
    numpy \
    tqdm \
    jupyter \
    ipykernel \
    ipython

# set up default workspace
RUN mkdir -p /root/BagX

WORKDIR /root/BagX

# Entrypoint command
ENTRYPOINT ["/bin/zsh"]
