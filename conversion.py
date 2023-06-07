#!/usr/bin/env python3

 # =============================================================================
 # Created on Wed Jun 07 2023 16:09:02
 # Author: Mukai (Tom Notch) Yu
 # Email: mukaiy@andrew.cmu.edu
 # Affiliation: Carnegie Mellon University, Robotics Institute, the AirLab
 #
 # Copyright Ⓒ 2023 Mukai (Tom Notch) Yu
 # =============================================================================

from utils.tools import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Conversion between rosbag, mp4, image directory, etc.')
    parser.add_argument('--config', '-c', type=str, required=True, default='./config/example/mp4_to_imgdir_rosbag.yaml', help='path to config file')
    args = parser.parse_args()

    cfg = load_config(args.config)
    trace_config(cfg)

    pipelines = []
    for pipeline_name in cfg["pipelines"]:
        pipeline = Pipeline(pipeline_name, cfg[pipeline_name])
        pipeline.start()
        pipelines.append(pipeline)

    for pipeline in pipelines:
        pipeline.join()
