import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np
import argparse



def main():
    parser = argparse.ArgumentParser(description="folder")
    parser.add_argument("-f", metavar='F', type=str,
                        help="add folder to store images")

    args = parser.parse_args()
    folder = ""
    if( len(args.f) > 0 ):
        folder = args.f

    # Start a socket listening for connections on 0.0.0.0:8000
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    counter = 1
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream).convert('RGB')
            image.save('../images/' + folder + '/' + str(counter).zfill(6) + '.jpg')
            counter +=1
    finally:
        connection.close()
        server_socket.close

    return 0

if __name__ == "__main__":
    main()