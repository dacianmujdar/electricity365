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
            url = 'https://video-edge-c680d4.fra02.hls.ttvnw.net/v1/segment/CoYDvvC9CL6PE6Y7yRYCGxpFpgJE72l7Krv_Ey_BKT3dwjZToJzaFIvBDbN1ATonFKbiIofn4Lu8F55Fc98vq8tZykZq0Rfge_87fA-VkDU0xBmUS-0EGkJ7NXVA9ZEQqrza1mUgKRJZKYEHn4F8yZEc94NCntWOn776gX1mJhG4l8H7XaTr4B-p3l2NWU-aOo3fj5YA2iMhDjkenSkqPNymyPKfOm28jGAbODiVNBlqSO5b76PUPRjZhB8npzcYMhn6BtJT-jV4oeN4hvbcS5DamlvTMFo77CehzqRCqSuRyon5auLipmkzYtrW0ClMUwUjCJHGVtK5ZzcHXzF-7DDqJ0DE6P9gmmEOkdKidh0AKTManDQ61zxpmGn5lWP9pvNQawS-Frg1J0U2lKp9eWoj8FdEsv1CO8xC0nvxS88S2lF8jgKzUzQcrF1bsYXmsdhRbS_76YQsAnKlNxVGLKADMZQqV_ZQ6bMwasocHOV42UU7y0fNHWUMT3c28DJRVpVHzAOXttE1EhDnwE5hoOTKU_jUX-ekEbM8GgwOLiD72wzxBhaq3-E.ts'
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
