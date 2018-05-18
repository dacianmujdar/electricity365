import PIL
import numpy as np
import cv2
from keras.models import model_from_json
from PIL import Image

NN_INPUT_SIZE = (64, 64)


class Predictor:

    _predictor = None

    @staticmethod
    def _load_model():
        # load json and create model
        json_file = open('electricity/predictor/neural_network/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        predictor = model_from_json(loaded_model_json)
        # load weights into new model
        predictor.load_weights("electricity/predictor/neural_network/model.h5")
        return predictor

    @staticmethod
    def predict(image_path):
        """
        Assumes the image found at image_path has exact size NN_INPUT_SIZE
        :param image_path:
        :return:
        """
        if not Predictor._predictor:
            Predictor._predictor = Predictor._load_model()
        image = Image.open(image_path)
        image_resized = image.resize(NN_INPUT_SIZE, PIL.Image.ANTIALIAS)
        np_array = np.array(image_resized)[:, :, :3]
        image_resized.save('partial_resized.png')
        return Predictor._predictor.predict(np_array.reshape(1, 64, 64, 3))[0][0] == 1
