from electricity.parking.models import CameraParkingSpot, CameraInput
import numpy as np
import cv2
from PIL import Image
import logging

from electricity.predictor.predictor import Predictor

RED = (0, 0, 255)
GREEN = (0, 255, 0)


class StreamFrameProcesser:

    @staticmethod
    def refresh_frames():
        for camera in CameraInput.objects.all():
            video = cv2.VideoCapture()
            video.open(camera.url)
            success, image = video.read()
            if success:
                for camera_parking_spot in camera.parking_spots.all():
                    upper_left = [camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y]
                    bottom_right = [camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_right_y]

                    rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                    cv2.imwrite('partial.png', rect_img)

                    camera_parking_spot.parking_spot.is_occupied = Predictor.predict(image_path="partial.png")
                    camera_parking_spot.parking_spot.save()

                    if camera_parking_spot.parking_spot.is_occupied:
                        cv2.rectangle(image, tuple(upper_left), tuple(bottom_right), RED, 2)
                    else:
                        cv2.rectangle(image, tuple(upper_left), tuple(bottom_right), GREEN, 2)
                cv2.imwrite('static/parking{}.png'.format(camera.id), image)
            else:
                logging.error("Failed to open video")
