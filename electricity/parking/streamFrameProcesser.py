from electricity.parking.models import CameraParkingSpot
import numpy as np
import cv2
from PIL import Image

class StreamFrameProcesser:

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
