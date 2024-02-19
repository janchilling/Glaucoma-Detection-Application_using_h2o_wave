import numpy as np
import cv2
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

        return f'The above retinal image shows {result} Glaucoma'

#     async def predict_stream(self, stream_name, q):
#         async for data in q.site.stream(stream_name):
#             nparr = np.frombuffer(data, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#             img = cv2.resize(img, (180, 180))  # Resize the image if necessary
#             img_array = np.expand_dims(img, axis=0)
#             img_array = img_array / 255.0

#             prediction = self.model.predict(img_array)

#             if prediction[0][0] >= 0.5:
#                 result = 'Positive'
#             else:
#                 result = 'Negative'

#             return f'The above retinal image shows {result} Glaucoma'


predictor = Predictor()