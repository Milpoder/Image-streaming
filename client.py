import io
import socket
import struct
import time
import picamera
import glob, sys
from PIL import Image


WIDTH  = 320
HEIGHT = 200

def main():

    if( len(sys.argv) < 2 ):
        return -1

    # Connect a client socket to my_server:8000
    client_socket = socket.socket()
    client_socket.connect(('server_ip', 8000))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        if(sys.argv[1] == "camera"):
            with picamera.PiCamera() as camera:
                camera.resolution = (WIDTH, HEIGHT)
                # Start a preview and let the camera warm up for 2 seconds
                camera.start_preview()
                time.sleep(2)
                #Start recoding
                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg'):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    connection.write(stream.read())
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        else:
            path = "images/test/" + sys.argv[1] + "/img1/"
            dirs = sorted(glob.glob(path + '*.jpg'))

            # This would print all the files and directories
            stream = io.BytesIO()
            for file in dirs:
                im = Image.open(file)
                #im.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
                im.save(stream,'png')
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()

    finally:
        connection.close()
        client_socket.close()

    return 0

if __name__ == "__main__":
    main()
