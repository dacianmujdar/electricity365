import PIL
from django.utils import timezone

from electricity.parking.models import ParkingSpot, CameraInput
import numpy as np
import urllib
import cv2
import imutils
from PIL import Image
import logging
from math import cos, sin, pi
from background_task import background


from electricity.predictor.predictor import Predictor, NN_INPUT_SIZE

RED = (0, 0, 255)
GREEN = (0, 255, 0)


def returnFrameThroughStream(url):
    video = cv2.VideoCapture()
    video.open(url)
    success, image = video.read()
    return success, image


def returnFrameThroughPoolling(url):
    url_response = urllib.urlopen(url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    return True, img


@background()
def refresh_frames():
    logging.info("Refreshing frames")
    for camera in CameraInput.objects.filter(is_active=True):
        if camera.is_stream:
            success, image = returnFrameThroughStream(camera.url)
        else:
            success, image = returnFrameThroughPoolling(camera.url)
        if success:
            for camera_parking_spot in camera.parking_spots.all():
                try:
                    upper_left = [camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y]
                    bottom_right = [camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_right_y]

                    #rect_img = image[upper_left[0]: bottom_right[0], upper_left[1]: bottom_right[1]]
                    rect_img = image[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
                    cv2.imwrite('partial.png', rect_img)
                    camera_parking_spot.is_occupied = Predictor.predict(image_path="partial.png")
                    camera_parking_spot.save()

                    if camera_parking_spot.is_occupied:
                        cv2.rectangle(image, tuple(upper_left), tuple(bottom_right), RED, 2)
                    else:
                        cv2.rectangle(image, tuple(upper_left), tuple(bottom_right), GREEN, 2)
                except:
                    pass
            cv2.imwrite('static/parking{}.png'.format(camera.id), image)

        else:
            logging.error("Failed to open video")
    logging.info("Frame processing cycle completed")


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
