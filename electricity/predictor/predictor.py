import numpy as np
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
    def predict(image_path=None, np_array=None):
        if not Predictor._predictor:
            Predictor._predictor = Predictor._load_model()
        image_path = "t.png"
        if image_path is not None:
            np_array = np.array(Image.open(image_path).resize((64, 64)))[:, :, :3].reshape(1, 64, 64,3)
        else:
            image = Image.fromarray(np_array)
            np_array = np.array(image.resize((64, 64)))[:, :, :3].reshape(1, 64, 64,3)
        return Predictor._predictor.predict(np_array)[0][0] == 1
