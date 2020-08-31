from PIL import Image
from collections import Counter
import numpy as np

def crop(pilimage, height, width):
    allbrightresults = []
    imgw, imgh = pilimage.size
    adjusth = (imgh // height) * height
    adjustw = (imgw // width) * width
    for i in range(0, adjusth, height):
        for j in range(0, adjustw, width):
            box = (j, i, j + width, i + height)
            a = pilimage.crop(box)
            single_brightness_val = calc_brightness(a)
            allbrightresults.append(single_brightness_val)
    
    theCounter = Counter(allbrightresults)
    if theCounter['Not Bright'] > 1:
        return 'Invalid'
    else:
        return 'Valid'



def calc_brightness(image):
    gray = image.convert('L')
    hist = gray.histogram()
    pixels = sum(hist)
    brightness = scale = len(hist)

    for i in range(0, scale):
        ratio = hist[i] / pixels
        brightness += ratio * (-scale + i)
    if brightness == 255:
        return "Bright"
    else:
        if brightness / scale > 0.5:
            return "Bright"
        return "Not Bright"


# if __name__ == "__main__":
#     filename = sys.argv[1]
#     image = Image.open(filename)
#     resultbright, resultblur = crop(image, 200, 200, 20)
#     counterbright = Counter(resultbright)
#     counterblur = Counter(resultblur)
#     print(counterbright)
#     print(counterblur)
