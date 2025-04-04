from time import sleep
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

cam = Picamera2()
encoder = H264Encoder(bitrate=50_00_000)
config = cam.create_still_configuration()
cam.configure(config)
cam.start()
cam.capture_file("img.jpeg")
cam.stop()

config = cam.create_video_configuration()
cam.configure(config)
cam.start()
cam.start_recording(encoder, "vid.h264")
sleep(10)
cam.stop_recording()
cam.stop()
