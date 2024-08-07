# Audio-Video Datamosh Script - Frame
# by Marceline / Marc Browning

import wave, os, ffmpeg, imghdr, pedalboard
from pedalboard import Pedalboard # type: ignore
from pedalboard.io import AudioFile # type: ignore

BMP_HEADER_SIZE = 54 # in bytes
WAV_HEADER_SIZE = 46 # in bytes

GLOBAL_SAMPLE_RATE = 44100.0
CHANNEL_NUM = 1
SAMPLE_WIDTH = 2

class Frame:
    # bmp frame
    __slots__ = ["__frame_header", "__data", "__wav_file_name", "__working", "__filename", "__debug"]

    def __init__(self, filename, WAV_FILE_NAME="INPROGRESS.wav", debug=False):
        # open bmp as binary data
        with open(filename, "rb") as f: data = bytearray(f.read())
        # split into header and editable data
        self.__frame_header = data[:BMP_HEADER_SIZE+1]
        self.__data = data[BMP_HEADER_SIZE+1:]
        # define the name of the working wav file
        self.__wav_file_name = WAV_FILE_NAME
        # initialize working state to false
        self.__working = False
        # save the filename for debugging
        self.__filename = filename
        # debug param
        self.__debug = debug
        # if debug: print("filetype: " + imghdr.what(FRAME_DIRECTORY + filename))
    
    def set_working_frame(self):
    # turn frame into current working wav
        bytes_to_wav(self.__data, self.__wav_file_name)
        # set working state to True
        self.__working = True
        # if self.__debug: print("filetype: " + imghdr.what(FRAME_DIRECTORY + self.__filename))

    def audio_datamosh(self, board):
    ## add audio effects to frame
        # check if frame is in working state
        if not self.__working: raise ValueError("Frame " + self.__filename + " not in working state.")
        # read the current working wav
        with AudioFile(self.__wav_file_name) as f: audio = f.read(f.frames)
        # add the effect
        effected = board(audio, GLOBAL_SAMPLE_RATE)  
        # output to the working wav
        with AudioFile(self.__wav_file_name, "w", GLOBAL_SAMPLE_RATE, CHANNEL_NUM) as o: o.write(effected)
        # if self.__debug: print("filetype: " + imghdr.what(FRAME_DIRECTORY + self.__filename))
    
    def export_frame(self):
    ## export the frame, end it from being worked on, and delete the wav.

        # open wav as binary
        with open(self.__wav_file_name, "rb") as f:
            data = bytearray(f.read())
            edited_data = data[WAV_HEADER_SIZE+1:]

        # write the edited data to the frame
        with open(self.__filename, "wb") as f: f.write(self.__frame_header + edited_data)
        # set working state to false
        self.__working = False
        # delete the working wav file
        os.remove(self.__wav_file_name)
        # print debug info
        if self.__debug: print("Frame " + self.__filename + " done!")
        # if self.__debug: print("filetype: " + imghdr.what(FRAME_DIRECTORY + self.__filename))

    def revert_frame(self):
    ## if the frame corrupts, set it back to its original state
        with open(self.__filename, "wb") as f: f.write(self.__frame_header + self.__data)
        
# helper function
# i would make this an inner function to Frame but private classes don't actually exist in Python, so whatever
def bytes_to_wav(data, filename):
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(CHANNEL_NUM)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(GLOBAL_SAMPLE_RATE)
        wav_file.writeframes(data)

# def main():
# ## for debugging
#     my_frame = Frame("testimage.bmp", debug=True)
#     my_frame.set_working_frame()
#     my_frame.audio_datamosh(Pedalboard([pedalboard.Chorus(), pedalboard.Reverb(room_size=0.7), pedalboard.Bitcrush(bit_depth=5)]))
#     my_frame.export_frame()

# if __name__ == "__main__": main()