import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
from packagetest import banks

def getBankName(image):
    model = tensorflow.keras.models.load_model('keras_model.h5')

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # image = Image.open('test_photo.jpg')

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    results = dict(zip(banks, [prediction[0][0], prediction[0][1]]))
    bankName = max(results, key= results.get)
    print(bankName)
    return bankName
