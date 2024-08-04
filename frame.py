# Audio-Video Datamosh Script
# by Marceline / Marc Browning

import wave, os, ffmpeg
from pedalboard import Pedalboard, Chorus, Reverb # type: ignore
from pedalboard.io import AudioFile # type: ignore

BMP_HEADER_SIZE = 54 # in bytes
WAV_HEADER_SIZE = 46 # in bytes

NUMBER_OF_FRAMES = 906 # number of images, including start and endpoints
FIRST_FILE_NUM = 1;

PARENT_DIRECTORY  = "C:\\Users\\ORION\Downloads\\audioFXonVideoProofofConcept\\"
FRAME_DIRECTORY = PARENT_DIRECTORY + "frames\\"
WAV_DIRECTORY = FRAME_DIRECTORY

GLOBAL_SAMPLE_RATE = 44100.0
CHANNEL_NUM = 1
SAMPLE_WIDTH = 2

class Frame:
    # bmp frame
    __slots__ = ["__frame_header", "__data", "__wav_file_name", "__working", "__filename", "__debug"]

    def __init__(self, filename, WAV_FILE_NAME="INPROGRESS.wav", debug=False):
        # open bmp as binary data
        with open(FRAME_DIRECTORY + filename, "rb") as f: data = bytearray(f.read())
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
    
    def set_working_frame(self):
    # turn frame into current working wav
        bytes_to_wav(self.__data, WAV_DIRECTORY + self.__wav_file_name)
        # set working state to True
        self.__working = True

    def edit_frame(self, board):
    # add audio effects to frame
        # check if frame is in working state
        if not self.__working: raise ValueError("Frame " + self.__filename + " not in working state.")
        # read the current working wav
        with AudioFile(WAV_DIRECTORY + self.__wav_file_name) as f: audio = f.read(f.frames)
        # add the effect
        effected = board(audio, GLOBAL_SAMPLE_RATE)  
        # output to the working wav
        with AudioFile(WAV_DIRECTORY + self.__wav_file_name, "w", GLOBAL_SAMPLE_RATE, CHANNEL_NUM) as o: o.write(effected)
    
    def export_frame(self):
    # export the frame, end it from being worked on, and delete the wav.

        # open wav as binary
        with open(WAV_DIRECTORY + self.__wav_file_name, "rb") as f:
            data = bytearray(f.read())
            edited_data = data[WAV_HEADER_SIZE+1:]

        # write the edited data to the frame
        with open(FRAME_DIRECTORY + self.__filename, "wb") as f: f.write(self.__frame_header + edited_data)
        # set working state to false
        self.__working = False
        # delete the working wav file
        os.remove(WAV_DIRECTORY + self.__wav_file_name)
        # print debug info
        if self.__debug: print("Frame " + self.__filename + " done!")

    def revert_frame(self):
    # if the frame corrupts, set it back to its original state
        with open(FRAME_DIRECTORY + self.__filename, "wb") as f: f.write(self.__frame_header + self.__data)

# helper function
# i would make this an inner function to Frame but private classes don't actually exist in Python, so whatever
def bytes_to_wav(data, filename):
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(CHANNEL_NUM)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(GLOBAL_SAMPLE_RATE)
        wav_file.writeframes(data)

class Video:
    # a video stream
    __slots__ = ["__stream"]
    def __init__(self, filename):

        

#### old code ####

# def edit_file(filename):
#     # open bmp as binary data
#     with open(filename, "rb") as f:
#         data = bytearray(f.read())
#     # split into header and editable data
#     header = data[:BMP_HEADER_SIZE+1]
#     edit_data = data[BMP_HEADER_SIZE+1:]
#     # turn into a wav file
#     bytes_to_wav(edit_data, CURRENT_DIRECTORY + WAV_FILE_NAME)
#     # add effects and re-export wav file
#     board = Pedalboard([Chorus(), Reverb(room_size=0.25)])
#     with AudioFile(CURRENT_DIRECTORY + WAV_FILE_NAME) as f:
#         audio = f.read(f.frames)
#         effected = board(audio, 44100.0)  
#     with AudioFile(CURRENT_DIRECTORY + WAV_FILE_NAME, "w", 44100.0, 1) as o: o.write(effected)
#     # open wav as binary
#     with open(CURRENT_DIRECTORY + WAV_FILE_NAME, "rb") as f:
#         data = bytearray(f.read())
#         edited_data = data[WAV_HEADER_SIZE+1:]
#     # export
#     with open(filename, "wb") as f:
#         f.write(header + edited_data)
#     # frame done
#     print("frame done!")

def pad_filename(current_frame, MAX_STR_SIZE = 3):
    """Add zeroes to the start of the filename if needed."""
    result = str(current_frame)
    while len(result) != MAX_STR_SIZE: result = "0" + result
    return result

def main():
    for i in range(NUMBER_OF_FRAMES):
        current_filename = CURRENT_DIRECTORY + pad_filename(i+FIRST_FILE_NUM) + ".bmp"
        edit_file(current_filename)


if __name__ == "__main__": main()