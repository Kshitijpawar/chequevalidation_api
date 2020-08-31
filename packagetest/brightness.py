from PIL import Image

def calc_brightness(image):
    image = Image.fromarray(image)
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
    # return 1 if brightness == 255 else brightness / scale

# if __name__ == "__main__":
#     print(sys.argv)
#     for file in sys.argv[1:]:
#         image = Image.open(file)
#         print("{} {}".format(file, calc_brightness(image)))