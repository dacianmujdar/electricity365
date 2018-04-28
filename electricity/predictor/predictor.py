import numpy as np
from keras.models import model_from_json
from PIL import Image


class Predictor:

    def __init__(self):
        self._predictor = self._load_model()

    @staticmethod
    def _load_model():
        # load json and create model
        json_file = open('neural_network/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        predictor = model_from_json(loaded_model_json)
        # load weights into new model
        predictor.load_weights("neural_network/model.h5")

        return predictor

    def predict(self, image_path=None, np_array=None):
        if image_path:
            np_array = np.array(Image.open(image_path).resize((64, 64)))[:, :, :3].reshape(1, 64, 64,3)
        import pdb; pdb.set_trace()
        return self._predictor.predict(np_array)[0][0] == 1
