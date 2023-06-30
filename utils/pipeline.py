# =============================================================================
# Created on Wed Jun 07 2023 16:09:02
# Author: Mukai (Tom Notch) Yu
# Email: mukaiy@andrew.cmu.edu
# Affiliation: Carnegie Mellon University, Robotics Institute, the AirLab
#
# Copyright Ⓒ 2023 Mukai (Tom Notch) Yu
# =============================================================================

from .input.mp4 import MP4Input
from .output.img_dir import ImgDirOutput
from .output.rosbag import RosbagOutput
from .macros import file_type_to_extension
import threading


class Pipeline(threading.Thread):
    def __init__(self, name: str, pipeline: dict):
        super().__init__()
        self.name = name
        self.outputs = self.init_outputs(pipeline["output"])
        self.input = self.init_input(pipeline["input"])

    def init_outputs(self, outputs_dict: dict) -> dict:
        """initialize the output classes

        Args:
            outputs_dict (dict): output config dictionary

        Returns:
            dict: dictionary of output class instances
        """
        outputs = {}
        for (
            name,
            output,
        ) in outputs_dict.items():  # name is arbitrary and doesn't matter
            output_type = output["type"]
            assert (
                output_type in file_type_to_extension.keys()
            ), f"pipeline {self.name} output's file type {output_type} is not supported"
            if output_type == "directory":
                outputs[name] = ImgDirOutput(name, output)
            elif output_type == "rosbag":
                outputs[name] = RosbagOutput(name, output)
        return outputs

    def init_input(self, input_dict: dict):
        """initialize the input class, should be called after output classes are initialized

        Args:
            input_dict (dict): input config dictionary, contains instances of the input classes, must have callback() and close() functions
        """
        assert (
            input_dict["type"] in file_type_to_extension.keys()
        ), f'pipeline {self.name} input\'s file type {input_dict["type"]} is not supported'
        if input_dict["type"] == "mp4":
            return MP4Input(self.name, input_dict, self.outputs)

    def run(self) -> None:
        """run the pipeline, starts the input loop, which will call the output callbacks
        This pipeline class is a thread, so this function will be called when the thread is started by calling start()
        """
        print(f"{self.name} pipeline started.")
        self.input.loop()
