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
            url = "https://video-weaver.fra02.hls.ttvnw.net/v1/playlist/CoMDcSbBLQvLi-jB93IEJuacqAPadhDoXFdDEpSJfzFpx9iNchykWSrIaVVGnnTqyojZOegr3AbHJAkFxPjPtnSP8y3dN3jNPrwHVzLKALSRf1X6POzYcAYMdOAbjwjOeDqR3KawFcEkq6xHWXguyfupOOFJcszrymr0Pect-3Yjv2vt1mAugQdcHNY3r2VlzBcYwyLmPT6kj9QnKVtmlT20sAJJIMuGeCf_-oD9Tk-4hWDOG9JSvPQr3g-iitFdAp_40aJcTWT1rw6MQwOUq_K_mU_SkW7DtjunQ7lYPutHI0QNR0tK0qBtZJjfPPNGhRT2afbRq3nR6ncp1qQgpK8KENi0huRJOP5fzaCDJyDC9g2Pe4fZdIbiaOu4F_genlmr_WYxmvd94E_DSWJ5aaeEIy-GDN3uRJWZoe667PormmKpi40i0WO3sdodvyBpaxf7RZ7G3siObaHt_6Ig5paAdNZBNE7vJ0dwF39g9v_IppUwT-W_4mVEv-EHUS4TqYLcf08mEhCpCnOCa_uDaaXKKsIh7hWJGgwbqvUilAu2VF5QCrk.m3u8"
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
