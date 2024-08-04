# Audio-Video Datamosh Script - Video
# by Marceline / Marc Browning

import os, ffmpeg, frame

# this isnt a good way to do this i think
PARENT_DIRECTORY  = frame.PARENT_DIRECTORY
FRAME_DIRECTORY = frame.FRAME_DIRECTORY


class Video:
    # a video stream
    __slots__ = ["__stream", "__fps"]

    def __init__(self, filename, fps):
        # initialize video stream
        self.__stream = ffmpeg.input(PARENT_DIRECTORY + filename)
        # init fps
        self.__fps = fps
    
    def make_frames(self, start_frame=1, end_frame=-1):
    ## turn stream into list of frame objects
        self.__stream.filter('fps', fps=self.__fps)


    