#!/usr/bin/env python3
import cv2
import os


class ImgDirOutput:
    def __init__(self, name: str, output: dict):
        self.name = name
        self.path = output['path']
        self.directory = output['directory']

        assert output['type'] == 'directory', f'{self.name}\'s output type {output["type"]} is inappropriate for ImgDirOutput Class.'

    def callback(self, image, time_stamp: int) -> None:
        output_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(self.directory, str(time_stamp) + '.png'), output_image)

    def close(self) -> None:
        pass
