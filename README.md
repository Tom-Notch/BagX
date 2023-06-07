# BagX

Bag Exchange for conversion between ROS Bag formats and mp4, jpg, png, csv, etc.

## Requirements

* NVIDIA GPU
* x86_64 machine (recommended)

## Docker

Grant permissions to all the scripts:

```Shell
sudo chmod -R a+wrx ./scripts
```

To pull:

```Shell
./docker/pull.sh
```

To run:

```Shell
./docker/run.sh
```

To build:

```Shell
./docker/build.sh
```

## Conda

If you have [NVIDIA DeepStream](https://developer.nvidia.com/deepstream-sdk) and ROS setup locally, you can try the conda environment `requirement.yaml`

```Shell
conda env create -f environment.yml
conda activate BagX
```

## Usage

1. modify the [./docker/run.sh](./docker/run.sh) according to your data directory

1. To run:

```Shell
./conversion.py -c < path to your config file >
```

## How it works

* The library currently **only** supports conversion from mp4 to rosbag/directory of images, but the coding structure is general enough to add other input/output later, e.g., rosbag input, csv output(for IMU, point cloud, etc.)
* The library can concurrently convert multiple files, i.e. multiple pipelines, using [Threading](https://docs.python.org/3/library/threading.html)
* mp4 reading is using [GStreamer](https://github.com/GStreamer/gstreamer), with [NVIDIA DeepStream](https://developer.nvidia.com/deepstream-sdk) plugin to enable `nvvideoconvert` pipeline for Nvidia's hardware-accelerated decoding on `NVDEC`
* Please follow the [example config](./config/example/mp4_to_imgdir_rosbag.yaml) for config file format, and follow the `./config` folder structure if you need to push your config
* Should you run into any trouble, please try the [Jupyter Notebook](./conversion.ipynb)

## Contacts

* Author: Mukai (Tom Notch) Yu: [mukaiy@andrew.cmu.edu](mailto:mukaiy@andrew.cmu.edu)
