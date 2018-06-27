import PIL
import numpy as np
from PIL import Image
import requests
from keras.models import model_from_json

from electricity.celery import app
from io import BytesIO

from electricity.parking.models import CameraInput

NN_INPUT_SIZE = (64, 64)

SNAPSHOT_LOCATION = 'snapshots/{}.png'


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


@app.task()
def refresh_frames(cycle):
    print("--------------------- Start refresh frame cycle {} ---------------------".format(cycle))
    neural_network_predictor = Predictor.load_model()
    print("--------------------- {} cameras detected ---------------------".format(CameraInput.objects.count()))
    for camera in CameraInput.objects.all():
        image = return_frame_from_url(camera.url)
        for camera_parking_spot in camera.parking_spots.all():
            try:
                # crop the image
                rect_img = image.crop((camera_parking_spot.upper_right_x, camera_parking_spot.upper_right_y,
                                       camera_parking_spot.bottom_left_x, camera_parking_spot.bottom_left_y))

                # resize to the accepted input of the neural network NN_INPUT_SIZE
                resized_image = rect_img.resize(NN_INPUT_SIZE, PIL.Image.ANTIALIAS)

                # make prediction
                camera_parking_spot.is_occupied = neural_network_predictor.predict(np.array(resized_image).reshape(1, 64, 64, 3))[0][0] == 1
                camera_parking_spot.save()

            except Exception as e:
                print("--------------------- exception occured {} ---------------------".format(e))
                pass
        image.save(SNAPSHOT_LOCATION.format(camera.id))

        # add this if we want to use AWS only
        # MediaStorage.upload_image(image_path)
    print("--------------------- Finish refresh frame cycle {} ---------------------".format(cycle))
    refresh_frames.apply_async((cycle + 1,), countdown=5)

