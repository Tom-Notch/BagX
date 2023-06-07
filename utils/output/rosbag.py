#!/usr/bin/env python3
import rosbag
import rospy
from sensor_msgs.msg import Image


class RosbagOutput:
    def __init__(self, name: str, output: dict):
        self.name = name
        self.path = output['path']
        self.directory = output['directory']
        self.topic = output['topic']
        self.frame_id = output.get('frame_id', None)

        assert output['type'] == 'rosbag', f'{self.name}\'s output type {output["type"]} is inappropriate for RosbagOutput Class.'

        self.init_rosbag()

    def init_rosbag(self) -> None:
        self.bag = rosbag.Bag(self.path, 'w')
        
        self.image_msg = Image()
        if self.frame_id is not None:
            self.image_msg.header.frame_id = self.frame_id
        self.image_msg.encoding = 'rgb8'
        self.image_msg.header.seq = -1

    def callback(self, image, time_stamp: int) -> None:
        self.image_msg.header.stamp = rospy.Time(secs=int(time_stamp // 1e9), nsecs=int(time_stamp % 1e9))
        self.image_msg.header.seq += 1
        self.image_msg.height = image.shape[0]
        self.image_msg.width = image.shape[1]
        self.image_msg.step = self.image_msg.width * 3
        self.image_msg.data = image.tobytes()

        self.bag.write(self.topic, self.image_msg, t=self.image_msg.header.stamp)

    def close(self) -> None:
        self.bag.close()
