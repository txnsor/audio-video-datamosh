import struct
FILEPATH = "C:\\Users\\ORION\\Downloads\\audio-video-datamosh\\testing\\test-image.bmp"
# reminder: bmp header is little endian-- lsb is first

def main():
    with open(FILEPATH, "rb") as f: data = bytearray(f.read())
    print("file path: " + FILEPATH)
    print(f"file type: {data[0:2].decode('ascii')}") # should return BM
    print(f"file size: {int.from_bytes(data[2:6], 'little')} bytes")
    print(f"bmp header offset: {int.from_bytes(data[10:14], 'little')} bytes")

if __name__ == "__main__": main()
