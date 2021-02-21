import picamera
import time

def start_frame_capture():
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = (1280, 720)

        while True:
            camera.capture("video_capture/frame.jpeg")

        return 0
