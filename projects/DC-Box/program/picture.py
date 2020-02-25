import cv2
import picamera
from picamera.array import PiRGBArray
import time
import numpy as np
from PIL import ImageTk, Image

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
    cv2.imwrite(path, imagecv)
    imagecv = cv2.resize(imagecv, (300, 200))
    imagepath = path
    print(imagepath)
    return imagecv

def live_preview(path,gui):
    camera = picamera.PiCamera()
    camera.resolution = (640,480)
    camera.framerate= 5
    # capture frames from the camera
    rawCapture = PiRGBArray(camera,size=(640,480))
    time.sleep(0.1)
    print("start frame capture")
    stop = False
    imagecv = None
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
        image = frame.array
    # show the frame
        imagecv = cv2.rotate(image, cv2.ROTATE_180)
        image_resize = cv2.resize(imagecv, (300, 200))
        stop = gui.update_live_preview(image_resize)

#        key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        if stop:
            break
    print("exit live_preview")
    imagecv = cv2.cvtColor(imagecv, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path, imagecv)
    camera.close()
    
def upload(path):
    image_resize= cv2.imread (path)
    cv2.imwrite(path, image_resize)
    image_resize = cv2.resize(image_resize, (300, 200))
    return image_resize

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
    return imagecv
    
def canny(image_upload, path_canny):
    print("image_upload",image_upload)
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))  
    image_resize = cv2.Canny(image_resize, 50, 150)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "Canny", (10, 90), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(path_canny,image_resize)
    return image_resize
    
def gray(image_upload, path_gray):
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))
    image_resize = cv2.cvtColor(image_resize, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "Gray", (10, 90), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imwrite(path_gray,image_resize)
    return image_resize
    
def background(image_upload, path_background):
    image_resize= cv2.imread (image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))
    image_resize = cv2.GaussianBlur(image_resize, (5,5),0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "GaussianBlur", (10, 90), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imwrite(path_background,image_resize)
    return image_resize

def boundingbox(image_upload, path_boundingbox):
    img = cv2.imread('canny.png')
    image_resize = cv2.imread(image_upload)
    image_resize = cv2.resize(image_resize, (150, 100))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((3,3), dtype=np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 1)
    cv2.imwrite(path_boundingbox,img)
    cv2.rectangle(image_resize, (x,y), (x+w, y+h), (255,255,0), 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image_resize, "Bounding Box", (10, 90), font, 0.5, (255, 0, 255), 1, cv2.LINE_AA)
    cv2.imwrite("image_edges_boundingbox.png", img)
    cv2.imwrite(path_boundingbox, image_resize)
    return image_resize
