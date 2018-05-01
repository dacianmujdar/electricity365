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
            video = cv2.VideoCapture()
            url = "https://video-weaver.cdg02.hls.ttvnw.net/v1/playlist/CoMD69PS9fTrFfErZIkqqJTfZ_SKxP4R1CzsRzAG1rMNXies_LNjpFDGml-J-ULdd0bjFYF98sU3AnG_yYYzyXon25u_p7M0lL4t1olN8IkpdYnwJr-OVGVa3aT-qz5V8yeoblEQWK32Jj0sv6e9WpAqFAG-Ou4vIy2fkXh0BQXNJmRfxvRcdimSWTFbPdupeByqGZu9RwCv86ek5Q0t2-FtHKQY1Me-LMKQJHDH56aoAk1_whtEaquFNH-JLTMITFEGgU2x9wpdsXuU7j4hqnQeIsPM1JbQ-dwSjRmBQilLy6v_FX-Q9qatKdRfeFyWd-H81JIe6ElyioPr0UvgBRmKS86op2p03YgWd-kzD7niv8tZDY8JdzYJ7SEPyKOILWbxHbA9B2V4qAoH_0lVX-9C3eSQqDRax4KbPNhMmi44QFGS_ApPtH1yINGR8MzKwYRWzmjJw9pq_GuCs8qu7mCBh7V-xBh_mKfRq1C-ZArcKJPnxZls9W0MyFTDS31kvy6G7P7dEhB9oePJmNzFZClo0MXfpCNyGgypAqoU-d2hU3nBang.m3u8"
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
