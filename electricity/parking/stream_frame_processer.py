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
            url = 'https://video-weaver.fra02.hls.ttvnw.net/v1/playlist/CoMD2YW4YVAR8uKgwZJ-g1SnEj30geTJyIjZjKWAKbdJtI6t8LI4NE4h_VpfKgvZ9zhrgnPyHgR6ktuqVCOYn_B4kWaq-cgvZXts-39-cK2QyyRKB9VxTGj4okfQ4Xv_M60SofZzTLd_zuzU87u8WL6WXDDjqo6Z7F2__4pXu0hMCyFeC5a33F1jITUJ8cFzeoPg0CKRK2Kbk4Rh8DSY2YjxPPPt8DAywiN5bMDBpEpvLdqdL76lbdMuV_pa1DV56t-25kp3SoAGuUjPaVb6cdBRX3z2rUzip_NoRyX2WZIOC9n52wPNbwh9hUI7_F59fjnkOaWexEQAOgToE19YIE9AfC_V04GQAMS1thyOdVNeD4PzidqueROXzdiVX3wZYTgFisr3kypqkh0nceMeRrSoWemYtnSwbRShzBs51yZPVcJKhYexvcNW4uC88Z2iZDVyroXYJPgtFOCaAu6NuuMM-kBHVzFzpWZEpK3Bfqn2-5sv_I76mTp_gX-64M09hmZRH-XiEhCUzygeNns0I8dlbYACCMWvGgye57gwe1RXPTFomfA.m3u8'
            video = cv2.VideoCapture()
            video.open(url)
            success, image = video.read()
            if success:
                for camera_parking_spot in camera.parking_spots.all():
                    upper_left = [camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y]
                    bottom_right = [camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_right_y]

                    rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]

                    camera_parking_spot.parking_spot.is_occupied = Predictor.predict(rect_img)
                    camera_parking_spot.parking_spot.save()

