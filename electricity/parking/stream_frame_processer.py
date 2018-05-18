import PIL
from django.utils import timezone

from electricity.parking.models import CameraParkingSpot, CameraInput
import numpy as np
import cv2
import imutils
from PIL import Image
import logging
from math import cos, sin, pi
from background_task import background


from electricity.predictor.predictor import Predictor, NN_INPUT_SIZE

RED = (0, 0, 255)
GREEN = (0, 255, 0)

@background()
def refresh_frames():
    logging.info("Refreshing frames")
    for camera in CameraInput.objects.filter(is_active=True):
        video = cv2.VideoCapture()
        video.open(camera.url)
        success, image = video.read()
        if success:
            for spot in camera.parking_spots.all():

                # crop the rectangle
                simage = subimage(image, center=(spot.center_x, spot.center_y), theta=spot.rotation_angle,
                                  width=spot.width, height=spot.height)
                cv2.imwrite('partial.png', simage)
                # make the prediction
                spot.parking_spot.is_occupied = Predictor.predict(image_path="partial.png")
                spot.parking_spot.save()

                # define the 4 points of tilted rectangle
                rect_points = [
                    [spot.center_x - spot.width / 2 * cos(spot.rotation_angle) - spot.height / 2 * sin(spot.rotation_angle),
                     spot.center_y - spot.width / 2 * sin(spot.rotation_angle) + spot.height / 2 * cos(spot.rotation_angle)],

                    [spot.center_x + spot.width / 2 * cos(spot.rotation_angle) - spot.height / 2 * sin(spot.rotation_angle),
                     spot.center_y + spot.width / 2 * sin(spot.rotation_angle) + spot.height / 2 * cos(spot.rotation_angle)],

                    [spot.center_x + spot.width / 2 * cos(spot.rotation_angle) + spot.height / 2 * sin(spot.rotation_angle),
                     spot.center_y + spot.width / 2 * sin(spot.rotation_angle) - spot.height / 2 * cos(spot.rotation_angle)],

                    [spot.center_x - spot.width / 2 * cos(spot.rotation_angle) + spot.height / 2 * sin(spot.rotation_angle),
                     spot.center_y - spot.width / 2 * sin(spot.rotation_angle) - spot.height / 2 * cos(spot.rotation_angle)]

                ]

                # add the tilted rectangle on image
                if spot.parking_spot.is_occupied:
                    #cv2.circle(image, (spot.center_x, spot.center_y), min(spot.width/2, spot.height/2), RED, 2)
                    cv2.polylines(image, np.int32([rect_points]), True, RED, 2)

                else:
                    #cv2.circle(image, (spot.center_x, spot.center_y), min(spot.width/2, spot.height/2), GREEN, 2)
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
   theta = 30
   aux = width
   width = height
   height = aux

   shape = image.shape[:2]

   matrix = cv2.getRotationMatrix2D(center=center, angle=theta, scale=1)
   image = cv2.warpAffine(src=image, M=matrix, dsize=shape)

   x = int(center[0] - width/2)
   y = int(center[1] - height/2)

   image = image[y:y+height, x:x+width]
   return image
