#!/usr/bin/python3
# DCbox Version 1
# Datum: 08.02.2020

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from classifier import Classifier
import logging as log
import sys
from picture import sidex, preview_image, upload, canny, gray, background
import os
from datetime import datetime

class Gui:
    def __init__(self,classifier):
    #Tktiner
        global folder_name, label_input, previewimageframe, section04
        root = tk.Tk()
        root.geometry('1200x1000+0+0')
        root.title("DC-Box")

        self.root = root
        self.classification_text=tk.StringVar(root)
        self.classification_text.set('\nClassification:\n\n')
        self.classifier = classifier

        self.segmentation_text=tk.StringVar(root)
        self.segmentation_text.set('\nSegmentation:\n\n')
        
        self.detection_text=tk.StringVar(root)
        self.detection_text.set('\nDetection:\nBounding Box: xyz')
        
    #Frames für die GUI
        topframe = tk.Frame(root, width= 1600, height = 50, bg="blue")
        topframe.grid(row=0, column=0, padx=10, pady=2)
        
        section01 = tk.Frame(root)
        section01.grid (row=1, column=0, padx=10, pady=2, sticky="W")
    
        previewframe = tk.Frame(root)
        previewframe.grid(row=2, column=0, padx=10, pady=2, sticky="W")
        previewimageframe = tk.Frame(root)
        previewimageframe.grid(row=3, column=0, padx=10, pady=2, sticky="W")

        section04 = tk.Frame(root)
        section04.grid (row=4, column=0, padx=10, pady=2, sticky="W")
    
        dcframe = tk.Frame(root)
        dcframe.grid(row=6, column=0, padx=10, pady=2, sticky="W")
        dcimageframe = tk.Frame(root)
        dcimageframe.grid(row=7, column=0, padx=10, pady=2, sticky="W")
    #Head
        head_text = tk.Label(topframe, font=('arial', 28), text='DC-Box').grid(row=0, column=1,)
        
    # Section 1
        section01_heading = tk.Label(section01, font=('arial', 16), text='Settings').grid(column=0, row=0, sticky="W")
        project_text = tk.Label(section01, font=('arial', 12), text='Project:  ').grid(column=0, row=1, sticky="W")
        project =["Leafs"]
        project_input=ttk.Combobox(section01,values=project,width=40)
        project_input.grid(column=1, row=1, pady = 5)
        
        imagesize_text = tk.Label(section01, font=('arial', 12), text='Image Size:  ').grid(column=0, row=2, sticky="W")
        imagesize =["224x224"]
        imagesize_input=ttk.Combobox(section01,values=imagesize,width=40)
        imagesize_input.current(0)
        imagesize_input.grid(column=1, row=2, pady = 5)
        
        label_text = tk.Label(section01, font=('arial', 12), text='Label:  ').grid(column=0, row=2, sticky="W")
        label=["","Abies", "Acer", "Betula"]
        label_input=ttk.Combobox(section01,values=label,width=40)
        label_input.grid(column=1, row=2, pady = 5)    
    
    #Preview
        preview_text = tk.Label(previewframe, font=('arial', 16), text='Preview').grid(column=0, row=0, sticky="W")
        bt_preview = tk.Button (previewframe, padx=16, bd=2, text="Preview",fg="blue", command=self.preview).grid(row=1, column=0, pady = 5, sticky="W")
        bt_livepreview = tk.Button (previewframe, padx=16, bd=2, text="Live-Preview",fg="blue", command=self.preview_live).grid(row=1, column=2, pady = 5, sticky="W")
        bt_quit = tk.Button (previewframe, padx=16, bd=2, text="Upload",fg="blue", command=self.upload).grid(row=1, column=1, pady = 5, sticky="W")
        bt_upload = tk.Button (previewframe, padx=16, bd=2, text="Quit",fg="blue", command=self.root.quit).grid(row=1, column=3, pady = 5, sticky="W")
        saveimage_text = tk.Label(previewframe, font=('arial', 12), text='Save Image:  ').grid(column=0, row=2, sticky="W")
        bt_side1 = tk.Button (previewframe, padx=16, bd=2, text="Save: Side 1",fg="red", command=self.side1).grid(row=3, column=0, pady = 5, sticky="W")
        bt_side2 = tk.Button (previewframe, padx=16, bd=2, text="Save: Side 2",fg="red", command=self.side2).grid(row=3, column=1, pady = 5, sticky="W")
        
        image_preview_text = tk.Label(previewimageframe, font=('arial', 12), text='Preview Image:  ').grid(column=0, row=1, sticky="W")
        image_preview = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
        image_panel01 = tk.Label(previewimageframe, image = image_preview).grid(column=0, row=2, sticky="W")
        image_livepreview_text = tk.Label(previewimageframe, font=('arial', 12), text='Live-Preview Image:  ').grid(column=1, row=1, sticky="W")
        image_livepreview = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
        image_panel02 = tk.Label(previewimageframe, image = image_livepreview).grid(column=1, row=2, sticky="W")
        
        image_canny = ImageTk.PhotoImage(Image.open("leaf_canny.png"))
        image_panel01 = tk.Label(section04, image = image_canny)
        image_panel01.grid(column=0, row=1)
        
        image_gray = ImageTk.PhotoImage(Image.open("leaf_gray.png"))
        image_panel02 = tk.Label(section04, image = image_gray)
        image_panel02.grid(column=1, row=1, sticky="W")
        
        image_background = ImageTk.PhotoImage(Image.open("leaf_background.png"))
        image_panel03 = tk.Label(section04, image = image_background)
        image_panel03.grid(column=2, row=1, sticky="W")
        
    #Folder
        #folder_name = leafs_input.get()
        
    # Detection/Classification
        dc_text = tk.Label(dcframe, font=('arial', 14), text='Detection/Classification ').grid(column=0, row=0)
        bt_detection = tk.Button (dcframe, padx=16, bd=2, text="Detection",fg="green", command=self.detection).grid(row=1, column=0, pady = 5, sticky="EW")
        bt_classification = tk.Button (dcframe, padx=16, bd=2, text="Classification",fg="green", command=self.classification).grid(row=1, column=1, pady = 5)
        bt_segmentation = tk.Button (dcframe, padx=16, bd=2, text="Segmentation",fg="green", command=self.segmentation).grid(row=1, column=2, pady = 5)
    
        image_detection = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
        image_panel01 = tk.Label(dcimageframe, image = image_detection).grid(column=0, row=2, sticky="W")
        detection_image_text = tk.Label(dcimageframe, font=('arial', 12), textvariable=self.detection_text).grid(column=0, row=3, sticky="EW")
    
        image_classification = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
        image_panel02 = tk.Label(dcimageframe, image = image_classification).grid(column=1, row=2, sticky="W")
        classification_image_text = tk.Label(dcimageframe, font=('arial', 12), textvariable=self.classification_text).grid(column=1, row=3, sticky="EW")
    
        image_segmentation = ImageTk.PhotoImage(Image.open("leaf_test.jpg"))
        image_panel03 = tk.Label(dcimageframe, image = image_segmentation).grid(column=2, row=2, sticky="W")
        segmentation_image_text = tk.Label(dcimageframe, font=('arial', 12), textvariable=self.segmentation_text).grid(column=2, row=3, sticky="EW")
        
        self.root.mainloop()


    def preview(self):
        global image_preview, image_preview01, image_preview02, image_preview03
        print('Save Preview Image')
        path = "/home/pi/DC-Box/leaf_preview.png"
        path_canny = "/home/pi/DC-Box/leaf_canny.png"
        path_gray = "/home/pi/DC-Box/leaf_gray.png"
        path_background = "/home/pi/DC-Box/leaf_background.png"
        
        preview_image(path)
        
        image_preview = ImageTk.PhotoImage(Image.open("leaf_preview.png"))
        image_panel01 = tk.Label(previewimageframe, image = image_preview)
        image_panel01.grid(column=0, row=2, sticky="W")
        
        canny(path, path_canny)
        gray(path, path_gray)
        background(path, path_background)
        
        image_preview01 = ImageTk.PhotoImage(Image.open("/home/pi/DC-Box/leaf_canny.png"))
        image_panel01 = tk.Label(section04, image = image_preview01)
        image_panel01.grid(column=0, row=1, sticky="W")
        
        image_preview02 = ImageTk.PhotoImage(Image.open("/home/pi/DC-Box/leaf_gray.png"))
        image_panel02 = tk.Label(section04, image = image_preview02)
        image_panel02.grid(column=1, row=1, sticky="W")
        
        image_preview03 = ImageTk.PhotoImage(Image.open("/home/pi/DC-Box/leaf_background.png"))
        image_panel03 = tk.Label(section04, image = image_preview03)
        image_panel03.grid(column=2, row=1, sticky="W")
        
    def preview_live(self):
        print('Preview Image (Live Video) optional')
        
    def side1(self):
        print('Save Side 1 of image')  
        time = datetime.now().strftime(" %Y%m%d_%H.%M.%S.png")
        folder_name = label_input.get()
        name = folder_name + "_side1"
        folder = "/home/pi/DC-Box/images" + "/" + folder_name +"/"
        try:
            os.makedirs(folder)
        except:
            pass
        path = folder + name + time
        sidex(path)
        
    def side2(self):
        print('Save Side 2 of image')
        time = datetime.now().strftime(" %Y%m%d_%H.%M.%S.png")
        folder_name = label_input.get()
        name = folder_name + "_side2"
        folder = "/home/pi/DC-Box/images" + "/" + folder_name +"/"
        try:
            os.makedirs(folder)
        except:
            pass
        path = folder + name + time
        sidex(path)
        
    def upload(event=None):
        global image_preview, image_preview01, image_preview02, image_preview03
        print('Uploads image')
        path = "/home/pi/DC-Box/leaf_upload.png"
        path_canny = "/home/pi/DC-Box/leaf_canny.png"
        path_gray = "/home/pi/DC-Box/leaf_gray.png"
        path_background = "/home/pi/DC-Box/leaf_background.png"
        
        filename = filedialog.askopenfilename(initialdir = "/home/pi/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        image_upload = filename
        upload(image_upload, path)
        canny(image_upload, path_canny)
        gray(image_upload, path_gray)
        background(image_upload, path_background)
        
        image_preview = ImageTk.PhotoImage(Image.open("leaf_upload.png"))
        image_panel01 = tk.Label(previewimageframe, image = image_preview)
        image_panel01.grid(column=0, row=2, sticky="W")
        
        image_preview01 = ImageTk.PhotoImage(Image.open("/home/pi/DC-Box/leaf_canny.png"))
        image_panel01 = tk.Label(section04, image = image_preview01)
        image_panel01.grid(column=0, row=1, sticky="W")
        
        image_preview02 = ImageTk.PhotoImage(Image.open("/home/pi/DC-Box/leaf_gray.png"))
        image_panel02 = tk.Label(section04, image = image_preview02)
        image_panel02.grid(column=1, row=1, sticky="W")
        
        image_preview03 = ImageTk.PhotoImage(Image.open("/home/pi/DC-Box/leaf_background.png"))
        image_panel03 = tk.Label(section04, image = image_preview03)
        image_panel03.grid(column=2, row=1, sticky="W")   
        
    def detection(self):
        print('Image detection (with Bounding Box)')
        self.detection_text.set('\nDetection\nBounding Box: {} {} {} {} \n\n'.format(0,0,0,0))
        
    def classification(self):
        print('Image classification')
        (prob,classlabel) = self.classifier.classify(imagepath, 3, True)
        self.classification_text.set('\nClassification\n{:20}{:.7f}\n'.format(classlabel,prob))
        
    def segmentation(self):
        print('Image classification')
        self.segmentation_text.set('\nSegmentation:\n\n'.format())
        

log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
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
imagepath= "leaf_test.jpg"
classifier = Classifier( modelpath, device, cpu_extension,labelspath)
gui = Gui(classifier)

