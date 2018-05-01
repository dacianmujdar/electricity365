from electricity.parking.models import CameraParkingSpot, CameraInput
import numpy as np
import cv2
from PIL import Image
import logging

from electricity.predictor.predictor import Predictor


class StreamFrameProcesser:

    @staticmethod
    def refresh_frames():

        video = cv2.VideoCapture()
        for camera in CameraInput.objects.all():
            url = 'https://video-weaver.fra02.hls.ttvnw.net/v1/playlist/CoMDFwvHqS_MIl2ZKYbvKUmDk-tblOiYDzyHH1LK6uLZiE8hrGgVxW4rtmwvAwnuCELm1bxuBi8DWFU6DAdScOtM7EFCruf-Rb8CJEUdiJVB-2_nqOhTzmCE-z1CaC_h0TKKGsQOWguqedVK2D7pXTKP_RBf60jEy0A0_Us0Q-XA8D8h17A4g-Dxxuc_D7aqjGQht-Jva07MvVclg-4T5J2a65INSxjmcDClRGOc8g38bUV-SiMai3WdZz2aCLNHawT1i1BxcezHNGwW7jySQKmrW5jO1BXOa8JA6G80P_t0opR9qrLaalDu2HGSO1TS-rEVLUjzkb0JzT45_SiLfhc2hvBcXdIpGnWG98cQC-vxm-SoKbfuvFz9PBHIIYgsAhcJKGcwSsR95ASuuzo5nIu0hUgJDZvLRqcYyM-qFjf3LgrEsSqv3eJVUE1bNQDghOjxbHJqaEXECIoYzfIG9bN-wddwolo8Ax3WYL8ax1AgBUvmWllkv8s-SpYs7TgtYo-OMJtjEhCNFqmPkzrH2qCLScxL_GorGgzJJgi4Q7-rMmPfjCY.m3u8'
            video = cv2.VideoCapture()
            video.open(url)
            success, image = video.read()
            if not success:
                logging.error("Failed to open video")
            for camera_parking_spot in camera.parking_spots.all():
                upper_left = [camera_parking_spot.upper_right_x + 180, camera_parking_spot.upper_right_y + 100]
                bottom_right = [camera_parking_spot.bottom_left_x + 180, camera_parking_spot.bottom_right_y + 100]

                rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                cv2.imwrite('t.png', rect_img)
                camera_parking_spot.parking_spot.is_occupied = Predictor.predict(np_array=rect_img)
                camera_parking_spot.parking_spot.save()
