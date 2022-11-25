import os
import base64
import tempfile
import tensorflow as tf
from .utils import get_current_time, read_image


class LewdImageDetector:
    def _setup(self):
        """
        Pre-setup model load
        """
        # saved_model_path = './saved_model/'
        saved_model_path = './private_detector/saved_model/'
        
        
        self.model = tf.saved_model.load(saved_model_path)

    def __init__(self):
        """
        A simple class which is responsible for generating predictions for incoming images
        """
        self.model = None

        self._setup()

        self.temp_dir = tempfile.mkdtemp()

    def predict(self, encoded_image_str: str):
        """
        Prediction function implementation
        
        Parameters
        ----------
        encoded_image_str : str
            Base64 string representation of an image

        Returns
        -------
        decision_flag : bool
            A flag with value True/False indicating whether input image is a lewd image or no
        """

        if encoded_image_str.startswith("data:image"):
            encoded_image_str = encoded_image_str.split("base64,")[-1]
        # write image to local dir
        filepath = os.path.join(self.temp_dir, f'{get_current_time()}.png')
        with open(filepath, "wb") as fh:
            fh.write(base64.b64decode(encoded_image_str))
        
        # run the prediction
        image = read_image(filepath)

        preds = self.model([image])

        # cleanup
        try:
            os.remove(filepath)
        except Exception as e:
            print(e)
        
        lewd_image_probability = tf.get_static_value(preds[0])[0]
        # set threshold for the probability and send true/false flag
        decision_flag = float(lewd_image_probability) > 0.5
        return decision_flag