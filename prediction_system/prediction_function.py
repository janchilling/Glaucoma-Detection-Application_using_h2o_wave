import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class Predictor:
    def __init__(self):
        self.model = load_model('prediction_system\prediction_model\convnetModel.h5')

    async def predict(self, file_path):
        img = image.load_img(file_path, target_size=(180, 180))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = self.model.predict(img_array)

        if prediction[0][0] >= 0.5:
            result = 'Positive'
        else:
            result = 'Negative'

        return f'The provided retinal image shows {result} Glaucoma'

predictor = Predictor()