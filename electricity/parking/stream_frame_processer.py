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
            url = 'https://video-weaver.lhr03.hls.ttvnw.net/v1/playlist/CoIDSHsQDAonb1oIcYRvzPf2qCidU4J7qMQwoTZ3Ow-5pOvCEXQlezpQbCbJl6Bau1k2vr-pircxy4VUaV-bYdVC7GMqEECN8JJR3FbD__QO2mLVAK5S5RLoikAx1YuET_aYwU9aLlfhEQ7-HIKQ6HzAj_VG7yFLF087HbaDgHi_19UWSAJL3u6XnFeOlWacnXImtqoW9ZkQDLCMnjDv60y8CG3UUXFVOtdxf6axxbeklRfu9B-ha5ZRPIYb5rjsg69N90sjVGIzcq0IVAHlXGABEDEaPGi2Vb5btfo-4-9ONfqvSc8gxlOkPRfzH85_XVO5wdiYhqjd9bhaRiYKqD_iGSTSosWhznHyIXqW4VLBu48BLzapqUXaNI77oKsnJFBO2dqmHMXodJKm4E5jjpOKoe2nE0mOjVBOLvxYxolFPdASpBk4GLDjhf92oTmuCDdwY1rz065DA6YFmqIiNieTCtdBJCI_c7tzVy3J9xBaxbDvnzy1G9EtZc6FrJ-zF4VMW70SEGtstqBlRIAPDn6QPeW_1XYaDLglT88WNqIxt0AG4A.m3u8'
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

