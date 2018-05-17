from django.utils import timezone

from electricity.parking.models import CameraParkingSpot, CameraInput
import numpy as np
import cv2
import imutils
from PIL import Image
import logging
from math import cos, sin, pi
from background_task import background



from electricity.predictor.predictor import Predictor

RED = (0, 0, 255)
GREEN = (0, 255, 0)


@background()
def refresh_frames():
    logging.info("Refreshing frames")
    for camera in CameraInput.objects.all():
        video = cv2.VideoCapture()
        video.open(camera.url)
        success, image = video.read()
        if success:
            for camera_parking_spot in camera.parking_spots.all():
                camera_parking_spot = camera.parking_spots.first()
                upper_left = (camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y)
                bottom_right = (camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_right_y)

                #rect_img = imutils.rotate_bound(image, camera_parking_spot.rotation_angle)[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                #rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]

                center = (832, 670)
                theta = 40
                width = 105
                height = 164
                simage = subimage(image, center=center, theta=theta, width=width, height=height)
                cv2.imwrite('partial.png', simage)

                camera_parking_spot.parking_spot.is_occupied = Predictor.predict(image_path="partial.png")
                camera_parking_spot.parking_spot.save()

                rect_points = [
                    [center[0] - height / 2 * cos(theta) - width / 2 * sin(theta), center[1] - height / 2 * sin(theta) + width / 2 * cos(theta)],
                    [center[0] + height / 2 * cos(theta) - width / 2 * sin(theta), center[1] + height / 2 * sin(theta) + width / 2 * cos(theta)],
                    [center[0] + height / 2 * cos(theta) + width / 2 * sin(theta), center[1] + height / 2 * sin(theta) - width / 2 * cos(theta)],
                    [center[0] - height / 2 * cos(theta) + width / 2 * sin(theta), center[1] - height / 2 * sin(theta) - width / 2 * cos(theta)]

                ]

                if camera_parking_spot.parking_spot.is_occupied:
                    cv2.polylines(image, np.int32([rect_points]), True, RED, 2)
                    #cv2.rectangle(image, upper_left, bottom_right, RED, 1)
                else:
                    cv2.polylines(image, np.int32([rect_points]), True, GREEN, 2)

            cv2.imwrite('static/parking{}.png'.format(camera.id), image)
        else:
            logging.error("Failed to open video")


def subimage(image, center, theta, width, height):

   '''
   Rotates OpenCV image around center with angle theta (in deg)
   then crops the image according to width and height.
   '''

   # Uncomment for theta in radians
   #theta *= 180/np.pi

   shape = image.shape[:2]

   matrix = cv2.getRotationMatrix2D(center=center, angle=theta, scale=1)
   image = cv2.warpAffine(src=image, M=matrix, dsize=shape)

   x = int(center[0] - width/2)
   y = int(center[1] - height/2)

   image = image[y:y+height, x:x+width]
   return image
