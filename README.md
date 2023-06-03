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
```
