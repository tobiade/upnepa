import time
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import controls
import redis
import io

from constants import LED_STREAM_CHANNEL

class StreamingOutput(io.BufferedIOBase):
    def __init__(self, redisUrl: str):
        self.frame = None
        self.redisClient = redis.from_url(redisUrl)

    def write(self, buf):
        self.frame = buf
        self.redisClient.publish(LED_STREAM_CHANNEL, buf)
        # print("published frame")

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
output = StreamingOutput('redis://159.65.93.235')
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    # Keep the program running to continue capturing frames
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Handle graceful shutdown on interrupt
    print("Stopping recording...")
finally:
        picam2.stop_recording()

# if __name__ == "__main__":
#     main()