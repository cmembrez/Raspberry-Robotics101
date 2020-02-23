#!/usr/bin/python3
# DCbox Version 1
# Datum: 08.02.2020

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from classifier import Classifier
from segmentation import Segmentation
import logging as log
import sys
from picture import sidex, preview_image, upload, canny, gray, background
import os
from datetime import datetime

class Gui:
    def __init__(self,classifier,SegmentationDetector,imagepath):
    #Tktiner
        root = tk.Tk()
        root.geometry('1200x1000+0+0')
        root.title("DC-Box")

        self.root = root
        self.classification_text=tk.StringVar(root)
        self.classification_text.set('\nClassification:\n\n')
        self.classifier = classifier

        self.segmentation_text=tk.StringVar(root)
        self.segmentation_text.set('\nSegmentation:\n\n')
        self.segmentationDetector = segmentationDetector
        
        self.detection_text=tk.StringVar(root)
        self.detection_text.set('\nDetection:\nBounding Box: xyz')
        
        #local variables for data exchange 
        self.current_image_path = imagepath        
#        self.folder_name
        
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
        project_input.current(0)
        project_input.grid(column=1, row=1, pady = 5)
        
        imagesize_text = tk.Label(section01, font=('arial', 12), text='Image Size:  ').grid(column=0, row=2, sticky="W")
        imagesize =["224x224"]
        imagesize_input=ttk.Combobox(section01,values=imagesize,width=40)
        imagesize_input.current(0)
        imagesize_input.grid(column=1, row=2, pady = 5)
        
        label_text = tk.Label(section01, font=('arial', 12), text='Label:  ').grid(column=0, row=3, sticky="W")
        label=["","Abies", "Acer", "Betula"]
        
        self.label_input=ttk.Combobox(section01,values=label,width=40)
        self.label_input.current(0)
        self.label_input.grid(column=1, row=3, pady = 5)    
    
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
        self.image_preview = ImageTk.PhotoImage(Image.open(self.current_image_path))
        self.image_panel01 = tk.Label(previewimageframe, image = self.image_preview)
        self.image_panel01.grid(column=0, row=2, sticky="W")
        
        image_livepreview_text = tk.Label(previewimageframe, font=('arial', 12), text='Live-Preview Image:  ').grid(column=1, row=1, sticky="W")
        self.image_livepreview = ImageTk.PhotoImage(Image.open(self.current_image_path))
        self.image_panel02 = tk.Label(previewimageframe, image = self.image_livepreview)
        self.image_panel02.grid(column=1, row=2, sticky="W")
        
        self.image_canny = ImageTk.PhotoImage(Image.fromarray(canny(self.current_image_path,"./canny.png")))
        self.image_panel03 = tk.Label(section04, image = self.image_canny)
        self.image_panel03.grid(column=0, row=1, sticky="W")
        
        self.image_gray = ImageTk.PhotoImage(Image.fromarray(gray(self.current_image_path,"./gray.png")))
        self.image_panel04 = tk.Label(section04, image = self.image_gray)
        self.image_panel04.grid(column=1, row=1, sticky="W")
        
        self.image_background = ImageTk.PhotoImage(Image.fromarray(background(self.current_image_path,"./backround.png")))
        self.image_panel05 = tk.Label(section04, image = self.image_background)
        self.image_panel05.grid(column=2, row=1, sticky="W")
        
    #Folder
        #folder_name = leafs_input.get()
        
    # Detection/Classification
        dc_text = tk.Label(dcframe, font=('arial', 14), text='Detection/Classification ').grid(column=0, row=0)
        bt_detection = tk.Button (dcframe, padx=16, bd=2, text="Detection",fg="green", command=self.detection).grid(row=1, column=0, pady = 5, sticky="EW")
        bt_classification = tk.Button (dcframe, padx=16, bd=2, text="Classification",fg="green", command=self.classification).grid(row=1, column=1, pady = 5)
        bt_segmentation = tk.Button (dcframe, padx=16, bd=2, text="Segmentation",fg="green", command=self.segmentation).grid(row=1, column=2, pady = 5)
    
        self.image_detection = ImageTk.PhotoImage(Image.open(self.current_image_path))
        self.image_panel06 = tk.Label(dcimageframe, image = self.image_detection)
        self.image_panel06.grid(column=0, row=2, sticky="W")
        detection_image_text = tk.Label(dcimageframe, font=('arial', 12), textvariable=self.detection_text).grid(column=0, row=3, sticky="EW")
    
        self.image_classification = ImageTk.PhotoImage(Image.open(self.current_image_path))
        self.image_panel07 = tk.Label(dcimageframe, image = self.image_classification)
        self.image_panel07.grid(column=1, row=2, sticky="W")
        classification_image_text = tk.Label(dcimageframe, font=('arial', 12), textvariable=self.classification_text).grid(column=1, row=3, sticky="EW")
    
        self.image_segmentation = ImageTk.PhotoImage(Image.open(self.current_image_path))
        self.image_panel08 = tk.Label(dcimageframe, image = self.image_segmentation)
        self.image_panel08 .grid(column=2, row=2, sticky="W")
        segmentation_image_text = tk.Label(dcimageframe, font=('arial', 12), textvariable=self.segmentation_text).grid(column=2, row=3, sticky="EW")
        
        self.root.mainloop()

# update the images after upload, preview, ..
# we need for each image to keep the image and the label in a local variable self.image_preview, self.image_panel01
    def update_images(self,image):
        self.image_preview = ImageTk.PhotoImage(Image.fromarray(image))
        self.image_panel01.configure(image=self.image_preview)
        
        self.image_livepreview = ImageTk.PhotoImage(Image.fromarray(image))
        self.image_panel02.configure(image=self.image_livepreview)
        
        self.image_canny = ImageTk.PhotoImage(Image.fromarray(canny(self.current_image_path,"./canny.png")))
        self.image_panel03.configure(image=self.image_canny)
        
        self.image_gray = ImageTk.PhotoImage(Image.fromarray(gray(self.current_image_path,"./gray.png")))
        self.image_panel04.configure(image=self.image_gray)

        self.image_bg = ImageTk.PhotoImage(Image.fromarray(background(self.current_image_path,"./background.png")))
        self.image_panel05.configure(image=self.image_bg)

        self.image_detection = ImageTk.PhotoImage(Image.fromarray(image))
        self.image_panel06.configure(image=self.image_detection)
        
        self.image_classification = ImageTk.PhotoImage(Image.fromarray(image))
        self.image_panel07.configure(image=self.image_classification)
        
        self.image_segmentation = ImageTk.PhotoImage(Image.fromarray(image))
        self.image_panel08.configure(image=self.image_segmentation)
        
        
    def preview(self):
#        global image_preview, image_preview01, image_preview02, image_preview03
        print('Save Preview Image')
        path = "./preview.png"
        
        cam_image = preview_image(path)
        self.current_image_path = path
        
        self.update_images(cam_image)
        
    def preview_live(self):
        print('Preview Image (Live Video) optional')
        
    def side1(self):
        print('Save Side 1 of image')  
        time = datetime.now().strftime(" %Y%m%d_%H.%M.%S.png")
        folder_name = self.label_input.get()
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
        folder_name = self.label_input.get()
        name = folder_name + "_side2"
        folder = "/home/pi/DC-Box/images" + "/" + folder_name +"/"
        try:
            os.makedirs(folder)
        except:
            pass
        path = folder + name + time
        sidex(path)
        
    def upload(self,event=None):
#        global image_preview, image_preview01, image_preview02, image_preview03
        print('Uploads image')
        filename = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
        self.current_image_path = filename
        upload_image = upload(filename, './upload.png')

        self.update_images(upload_image)
               
        
    def detection(self):
        print('Image detection (with Bounding Box)')
        self.detection_text.set('\nDetection\nBounding Box: {} {} {} {} \n\n'.format(0,0,0,0))
        
    def classification(self):
        print('Image classification')
        (prob,classlabel) = self.classifier.classify(self.current_image_path, 3, True)
        self.classification_text.set('\nClassification\n{:20}{:.7f}\n'.format(classlabel,prob))
        
    def segmentation(self):
        print('Image segmentation')
        (image_segmentation, classlabel) = self.segmentationDetector.segmentation(self.current_image_path)

        self.image_segmentation = ImageTk.PhotoImage(image_segmentation)
        
        self.image_panel08.configure(image=self.image_segmentation)
        self.segmentation_text.set('\nSegmentation:\n{:20}\n'.format(classlabel))
        

log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
#prepare classifier pathes @@@ todo create a main method and hand it over or extend the gui
#expects the model and a label file there:
clabelspath='./openvino/labels.txt'
cmodelpath= './openvino/model_leaf_01.xml'

slabelspath='./openvino/voc.names'
smodelpath= './openvino/model_leaf_segmentation_01.xml'
#needed on intel desktop
#device='CPU'
#cpu_extension='/opt/intel/openvino/inference_engine/samples/build/intel64/Release/lib/libcpu_extension.so'
#needed on raspberry + nsc2
device='MYRIAD'
cpu_extension=''
#init the classifier
imagepath= "./leaf_test.jpg"
classifier = Classifier( cmodelpath, device, cpu_extension,clabelspath)
segmentationDetector = Segmentation( smodelpath, device, cpu_extension,slabelspath)
gui = Gui(classifier,segmentationDetector,imagepath)

