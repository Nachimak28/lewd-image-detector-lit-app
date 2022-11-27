import os
import base64
from lewd_image_detector_lit_api.components.lewd_image_detector_model import LewdImageDetector

### tests for the Image classifier class
def test_pred_function():
    image_model = LewdImageDetector()
    
    assets_for_test = ["../../assets/dog_image.jpeg", "../../assets/foot_image.jpeg"]

    # first asset should return False
    # encode image
    with open(assets_for_test[0], 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        assert image_model.predict(encoded_image_str=encoded_string) == False
    
    # second asset should return True
    with open(assets_for_test[1], 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        assert image_model.predict(encoded_image_str=encoded_string) == True