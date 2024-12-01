# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import socketserver
from http import server
import subprocess
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import Quality,H264Encoder
from picamera2.outputs import FileOutput
from libcamera import controls
import time

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<video width="1920" height="1080" controls>
  <source src="http://192.168.0.225:8000/stream" type="video/mp4">

Your browser does not support the video tag.
</video>
</body>
</html>
"""


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()
        self.total_bytes = 0

    def write(self, buf):
        with self.condition:
            self.frame = buf
            # print("Length of frame: ", len(buf))
            self.total_bytes += len(buf)
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream':
            # self.send_response(200)

            # DataChunkSize = 10000

            # command = 'gst-launch-1.0 -e -q fdsrc fd=0 ! video/x-h264,width=1920,height=1080,framerate=30/1,stream-format=byte-stream ! h264parse config-interval=1 ! h264timestamper ! mp4mux streamable=true fragment-duration=10 presentation-time=true ! filesink location=/dev/stdout'
            # print("running command: %s" % (command, ))
            # p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=-1, shell=True)
            # # Set the stdout to non-blocking mode
            # fd = p.stdout.fileno()
            # fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            # fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

            # print("starting polling loop.")
            # while True:
            #     with output.condition:
            #         output.condition.wait()
            #         # Send the input data to the subprocess
            #         p.stdin.write(output.frame)
            #         p.stdin.flush()  # Ensure the data is sent immediately

            #         try:
            #             stdoutdata = p.stdout.read(DataChunkSize)
            #             if stdoutdata:
            #                 print("Read data from stdout")
            #                 self.wfile.write(stdoutdata)
            #                 print(f"Wrote {len(stdoutdata)} bytes")
            #             else:
            #                 print("No data available yet")
            #         except BlockingIOError:
            #             # No data available yet
            #             print("No data available yet")
            #             pass
            self.send_response(200)

            DataChunkSize = 10000

            command = '(echo "--video boundary--"; libcamera-vid --width 1920 --height 1080 --framerate 30 --profile high --nopreview --timeout 0 --output -;) | gst-launch-1.0 -e -q fdsrc fd=0 ! video/x-h264,width=1920,height=1080,framerate=30/1,stream-format=byte-stream ! h264parse ! mp4mux streamable=true fragment-duration=10 presentation-time=true ! filesink location=/dev/stdout'
            print("running command: %s" % (command, ))
            p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=-1, shell=True)

            print("starting polling loop.")
            while(p.poll() is None):
                print("looping... ")
                stdoutdata = p.stdout.read(DataChunkSize)
                self.wfile.write(stdoutdata)

            print("Done Looping")

            print("dumping last data, if any")
            stdoutdata = p.stdout.read(DataChunkSize)
            self.wfile.write(stdoutdata)
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}, controls={
        # "AeEnable": True,       # Enable Auto Exposure
        # "AwbEnable": True,      # Enable Auto White Balance
        # "ExposureTime": 10000,  # Adjust exposure time (in microseconds)
        # "AnalogueGain": 1.0,    # Set Analog Gain to minimum
        # "ColourGains": (1.0, 1.0)  # Neutral White Balance
        "AfMode": controls.AfModeEnum.Continuous,           # Set Auto Focus to Continuous
        "AwbMode": controls.AwbModeEnum.Auto,  # Set Auto White Balance to Auto
        "Sharpness": 4,

    }))
output = StreamingOutput()
# picam2.start_recording(JpegEncoder(q=100), FileOutput(output), quality=Quality.VERY_HIGH)
picam2.start_recording(H264Encoder(), FileOutput(output), quality=Quality.VERY_HIGH)
try:
    start_time = time.time()
    print("Start time:", start_time)
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    picam2.stop_recording()
    elapsed = time.time() - start_time
    print("Total time:", elapsed)
    print("Total bytes:", output.total_bytes)
    print("Average bitrate:", output.total_bytes * 8 / elapsed / 1000, "kbps")