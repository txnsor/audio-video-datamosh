# Audio-Video Datamosh Script - Video
# by Marceline / Marc Browning

import os, ffmpeg, frame, pedalboard, math, time, shutil

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
    __slots__ = ["__stream", "__fps", "__number_of_frames", "__frames", "__working", "__filename", "__path"]

    def __init__(self, filename, fps):
        # initialize video stream
        self.__stream = ffmpeg.input(filename)
        # init fps
        self.__fps = fps
        # get number of frames
        self.__number_of_frames = fps * float(get_length(filename))
        # init working as False
        self.__working = False
        # save filename
        self.__filename = filename
        # create frames folder if it doesnt exist
        if not os.path.exists(os.path.dirname(os.path.abspath(self.__filename)) + "\\frames\\"): os.mkdir(os.path.dirname(os.path.abspath(self.__filename)) + "\\frames\\")

        self.__path = os.path.dirname(os.path.abspath(self.__filename)) + "\\frames\\"
    
    def make_frames(self):
    ## turn stream into frames
        # export the frames of the stream as bmp files
        self.__stream.filter('fps', fps=str(self.__fps)).output(self.__path + "%0" + str(PADDING_ZEROES) + "d.bmp", start_number=0
            ).overwrite_output().run()
        
    def get_frames(self, debug=False):
    ## initialize list of frame objects
        self.__frames = []
        # loop through the frames
        for i in range(FIRST_FRAME_NUM, math.floor(self.__number_of_frames) + FIRST_FRAME_NUM):
            # adds frames to list
            self.__frames.append(frame.Frame(self.__path + pad_filename(i) + ".bmp"))
        self.__working = True
        return self.__frames

    def set_frames(self, frames): self.__frames = frames

    def clear_frames(self):
        # delete all frames in the folder
        shutil.rmtree(self.__path)
    
    def frames_to_video(self, out):
        if not self.__working: raise ValueError("Video not in a working state.")
        # overwrite video with frames
        ffmpeg.input(self.__path + "%0" + str(PADDING_ZEROES) + "d.bmp", framerate=self.__fps
                     ).output(out).run()
        self.__working = False
        self.clear_frames()
    
def audio_datamosh(effects, in_video, out_video, fps):
    start = time.time()
    video = Video(in_video, fps)

    print("making frames...")
    video.make_frames()
    frames = video.get_frames()

    print("adding effects...")
    for frame in frames:
        frame.set_working_frame_audio()
        frame.audio_datamosh(effects)
        frame.export_frame_audio()

    print("assembling video...")
    video.set_frames(frames)
    video.frames_to_video(out_video)

    print("done! exported to " + out_video)
    end = time.time()
    print("elapsed: " + str(end - start) + " seconds")

def search_and_replace(se, rp, in_video, out_video, fps):
    start = time.time()
    video = Video(in_video, fps)

    print("making frames...")
    video.make_frames()
    frames = video.get_frames()

    print("adding effects...")
    for frame in frames:
        frame.set_working_frame_other()
        temp = frame.search_and_replace_datamosh(se, rp)
        frame.export_frame_other(temp)

    print("assembling video...")
    video.set_frames(frames)
    video.frames_to_video(out_video)

    print("done! exported to " + out_video)
    end = time.time()
    print("elapsed: " + str(end - start) + " seconds")

def main():

    mode = str(input("(A - audio effects, B - search and replace) \nmode > "))

    effects = pedalboard.Pedalboard([pedalboard.Delay(), pedalboard.Reverb(room_size=0.7)])

    video = str(input("video file path > "))
    out = str(input("output file path > "))
    fps = float(input("target fps > "))

    if mode == "A":
        audio_datamosh(effects, video, out, fps)
    elif mode == "B":
    # SEARCH AND REPLACE
        se = input("\nsearch string > ")
        rp = input("replacement string (this should be the same length as the search string) > ")
        search_and_replace(se, rp, video, out, fps)
    else:
        print("Goodbye!")


if __name__ == "__main__": main()


        


    