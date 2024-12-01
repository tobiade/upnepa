from fileinput import filename
import time
from picamera2 import Picamera2
from libcamera import controls
picam2 = Picamera2()
# picam2.start(show_preview=True)
# # picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})
# picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

filename = "test_image5.jpg"
# Configure the camera for still capture with maximum resolution
config = picam2.create_still_configuration(
    main={"size": (1920, 1080)},  # Adjust to the highest supported resolution
    controls={
        # "AeEnable": True,       # Enable Auto Exposure
        # "AwbEnable": True,      # Enable Auto White Balance
        # "ExposureTime": 10000,  # Adjust exposure time (in microseconds)
        # "AnalogueGain": 1.0,    # Set Analog Gain to minimum
        # "ColourGains": (1.0, 1.0)  # Neutral White Balance
        "AfMode": controls.AfModeEnum.Continuous,           # Set Auto Focus to Continuous
        "AwbMode": controls.AwbModeEnum.Auto,  # Set Auto White Balance to Auto
        "Sharpness": 4,
        # "HdrMode": controls.HdrModeEnum.MultiExposure,
    }
)
print(config['controls'])
    
picam2.configure(config)
picam2.start()

# Allow the camera to adjust settings
time.sleep(2)

# Capture the image
picam2.capture_file(filename)
picam2.stop()
print(f"Captured image saved as {filename}")

