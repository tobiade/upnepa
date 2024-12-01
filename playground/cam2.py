from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
from picamera2.outputs import FfmpegOutput
import time
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}, controls={"AfMode": 2}))
encoder = H264Encoder()
output = FfmpegOutput("-preset veryfast -tune zerolatency -f hls -hls_time 1 -hls_list_size 3 -hls_flags delete_segments -hls_allow_cache 0 /var/www/html/stream.m3u8")
picam2.start_recording(encoder, output, quality=Quality.LOW)
time.sleep(1000)
picam2.stop_recording()