#import argparse
import os
import sys
import time
import re
import torch
from torchvision import transforms
import torch.onnx
import utilsIm
from transformer_net import TransformerNet
from time import sleep
import cv2


def load_img():   
    
    if combo1.value=="Picamera":
        from picamera import PiCamera
        camera=PiCamera()
        camera.resolution=(640,480)
        camera.start_preview()
        sleep(5)
        img_time=time.strftime("image-%Y%m%d-%H%M%S")
        img='/home/pi/Desktop/'+img_time+'.jpg'
        camera.capture(img)
        camera.stop_preview()
        content_image = utilsIm.load_image(img, scale=args.content_scale)
    elif combo1.value=="USB Camera":
        #from cv2 import VideoCapture
        cam=VideoCapture(0)
        s, img=cam.read()
        shot_time=time.strftime("image-%Y%m%d-%H%M%S")
        shot='/home/pi/Desktop/'+shot_time+'.jpg'      
        imwrite(shot,img)
#         content_image = utilsIm.load_image(shot, scale=args.content_scale)
    else :
        content_image = utilsIm.load_image(input_box2.value, scale=slider.value)
        #content_image = utilsIm.load_image("C:/Users/K/Pictures/uda/led.jpg", scale=slider.value)
        
    return content_image

def st_fns():    
    tstart=time.time()
    
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(load_img())
    content_image = content_image.unsqueeze(0)

 
    with torch.no_grad():
        style_model = TransformerNet()
        state_dict = torch.load("../saved_models/"+combo2.value+".pth")
        # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
            
        output = style_model(content_image)
    shot_time=time.strftime("-%Y%m%d-%H%M%S")
    utilsIm.save_image(input_box1.value+"/image_st_"+shot_time+".jpg", output[0])
    
    image_st = cv2.imread(input_box1.value+"/image_st_"+shot_time+".jpg")
    window_name = "image_st_"+shot_time+".jpg"
    cv2.imshow(window_name, image_st)
    
    tstop=time.time()
    print("Inference time : "+str(1000*(tstop-tstart))+" ms")

def run_stylize():    
    if checkbox1.value==True:
        
        import RPi.GPIO as GPIO
        
        def button_callback(channel):
            st_fns()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

        message=input("press enter to quit \n\n")
        
        GPIO.cleanup()
    
    elif checkbox2.value==True:
        import st_mrf
        
        tstart=time.time()
        
        st_mrf.mrf("nst_vgg19-symbol.xml",input_box2.value)
        
        tstop=time.time()
        print("Inference time : "+str(1000*(tstop-tstart))+" ms")
        
        image_mrf = cv2.imread("out_0.bmp")
        window_name = "out"
        cv2.imshow(window_name, image_mrf)
    
    else :
        st_fns()


from guizero import App, Box, TextBox, PushButton, Text, Picture, Combo, CheckBox, Slider
import tkinter
#import tkFileDialog
import os


def getdir():
    root = tkinter.Tk()
    root.withdraw() #use to hide tkinter window

    currdir = os.getcwd()
    tempdir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    input_box1.value=tempdir

def getfile():
    root = tkinter.Tk()
    root.withdraw() #use to hide tkinter window

    currdir = os.getcwd()
    tempdir = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a file')
    input_box2.value=tempdir

def input_choice(selected_value):
    if selected_value=="Picamera"or selected_value=="USB Camera":
        button2.disable()
        input_box2.disable()
    elif selected_value=="File":
        button2.enable()
        input_box2.enable()  

def show_img(selected_value):
        if selected_value=="Mosaic":
            picture.image="../images/output-images/amber-mosaic.jpg"
        elif selected_value=="Candy":
            picture.image="../images/output-images/amber-candy.jpg"
        elif selected_value=="Princess":
            picture.image="../images/output-images/amber-rain-princess.jpg"
        elif selected_value=="Udnie":
            picture.image="../images/output-images/amber-udnie.jpg"
        elif selected_value=="NCS 13":
            picture.image="../images/output-images/fastmrf13.jpg"

def nbox():
    if checkbox2.value==True:
        text.enabled=False
        slider.enabled=False
    else :
        text.enabled=True
        slider.enabled=True

    
app = App(title="Style Transfer Picamera", width=460, height=340)

dir_box = Box(app, width="fill", align="top")
button1 = PushButton(dir_box, command=getdir, text="Select Output Directory", width=18, align="left")
input_box1 = TextBox(dir_box, multiline=False, text="/home/pi/Documents", width="fill", height=2, align="left")

dir_box2 = Box(app, width="fill", align="top")
button2 = PushButton(dir_box2, command=getfile, text="Select Input File", width=18, align="left", enabled=False)
input_box2 = TextBox(dir_box2, multiline=False, text="/home/pi/Documents", width="fill", height=2, align="left", enabled=False)

buttons_box = Box(app, align="bottom")
button_style = PushButton(buttons_box, command=run_stylize, text="Take/Load Picture & Apply Style Transfer", width=30, align="right")
#button_phot = PushButton(buttons_box, command=getdir, text="Take Photo", width=18, align="right")

center_box = Box(app, align="left")
left_box = Box(center_box, align="left", layout="grid")

text3 = Text(left_box,size=10, text="Push Button : ", grid=[0,2])
checkbox1 = CheckBox(left_box, grid=[1,2])
text4 = Text(left_box,size=10, text="Neural Compute Stick : ", grid=[0,3])
checkbox2 = CheckBox(left_box, command=nbox, grid=[1,3])


text1 = Text(left_box,size=10, text="Device : ", grid=[0,0])
combo1 = Combo(left_box, options=["Picamera", "USB Camera", "File"], width=10, command=input_choice, grid=[1,0])
text2 = Text(left_box,size=10, text="Style : ", grid=[0,1])
combo2 = Combo(left_box,command=show_img, options=["Mosaic", "Candy", "Princess", "Udnie", "NCS 13"], width=10, grid=[1,1])

text = Text(left_box,size=10, text="Downscale : ", grid=[0,4])
slider = Slider(left_box, start=1, end=10, grid=[1,4])
#slider.bg='gray10'

picture_box = Box(center_box, align="right")
picture = Picture(picture_box, align="top", width=200, height=200, image="../images/output-images/amber-mosaic.jpg")
picture_box.bg="white"
picture.bg="white"

app.display()
