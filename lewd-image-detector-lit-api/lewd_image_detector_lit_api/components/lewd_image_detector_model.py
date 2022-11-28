import os
import platform
import base64
import tempfile
import tensorflow as tf
from .utils import get_current_time, read_image


class LewdImageDetector:

    def __init__(self):
        """
        A simple class which is responsible for generating predictions for incoming images
        """
        saved_model_path = './private_detector/saved_model/'
        # for windows, download the model, unzip and place it at the directory level
        # /lewd-image-detector-lit-app/lewd-image-detector-lit-api 
        

        self.temp_dir = tempfile.mkdtemp()

        if os.path.exists(saved_model_path) == False:
            self.model_path = os.path.join(self.temp_dir, 'private_detector/saved_model/')
            if platform.system() != "Windows":
                print('downloading')
                # download the model 
                os.system(f'curl --output {self.temp_dir}/private_detector.zip https://storage.googleapis.com/private_detector/private_detector.zip')
                # unzip
                os.system(f"unzip -x {self.temp_dir}/private_detector.zip -d {self.temp_dir}")
            # for windows, please do this manually
        else:
            self.model_path = saved_model_path
        
        # load model
        self.model = tf.saved_model.load(self.model_path)


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