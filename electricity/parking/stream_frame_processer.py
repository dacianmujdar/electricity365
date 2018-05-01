from electricity.parking.models import CameraParkingSpot, CameraInput
import numpy as np
import cv2
from PIL import Image
import logging

from electricity.predictor.predictor import Predictor


class StreamFrameProcesser:

    @staticmethod
    def refresh_frames():
        for camera in CameraInput.objects.all():
            video = cv2.VideoCapture()
            url = 'https://hddn01.skylinewebcams.com/live.m3u8?a=5tm6kfqrhqbpblan9j5d4bmua4'
            video.open(url)
            success, image = video.read()
            Predictor.predict(image_path='t.png')
            if success:
                for camera_parking_spot in camera.parking_spots.all():
                    upper_left = [camera_parking_spot.upper_right_x + 180, camera_parking_spot.upper_right_y + 100]
                    bottom_right = [camera_parking_spot.bottom_left_x + 180, camera_parking_spot.bottom_right_y + 100]

                    rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                    cv2.imwrite('t.png', rect_img)
                    camera_parking_spot.parking_spot.is_occupied = Predictor.predict(np_array=rect_img)
                    camera_parking_spot.parking_spot.save()
            else:
                logging.error("Failed to open video")
