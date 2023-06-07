#!/usr/bin/env python3
import cv2
import os


class ImgDirOutput:
    """Image Directory Output, outputs a directory of images with timestamps in nanoseconds as file names
    """
    def __init__(self, name: str, output: dict):
        """initialize the ImgDirOutput class
        
        Args:
            name (str): name of this pipeline in the yaml config
            output (dict): output config dictionary
        """
        self.name = name
        self.path = output['path']
        self.directory = output['directory']

        assert output['type'] == 'directory', f'{self.name}\'s output type {output["type"]} is inappropriate for ImgDirOutput Class.'

    def callback(self, image, time_stamp: int) -> None:
        """Callback function of the ImgDirOutput class, writes the image to the directory with the timestamp as the file name

        Args:
            image (numpy.array): image in RGB encoding to be written
            time_stamp (int): timestamp in nanoseconds

        Returns:
            None
        """
        output_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(self.directory, str(time_stamp) + '.png'), output_image)

    def close(self) -> None:
        """Close function of the ImgDirOutput class, does nothing

        Returns:
            None
        """
        pass
