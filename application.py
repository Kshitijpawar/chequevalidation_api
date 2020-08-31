from flask import Flask, jsonify, abort, make_response, request, url_for
import cv2
import numpy as np
from PIL import Image

from packagetest.brightness import calc_brightness    
from packagetest.blur import blur_or_not
from packagetest.template import crop_image
from packagetest.analyzeocr import *
from packagetest.revisedbrightness import *


# auth = HTTPBasicAuth()
app = Flask(__name__)


@app.route('/imagehandling', methods= ['POST'])
def get_image():
    print("inside")
    img = cv2.imdecode(np.frombuffer(request.files['hello'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    bankName = request.files['hello'].filename

    resolution = [img.shape[0], img.shape[1]]


    crop_img, stored_fn = crop_image(img, )
    
    print(resolution)
    print(crop_img.shape)
    cv2.imwrite(stored_fn, img)

    blurry, blur_no = blur_or_not(crop_img)

    # brightness = calc_brightness(crop_img)
    brightness = crop(Image.fromarray(crop_img), 200, 200)


    # argumentsList = [stored_fn, '-t', 'image/jpeg', '-o', './packagetest/newresult.json']
    # okthisisvaliddict = entrymain(argumentsList)
    # print(okthisisvaliddict)
    # runAnalysis(argumentsList)


    result = {
        # 'Stats' : 'Image received',
        'Blurry' : blurry,
        # 'Amount of Blur' : blur_no,
        'Brightness' : brightness,
        'Resolution' : "{} X {}".format(resolution[0], resolution[1]),
    }
    # result.update(okthisisvaliddict)

    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
