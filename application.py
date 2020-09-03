from flask import Flask, jsonify, abort, make_response, request, url_for
import cv2
import numpy as np
from PIL import Image
import tensorflow.keras

from packagetest.brightness import calc_brightness    
from packagetest.blur import blur_or_not
from packagetest.template import crop_image
from packagetest.analyzeocr import *
from packagetest.revisedbrightness import *
from packagetest.bankname import getBankName 

# auth = HTTPBasicAuth()
app = Flask(__name__)


@app.route('/imagehandling', methods= ['POST'])
def get_image():
    img = cv2.imdecode(np.frombuffer(request.files['hello'].read(), np.uint8), cv2.IMREAD_UNCHANGED)    
    
    forBankNameImage = Image.open(request.files['hello'])
    bankName = getBankName(model, forBankNameImage)
    # bankName = request.files['hello'].filename

    resolution = 'Valid' if img.shape[0] > 720 and img.shape[1] > 720 else 'Invalid'

    try:
        crop_img, stored_fn = crop_image(img, bankName)
    except:
        return json.dumps({'Obscured Check':'Invalid'})
    
    cv2.imwrite(stored_fn, img)
    
    blurry, blur_no = blur_or_not(crop_img)

    brightness = crop(Image.fromarray(crop_img), 200, 200)

    result = {
        # 'Stats' : 'Image received',
        'Blurry' : blurry,
        # 'Amount of Blur' : blur_no,
        'Brightness' : brightness,
        'Resolution' : resolution,
    }
    if 'Invalid' in result.values():
        debug = {
        # 'Stats' : 'Image received',
        'Blurry' : blurry,
        'Amount of Blur' : blur_no,
        'Brightness' : brightness,
        'Resolution' : resolution,
        }
        # print(debug)
        return json.dumps({'Image Quality Poor':'Invalid'})
    else:
        argumentsList = [stored_fn, '-t', 'image/jpeg', '-o', './packagetest/newresult.json']
        okthisisvaliddict = entrymain(argumentsList)
        result.update(okthisisvaliddict)
        print(result)
        return jsonify(result)

if __name__ == '__main__':
    model = tensorflow.keras.models.load_model('keras_model.h5')
    app.run(host= '0.0.0.0', port= 80,debug= True)
    # app.run()