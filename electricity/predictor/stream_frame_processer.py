from __future__ import division
import PIL
import numpy as np
from PIL import Image, ImageDraw
import requests
from keras.models import model_from_json
import datetime

from electricity.celery import app
from io import BytesIO

from electricity.parking.models import CameraInput, ParkingSpot

NN_INPUT_SIZE = (64, 64)


def return_frame_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


class Predictor:
    _neural_network_predictor = None

    @classmethod
    def load_model(cls):
        if not cls._neural_network_predictor:
            # load json and create model
            json_file = open('electricity/predictor/neural_network/model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            cls._neural_network_predictor = model_from_json(loaded_model_json)
            # load weights into new model
            cls._neural_network_predictor.load_weights("electricity/predictor/neural_network/model.h5")

        return cls._neural_network_predictor

#
# @app.task()
def refresh_frames(cycle):
    print("--------------------- Start refresh frame cycle {} ---------------------".format(cycle))
    neural_network_predictor = Predictor.load_model()
    print("--------------------- {} cameras detected ---------------------".format(CameraInput.objects.count()))

    for camera in CameraInput.objects.all():
        # Get the image
        image = return_frame_from_url(camera.url)

        # Detect parking spots
        analyze_parking_spots(camera, image, neural_network_predictor)

        # Detect parking lanes
        analyze_parking_lanes(camera, image, neural_network_predictor)

        camera.last_updated = datetime.datetime.now()

    print("--------------------- Finish refresh frame cycle {} ---------------------".format(cycle))
    #refresh_frames.apply_async((cycle + 1,), countdown=5)


def analyze_parking_spots(camera, image, neural_network_predictor):
    for camera_parking_spot in camera.parking_spots.all():
        try:
            # crop the image
            rect_img = image.crop((camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y,
                                   camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_left_y))

            # resize to the accepted input of the neural network NN_INPUT_SIZE
            resized_image = rect_img.resize(NN_INPUT_SIZE, PIL.Image.ANTIALIAS)

            # make prediction
            camera_parking_spot.is_occupied = \
            neural_network_predictor.predict(np.array(resized_image).reshape(1, 64, 64, 3))[0][0] == 1
            camera_parking_spot.save()

        except Exception as e:
            print("--------------------- exception occured {} ---------------------".format(e))
            pass


def analyze_parking_lanes(camera, image, neural_network_predictor):
    for parking_lane in camera.parking_lanes.all():
        try:
            NR_RECTANGLES = 10
            for index in range(1, NR_RECTANGLES + 1):
                distance_ratio = index / NR_RECTANGLES
                x_up, y_up = parking_lane.get_point_at_distance_ratio_up(distance_ratio)

                width = min(parking_lane.right_width, parking_lane.left_width) + \
                        abs(parking_lane.right_width - parking_lane.left_width) * ((NR_RECTANGLES - index) / NR_RECTANGLES)
                width = int(width)
                distance_to_second_point = int(parking_lane.get_distance_up() * distance_ratio + width)
                x2_up, y2_up = parking_lane.get_point_at_distance_ratio_up(distance_to_second_point / parking_lane.get_distance_up())

                x_down, y_down = parking_lane.get_point_at_distance_ratio_down(distance_ratio)

                distance_to_second_point = int(parking_lane.get_distance_down() * distance_ratio + width)
                x2_down, y2_down = parking_lane.get_point_at_distance_ratio_down(distance_to_second_point / parking_lane.get_distance_down())

                # crop the image

                rectangle = image.crop((x2_up, y2_up, x_down, y_down))

                # resize to the accepted input of the neural network NN_INPUT_SIZE
                resized_image = rectangle.resize(NN_INPUT_SIZE, PIL.Image.ANTIALIAS)

                # make prediction
                is_occupied = neural_network_predictor.predict(np.array(resized_image).reshape(1, 64, 64, 3))[0][0] == 1
                #if is_occupied:
                p = ParkingSpot()
                p.camera = parking_lane.camera
                p.bottom_left_x = x_down
                p.bottom_left_y = y_down
                p.upper_right_x = x2_up
                p.upper_right_y = y2_up
                p.latitude = 0
                p.longitude = 0
                p.save()
                p.is_occupied = is_occupied
                p.save()

                print("______", x2_up, y2_up, x_down, y_down)


        except Exception as e:
            print("--------------------- exception occured {} ---------------------".format(e))
            pass