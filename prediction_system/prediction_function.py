import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class Predictor:
    def __init__(self):
        """
        Initializes the Predictor class by loading the pre-trained deep learning model.
        """

        self.model = load_model('prediction_system/prediction_model/convnetModel.h5')

    async def predict(self, file_path):
        """
        Gets the image from the file path and runs through
        the deep learning model to identify if there is Glaucoma.

        Args :
            file_path (str): The file path of the retinal image to be predicted.

        Returns : 
            String containing the result 
        """

        # Getting the image
        img = image.load_img(file_path, target_size=(180, 180))

        # Preprocessing the image
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        #Fitting the image array to the model
        prediction = self.model.predict(img_array)

        if prediction[0][0] >= 0.5:
            result = 'Positive'
        else:
            result = 'Negative'

        return f'The provided retinal image is Glaucoma {result}'

predictor = Predictor()