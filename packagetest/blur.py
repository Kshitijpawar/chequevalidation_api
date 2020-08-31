import cv2
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def blur_or_not(image, threshold= 100):
    #define threshold defaults to 100

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hy = cv2.Laplacian(image, cv2.CV_64F)
    fm = variance_of_laplacian(gray)
    text = "Not Blurry"

    if fm < threshold:
        text = "Blurry"
    return text, fm