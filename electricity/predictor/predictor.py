import numpy as np
import cv2
from keras.models import model_from_json
from PIL import Image


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
        if not Predictor._predictor:
            Predictor._predictor = Predictor._load_model()
        image = Image.open(image_path)

        np_array = np.array(image.resize((64, 64)))[:, :, :3].reshape(1, 64, 64, 3)
        return Predictor._predictor.predict(np_array)[0][0] == 1
