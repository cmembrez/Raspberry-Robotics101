# GUI for DC-Box
The program is not yet finished. So if you want to make a contribution, we are more than happy.

## Preview
### def preview()
In this section you can preview the pictures from Picamera.
### def upload()
If you do not want to make your own pictures, then here you can upload a images from your PC.
### def preview_live()
Here there should be an live preview (video) of the object. This should help to set up the object.
## Labeling
### OpenCV
This section should come before saving the image. The images will be processed.
Resized, turned, color is changed if necessary (gray, BGR), ....
### def side1()
The preview image (side 1) is saved on the PI. e.g. birch_side1_0802201908
### def side2()
The preview image (side 2) is saved on the PI.
## Detection/Classification
### def detection()
The saved image is used for object detection. The model should detect an object and draw a bounding box.

### def classification()
The saved image will be classified using NUC2 and openvino.

### def segmentation()
The saved image will be segmented using NUC2 and openvino.

## GUI
### Tkinter
Layout for the program.
Very Basic. 
## If anyone could program a nicer GUI, don't hesitate. 
