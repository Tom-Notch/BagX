#!/usr/bin/env python3
from .input.mp4 import MP4Input
from .output.img_dir import ImgDirOutput
from .output.rosbag import RosbagOutput
from .macros import file_type_to_extension
import threading


class Pipeline(threading.Thread):
    def __init__(self, name: str, pipeline: dict):
        super().__init__()
        self.name = name
        self.outputs = self.init_outputs(pipeline['output'])
        self.input = self.init_input(pipeline['input'])

    def init_outputs(self, outputs_dict: dict):
        outputs={}
        for name, output in outputs_dict.items(): # name is arbitrary and doesn't matter
            output_type = output['type']
            assert output_type in file_type_to_extension.keys(), f'pipeline {self.name} output\'s file type {output_type} is not supported'
            if output_type == 'directory':
                outputs[name] = ImgDirOutput(name, output)
            elif output_type == 'rosbag':
                outputs[name] = RosbagOutput(name, output)
        return outputs

    def init_input(self, input_dict: dict):
        assert input_dict['type'] in file_type_to_extension.keys(), f'pipeline {self.name} input\'s file type {input_dict["type"]} is not supported'
        if input_dict['type'] == 'mp4':
            return MP4Input(self.name, input_dict, self.outputs)

    def run(self):
        print(f"{self.name} pipeline started.")
        self.input.loop()
