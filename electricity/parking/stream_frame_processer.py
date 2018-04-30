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
            url = 'https://video-weaver.lhr03.hls.ttvnw.net/v1/playlist/CoMDm3zntZ6qhdxFlBnYIrM9eOey1lf4c1K_oGsVNf8CzZFU3JTRoRvCzvIafdGqqzBvtbo0wJEzq7Mx9d0maGy-XL-lE60-yGTNfiTcEWat_S9B3jzmRR4lm2EGG6KwYZfMSE60kylitxlWVzYQPdZ3Ooi0nuMFrcYMcpOcwVfdHYm9oirb0tZiTmQVpQJ_bgddfUuDhU6MGOBL545nAvkUm7hub4TD_PR6bUCChVGfENoyoIP9SR3s4opK3c6-stMI4HDiDRv3FF1WUsKwK5kpKH_muzr5ZiFuBQSZH67LTZhnLP4138mA5vJqrLsCBUzTKDNzjzfmFDyY_UWnX7a6ihSa_Bpb_XUvxQjYpygY3YSuzu5iWpwjJXgBg8GUTw_9ARgURB09hzGo1Ct2wOLBEbnKA4tniVmQChjD64QpbXuI-8Ww20caJmEHKLSCT2QDVVXlOl4Qk1xWHKffs1dEplnJkmUZ7xr9wCZD8AyPoSAGIttPNIgeXhL20Gw2JgdNP0CwEhDEcyHXkeOPvAuWm2DWfhWQGgyLZkYnPq0mDUnB8cs.m3u8'
            video = cv2.VideoCapture()
            video.open(url)
            success, image = video.read()
            if success:
                for camera_parking_spot in camera.parking_spots.all():
                    upper_left = [camera_parking_spot.upper_right_x + 180, camera_parking_spot.upper_right_y + 100]
                    bottom_right = [camera_parking_spot.bottom_left_x + 180, camera_parking_spot.bottom_right_y + 100]

                    rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                    cv2.imwrite('t.png', rect_img)
                    camera_parking_spot.parking_spot.is_occupied = Predictor.predict(np_array=rect_img)
                    camera_parking_spot.parking_spot.save()

