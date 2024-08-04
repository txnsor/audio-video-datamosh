# Audio-Video Datamosh Script - Video
# by Marceline / Marc Browning

import os, ffmpeg, frame, pedalboard, math, time

# this isnt a good way to do this i think
PARENT_DIRECTORY  = frame.PARENT_DIRECTORY
FRAME_DIRECTORY = frame.FRAME_DIRECTORY

PADDING_ZEROES = 5
FIRST_FRAME_NUM = 0

# helper function
def pad_filename(current_frame, MAX_STR_SIZE = PADDING_ZEROES):
## Add zeroes to the start of the filename if needed.
    result = str(current_frame)
    while len(result) != MAX_STR_SIZE: result = "0" + result
    return result

# helper function
def get_length(filename):
    probe = ffmpeg.probe(filename)
    return probe['format']['duration']

class Video:
    # a video stream
    __slots__ = ["__stream", "__fps", "__number_of_frames", "__frames", "__working", "__filename"]

    def __init__(self, filename, fps):
        # initialize video stream
        self.__stream = ffmpeg.input(PARENT_DIRECTORY + filename)
        # init fps
        self.__fps = fps
        # get number of frames
        self.__number_of_frames = fps * float(get_length(PARENT_DIRECTORY + filename))
        # init working as False
        self.__working = False
        # save filename
        self.__filename = filename
    
    def make_frames(self):
    ## turn stream into frames
        # export the frames of the stream as bmp files
        self.__stream.filter('fps', fps=str(self.__fps)).output(
            FRAME_DIRECTORY + "%0" + str(PADDING_ZEROES) + "d.bmp", start_number=0
            ).overwrite_output().run(quiet=True)
        
    def get_frames(self, debug=False):
    ## initialize list of frame objects
        self.__frames = []
        # loop through the frames
        for i in range(FIRST_FRAME_NUM, math.floor(self.__number_of_frames) + FIRST_FRAME_NUM):
            # adds frames to list
            self.__frames.append(frame.Frame(pad_filename(i) + ".bmp"))
        self.__working = True
        return self.__frames

    def set_frames(self, frames): self.__frames = frames
    
    def frames_to_video(self):
        if not self.__working: raise ValueError("Video not in a working state.")
        # overwrite video with frames
        ffmpeg.input(FRAME_DIRECTORY + "%0" + str(PADDING_ZEROES) + "d.bmp", framerate=self.__fps
                     ).output(PARENT_DIRECTORY + self.__filename).run()
        self.__working = False

def main():
## for debugging
    start = time.time()
    my_video = Video("test.mp4", 12) # 1 frame every 4 seconds
    print("making frames...")
    my_video.make_frames()
    print("getting frames...")
    frames = my_video.get_frames()
    print("effecting frames...")
    for frame in frames:
        frame.set_working_frame()
        frame.edit_frame(pedalboard.Pedalboard([pedalboard.Chorus(), pedalboard.Reverb(room_size=0.7), pedalboard.Bitcrush(bit_depth=5)]))
        frame.export_frame()
    print("putting video together...")
    my_video.set_frames(frames)
    my_video.frames_to_video()
    print("done!")
    end = time.time()
    print("elapsed: " + end - start + " seconds")

if __name__ == "__main__": main()


        


    