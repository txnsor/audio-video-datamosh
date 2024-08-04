# Audio-Video Datamosh Script - Video
# by Marceline / Marc Browning

import os, ffmpeg, frame, subprocess

# this isnt a good way to do this i think
PARENT_DIRECTORY  = frame.PARENT_DIRECTORY
FRAME_DIRECTORY = frame.FRAME_DIRECTORY

PADDING_ZEROES = 5
FIRST_FRAME_NUM = 1

# helper function
def pad_filename(current_frame, MAX_STR_SIZE = PADDING_ZEROES):
## Add zeroes to the start of the filename if needed.
    result = str(current_frame)
    while len(result) != MAX_STR_SIZE: result = "0" + result
    return result

# helper function, taken from stack overflow
def get_length(filename):
    ## get the length in seconds of a video
    result = subprocess.Popen(["ffprobe", "filename"],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    return [x for x in result.stdout.readlines() if "Duration" in x]

class Video:
    # a video stream
    __slots__ = ["__stream", "__fps", "__number_of_frames", "__frames"]

    def __init__(self, filename, fps):
        # initialize video stream
        self.__stream = ffmpeg.input(PARENT_DIRECTORY + filename)
        # init fps
        self.__fps = fps
        # get number of frames
        self.__number_of_frames = fps * get_length(PARENT_DIRECTORY + filename)
    
    def make_frames(self):
    ## turn stream into frames
        # export the frames of the stream as bmp files
        self.__stream.filter('fps', fps=str(self.__fps)).output(
            FRAME_DIRECTORY + "%0" + PADDING_ZEROES + "d.bmp", start_number=0
            ).overwrite_output().run(quiet=True)
        
    def get_frames(self, debug=False):
    ## initialize list of frame objects
        self.__frames = []
        # loop through the frames
        for i in range(FIRST_FRAME_NUM, self.__number_of_frames + FIRST_FRAME_NUM):
            # adds frames to list
            self.__frames.append(frame.Frame(FRAME_DIRECTORY + pad_filename(i) + ".bmp"), debug=debug)
    
    def frames_to_video(self):
        # overwrite video with frames

        


    