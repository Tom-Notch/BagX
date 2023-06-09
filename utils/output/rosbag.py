# =============================================================================
# Created on Wed Jun 07 2023 16:09:02
# Author: Mukai (Tom Notch) Yu
# Email: mukaiy@andrew.cmu.edu
# Affiliation: Carnegie Mellon University, Robotics Institute, the AirLab
#
# Copyright Ⓒ 2023 Mukai (Tom Notch) Yu
# =============================================================================

import rosbag
import rospy
from sensor_msgs.msg import Image


class RosbagOutput:
    """Rosbag output, outputs a rosbag file"""

    def __init__(self, name: str, output: dict):
        """initialize the RosbagOutput class

        Args:
            name (str): name of this pipeline in the yaml config
            output (dict): output config dictionary
        """
        self.name = name
        self.path = output["path"]
        self.directory = output["directory"]
        self.topic = output["topic"]
        self.frame_id = output.get("frame_id", None)

        assert (
            output["type"] == "rosbag"
        ), f'{self.name}\'s output type {output["type"]} is inappropriate for RosbagOutput Class.'

        self.init_rosbag()

    def init_rosbag(self) -> None:
        """initialize the rosbag file, set up the common part of the image message"""
        self.bag = rosbag.Bag(self.path, "w")

        self.image_msg = Image()
        if self.frame_id is not None:
            self.image_msg.header.frame_id = self.frame_id
        self.image_msg.encoding = "rgb8"
        self.image_msg.header.seq = -1

    def callback(self, image, time_stamp: int) -> None:
        """callback function of the RosbagOutput class, writes the image to the rosbag file

        Args:
            image (numpy.array): image in RGB encoding to be written
            time_stamp (int): timestamp in nanoseconds
        """
        self.image_msg.header.stamp = rospy.Time(
            secs=int(time_stamp // 1e9), nsecs=int(time_stamp % 1e9)
        )
        self.image_msg.header.seq += 1
        self.image_msg.height = image.shape[0]
        self.image_msg.width = image.shape[1]
        self.image_msg.step = self.image_msg.width * 3
        self.image_msg.data = image.tobytes()

        self.bag.write(self.topic, self.image_msg, t=self.image_msg.header.stamp)

    def close(self) -> None:
        """close function of the RosbagOutput class, closes the rosbag file to prevent reindex operation"""
        self.bag.close()
