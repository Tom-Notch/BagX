#!/usr/bin/env python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np
import re
import time


class MP4Input:
    """MP4 Input recorded by the image_sharing package: https://bitbucket.org/castacks/image_sharing/
    """
    def __init__(self, name: str, input: dict, outputs: dict):
        """initialize the MP4Input class

        Args:
            name (str): name of this pipeline in the yaml config, used in named sink of gstreamer pipeline
            input (dict): input config
            output (list): list of output class instances, this input class only uses their callback functions
        """
        Gst.init(None)
        self.name = name
        self.path = input['path']
        if not input['type'] == 'mp4': # verify type is correct
            raise ValueError(f'Input type {input["type"]} is inappropriate for MP4Input Class.')

        self.width = input.get('width', None)
        self.height = input.get('height', None)
        self.start = input.get('start', None)
        self.end = input.get('end', None)
        self.output_callbacks = [output.callback for output in outputs.values()]
        self.close_handlers = [output.close for output in outputs.values()]

        self.setup()

    def setup(self) -> None:
        """setup the gstreamer pipeline

        Returns:
            None
        """
        self.parse_start_time()

        self.bytes_per_pixel = 3 # since it's in RGB format
        self.current_relative_time = 0

        # setup gstreamer pipeline
        self.gstreamer_pipeline_str = "filesrc location=" + self.path + " ! decodebin ! nvvideoconvert ! video/x-raw,format=RGB"
        if self.width:
            self.gstreamer_pipeline_str += ",width=" + str(self.width)
        if self.height:
            self.gstreamer_pipeline_str += ",height=" + str(self.height)
        self.gstreamer_pipeline_str += " ! progressreport update-freq=1 name=" + self.name + "_progress ! fakesink name=" + self.name # Using fakesink since it's significantly faster than using appsink
        print(self.name + " MP4Input's gstreamer pipeline string: " + self.gstreamer_pipeline_str)
        self.gstreamer_pipeline = Gst.parse_launch(self.gstreamer_pipeline_str)
        self.gstreamer_pipeline.get_by_name(self.name).get_static_pad('sink').add_probe(Gst.PadProbeType.BUFFER, self.callback)

    def parse_start_time(self) -> None:
        """parse the absolute start time in nanoseconds from the file name

        Returns:
            None
        """
        match = re.search(r'(\d{10}_\d{9})(?=\.\w+$)', self.path)
        assert match is not None, f'{self.path} does not contain the proper timestamp sub-string.'
        time_str = match[1].split('_')
        self.absolute_start_time = int(time_str[0]) * int(1e9) + int(time_str[1])

    def callback(self, pad, info) -> Gst.PadProbeReturn:
        """callback probe function for the sink pad of the fakesink of the gstreamer pipeline

        Args:
            pad (Gst.Pad): the sink pad of the fakesink
            info (Gst.PadProbeInfo): the probe info

        Returns:
            Gst.PadProbeReturn: Gst.PadProbeReturn.OK to continue the pipeline
        """

        # get the current frame and time stamp in nanoseconds
        image, self.current_relative_time = self.get_frame(pad, info)

        # check if the current frame is within the start and end time
        if (self.start and self.current_relative_time * 1e-9 < self.start) or (self.end and self.current_relative_time * 1e-9 > self.end):
            return Gst.PadProbeReturn.OK

        current_absolute_time = self.absolute_start_time + self.current_relative_time

        # calling callbacks for each output pipeline
        for callback in self.output_callbacks:
            callback(image, current_absolute_time)

        return Gst.PadProbeReturn.OK

    def get_frame(self, pad, info) -> tuple:
        """get the current frame and time stamp in nanoseconds
        
        Args:
            pad (Gst.Pad): the sink pad of the sink
            info (Gst.PadProbeInfo): the probe info

        Returns:
            tuple: (image, time_stamp): image in RGB format and time stamp in nanoseconds
        """
        buffer = info.get_buffer()
        caps = pad.get_current_caps()

        caps_structure = caps.get_structure(0)
        height, width = caps_structure.get_value('height'), caps_structure.get_value('width')

        is_mapped, map_info = buffer.map(Gst.MapFlags.READ)
        if is_mapped:
            try:
                image = np.ndarray((height, width, self.bytes_per_pixel), dtype='uint8', buffer=map_info.data).copy() # extend array lifetime beyond subsequent unmap
            finally:
                buffer.unmap(map_info)
        
        return image, buffer.pts # using pts instead of dts since it's set in the mp4 file recorded using https://bitbucket.org/castacks/image_sharing/src/c5ab07622155793ff756020d1a8117a7d5036325/src/tools/to_gstreamer.cpp#lines-156
    
    def loop(self) -> None:
        """Starts the gstreamer pipeline

        Returns:
            None
        """
        self.gstreamer_pipeline.set_state(Gst.State.PLAYING)

        try:
            while True:
                msg = self.gstreamer_pipeline.get_bus().timed_pop_filtered(Gst.SECOND * 5, Gst.MessageType.EOS | Gst.MessageType.ERROR) #! 5 seconds timeout

                if msg:
                    if msg.type == Gst.MessageType.EOS:
                        break
                    elif msg.type == Gst.MessageType.ERROR:
                        raise Exception('GStreamer stream Error occurred in pipeline: ' + self.name)

                # # Query position and duration to display progress
                # success, position = self.gstreamer_pipeline.query_position(Gst.Format.TIME)
                # success, duration = self.gstreamer_pipeline.query_duration(Gst.Format.TIME)

                # if success and duration != Gst.CLOCK_TIME_NONE and duration != 0:
                #     progress = (position / duration) * 100
                #     print(f"{self.name}\'s progress: {progress:.2f}%")

                #! delay for 5 seconds since the progress query is blocking
                time.sleep(5)
        finally:
            self.gstreamer_pipeline.set_state(Gst.State.NULL)

            # call close handlers for each output pipeline
            for close_handler in self.close_handlers:
                close_handler()
            print(f'Pipeline {self.name} finished.')
