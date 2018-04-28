from electricity.parking.models import CameraParkingSpot, CameraInput
import numpy as np
import cv2
from PIL import Image

from electricity.predictor.predictor import Predictor


class StreamFrameProcesser:

    @staticmethod
    def refresh_frames():
        video = cv2.VideoCapture()
        for camera in CameraInput.objects.all():
            #url = camera.url
            url = 'https://video-weaver.fra02.hls.ttvnw.net/v1/playlist/CvkCDghgcHyWpBUqrjjn9OZNif3HWlstL9-GNPc6fGZJoG6C3pm5s64O1Yd-Wktrgn8diMYjjaP84n1E8Noyr3rzgKoqb-aMroNnmu-zUArJ3sZvJzJTtTRyf0xC7kbQhlQI1yRjo_WtyrJ7uTbuOwCCyZuF8FeW1_glhLRtQ-wfUDFYLXO7AA5lOmW-jV1Ve7PNyCr3DHRgHVPGOkMtgVcC9_0Xw1-DKAZo4uIz8PUWQBDlnInKbsZJHD37g8goNz7jHzUvZnbxxEa1N83_79OTHw3t9lZWp7ZjF9Kx2tqNSKRc5ZGZQAEStY05lOnAsm4CFUTIiX6jmeLHuJb9VDdFliQ3Pan3pjhmkuggqqlQMe47arKzj5ZUH7iYOqgdtgQM4lYc1KGdBQDW3OSALjMNjB3mYXEZcfGJKWjgOqmrqf3lV4wuzWd4FCs0cpd9MWR1Df1ktQc1n7iawpBOSYvgAdZZOOPcx7KsQeZPLgGXdad0Eb02nhaf8cwSENqKVUHA3ULGOjlXEnfGilUaDL_FGze6o47p-0dsig.m3u8'
            video = cv2.VideoCapture()
            video.open(url)
            success, image = video.read()
            for camera_parking_spot in camera.parking_spots.all():
                upper_left = [camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y]
                bottom_right = [camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_right_y]
                rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                camera_parking_spot.parking_spot.is_occupied = Predictor.predict(rect_img)
                camera_parking_spot.parking_spot.save()

                cv2.imwrite('imgRect.png',rect_img)

    @staticmethod
    def processFrame(imgPath):
        spots = CameraParkingSpot.objects.all()
        digitalImg = np.array(Image.open(imgPath))

        for spot in spots:
            # draw in the image
            upper_left = [spot.upper_left,spot.upper_right]
            bottom_right = [spot.bottom_left, spot.bottom_right]
            cv2.rectangle(digitalImg, upper_left, bottom_right, (0, 255, 0), 2)
            rect_img = digitalImg[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]

        cv2.imshow('img', digitalImg)
