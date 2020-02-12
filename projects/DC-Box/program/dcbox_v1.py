#!/usr/bin/python3
# DCbox Version 1
# Datum: 08.02.2020

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from classifier import Classifier
import logging as log
import sys

def preview():
    camera = picamera.PiCamera()
    rawCapture = PiRGBArray(camera)
    camera.resolution = (1920, 1088)
    camera.capture(rawCapture, format="bgr")
    imagecv = rawCapture.array
    camera.close()
    path = "/home/pi/Desktop/preview.png"
    cv2.imwrite(path, imagecv)
    print('Save Preview Image on Desktop')
    
def preview_live():
    print('Preview Image (Live Video) optional')
    
def side1():
    print('Save Side 1 of image')
    
def side2():
    print('Save Side 2 of image')
    
def detection():
    print('Image detection (with Bounding Box)')
    
def classification():
    print('Image classification')
    classifier.classify(imagepath, 3, True)
    
def segmentation():
    print('Image segmentation')
    
log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
#Tktiner
root = tk.Tk()
root.geometry('1200x1000+0+0')
root.title("DC-Box")

#Frames für die GUI
topframe = tk.Frame(root, width= 1600, height = 50, bg="blue")
topframe.grid(row=0, column=0, padx=10, pady=2)

previewframe = tk.Frame(root)
previewframe.grid(row=1, column=0, padx=10, pady=2, sticky="W")
previewimageframe = tk.Frame(root)
previewimageframe.grid(row=2, column=0, padx=10, pady=2, sticky="W")

labelframe = tk.Frame(root)
labelframe.grid(row=3, column=0, padx=10, pady=2, sticky="W")
labelpanelframe = tk.Frame(root)
labelpanelframe.grid(row=4, column=0, padx=10, pady=2, sticky="W")

dcframe = tk.Frame(root)
dcframe.grid(row=5, column=0, padx=10, pady=2, sticky="W")
dcimageframe = tk.Frame(root)
dcimageframe.grid(row=6, column=0, padx=10, pady=2, sticky="W")
#Head
head_text = tk.Label(topframe, font=('arial', 28), text='DC-Box').grid(row=0, column=1,)

#Preview
preview_text = tk.Label(previewframe, font=('arial', 14), text='Preview ').grid(column=0, row=0, sticky="W")
bt_preview = tk.Button (previewframe, padx=16, bd=2, text="Preview",fg="blue", command=preview).grid(row=1, column=0, pady = 5, sticky="W")
bt_livepreview = tk.Button (previewframe, padx=16, bd=2, text="Live-Preview",fg="blue", command=preview_live).grid(row=1, column=1, pady = 5, sticky="W")

image_preview = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
image_panel01 = tk.Label(previewimageframe, image = image_preview).grid(column=0, row=2, sticky="W")
image_livepreview = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
image_panel02 = tk.Label(previewimageframe, image = image_livepreview).grid(column=1, row=2, sticky="W")

#Labeling
labeling_text = tk.Label(labelframe, font=('arial', 14), text='Labeling').grid(column=0, row=0, sticky="W")
leafs=["","birch"]
leafs_input=ttk.Combobox(labelpanelframe,values=leafs,width=40).grid(column=0, row=1, pady = 5)
bt_side1 = tk.Button (labelframe, padx=16, bd=2, text="Side 1",fg="red", command=side1).grid(row=2, column=0, pady = 5, sticky="W")
bt_side2 = tk.Button (labelframe, padx=16, bd=2, text="Side 2",fg="red", command=side2).grid(row=2, column=1, pady = 5, sticky="W")

# Detection/Classification
dc_text = tk.Label(dcframe, font=('arial', 14), text='Detection/Classification ').grid(column=0, row=0)
bt_detection = tk.Button (dcframe, padx=16, bd=2, text="Detection",fg="green", command=detection).grid(row=1, column=0, pady = 5, sticky="EW")
bt_classification = tk.Button (dcframe, padx=16, bd=2, text="Classification",fg="green", command=classification).grid(row=1, column=1, pady = 5)
bt_segmentation = tk.Button (dcframe, padx=16, bd=2, text="Segmentation",fg="green", command=segmentation).grid(row=1, column=2, pady = 5)

image_detection = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
image_panel01 = tk.Label(dcimageframe, image = image_detection).grid(column=0, row=2, sticky="W")
detection_image_text = tk.Label(dcimageframe, font=('arial', 12), text='\nResults: Detection e.g. \n\n Bounding Box: xyz').grid(column=0, row=3, sticky="EW")

image_classification = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
image_panel02 = tk.Label(dcimageframe, image = image_classification).grid(column=1, row=2, sticky="W")
classification_image_text = tk.Label(dcimageframe, font=('arial', 12), text='\nResults: Classification e.g.\n\n acer_negundo 0.9999982\nptelea_trifoliata0.0000018 ').grid(column=1, row=3, sticky="EW")

image_segmentation = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
image_panel03 = tk.Label(dcimageframe, image = image_segmentation).grid(column=2, row=2, sticky="W")
segmentation_image_text = tk.Label(dcimageframe, font=('arial', 12), text='\nResults: Segmentation e.g.\n\n ??? ').grid(column=2, row=3, sticky="EW")

#prepare classifier pathes @@@ todo create a main method and hand it over or extend the gui
#expects the model and a label file there:
labelspath='./openvino/labels.txt'
modelpath= './openvino/model_leaf_01.xml'
#needed on intel desktop
#device='CPU'
#cpu_extension='/opt/intel/openvino/inference_engine/samples/build/intel64/Release/lib/libcpu_extension.so'
#needed on raspberry + nsc2
device='MYRIAD'
cpu_extension=''
#init the classifier
classifier = Classifier( modelpath, device, cpu_extension,labelspath)


root.mainloop()

