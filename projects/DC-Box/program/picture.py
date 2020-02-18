import cv2
import picamera
from picamera.array import PiRGBArray
import time

def settings():
    global font
    font = cv2.FONT_HERSHEY_SIMPLEX

def preview_image(path):
    camera = picamera.PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.resolution = (1920, 1088)
    camera.capture(rawCapture, format="bgr")
    imagecv = rawCapture.array
    camera.close()
    imagecv = cv2.rotate(imagecv, cv2.ROTATE_180)
    imagecv = cv2.resize(imagecv, (250, 160))
    cv2.imwrite(path, imagecv)
    imagepath = path
    print(imagepath)
    
def upload(image_upload, path):
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (250, 160))
    cv2.imwrite(path, image_resize)
    imagepath = path
    print(imagepath)

def sidex(path):
    camera = picamera.PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.resolution = (1920, 1088)
    camera.capture(rawCapture, format="bgr")
    imagecv = rawCapture.array
    imagecv = cv2.rotate(imagecv, cv2.ROTATE_180)
    # The image size is changed according to the model in our case (224x224)
    imagecv = cv2.resize(imagecv, (224, 224))
    camera.close()
    cv2.imwrite(path, imagecv)
    
def canny(image_upload, path_canny):
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))  
    image_resize = cv2.Canny(image_resize, 50, 150)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "Canny", (10, 90), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(path_canny,image_resize)
    
def gray(image_upload, path_gray):
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))
    image_resize = cv2.cvtColor(image_resize, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "Gray", (10, 90), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imwrite(path_gray,image_resize)
    
def background(image_upload, path_background):
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))
    image_resize = cv2.GaussianBlur(image_resize, (5,5),0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "GaussianBlur", (10, 90), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imwrite(path_background,image_resize)
