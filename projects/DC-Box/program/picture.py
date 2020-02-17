import cv2
import picamera
from picamera.array import PiRGBArray
import time

def preview_image(path):
    camera = picamera.PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.resolution = (1920, 1088)
    camera.capture(rawCapture, format="bgr")
    imagecv = rawCapture.array
    camera.close()
    imagecv = cv2.rotate(imagecv, cv2.ROTATE_180)
    imagecv = cv2.resize(imagecv, (0, 0), fx=0.3, fy=0.3)
    cv2.imwrite(path, imagecv)
    cv2.imshow('image', imagecv)

def sidex(path):
    camera = picamera.PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.resolution = (1920, 1088)
    camera.capture(rawCapture, format="bgr")
    imagecv = rawCapture.array
    imagecv = cv2.rotate(imagecv, cv2.ROTATE_180)
    # The image size is changed according to the model
    imagecv = cv2.resize(imagecv, (0, 0), fx=0.5, fy=0.5)
    camera.close()
    cv2.imwrite(path, imagecv)
    cv2.imshow('image', imagecv)
