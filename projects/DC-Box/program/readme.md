# What you will find here:
## Files:
### GUI for the DCbox
- dcbox_v1.py
### Files for Detection, Classification, Segmentation
- detection.py
- classifier.py
- segmentation.py
- tinyyolov3.py
### .txt files for project and label (copy in openvino folder)
- project.txt
- label.txt
### Folder structure
#### DCbox
- dcbox_v1.py
- detection.py
- classifier.py
- segmentation.py
- tinyyolov3.py
#### Dcbox/openvino
- All models from Google Drive (bin and xml file)
- [classification model](https://drive.google.com/open?id=1wUgWwVYkGkXe6_noGpI24l3Pv4C3Z5RM)
- [segmentation model](https://drive.google.com/open?id=1LeClOcnVulWA0Z8ngMvnPUC9dgUmTMc_)
- [detection model](https://drive.google.com/open?id=17QcqasXilx4z5XL6ZFKiIvKECaXAls5b)
- project.txt
- label.txt

## GUI for DC-Box (dcbox_v1.py)
In the GUI you can preview images from the PI camera or upload them from your PC. The images are displayed with opencv and pre-processed (currently only for illustration). You can save your pictures in the project folder or start a new project.
The implemented "leaf" models recognize, classify and segment the input images. Note, however, that the accuracy of the model needs to be improved, but it's good enough to show the use case.
In future versions, you can also specify your settings in the Settings area or display your results on a second screen.
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/DCbox_gui_01_500.jpg)
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/DCbox_gui_02_500.jpg)
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/DCbox_gui_03_500.jpg)

## Detection 
A tiny yolov3 model was trained using the darknet tool on bounding boxes. The ground truth bounding boxes have been created based on the images themself. The accuracy of the model need to be improved, but it is good enough to show a different use case of Edge AI.
- projects/darknet/Leaf_DarknetTinyYolov3ObjectDetection.ipynb

## Classification 
Our custom CNN model with several convolutional, pooling and fully-connected layers performed rather poorly, so the decision was to exercise the pre-trained VGG model. The VGG-19 model gave us 94% accuracy result on the test set and VGG=19_bn outperformed by 1.2%, producing a 95.2% accuracy level.

- projects/DC-Box/pytorch/pytorch2onnx.ipynb
- projects/DC-Box/pytorch/Leaf_dataset.ipynb

## Segmentation 
A tensorflow deeplab model was trained on the leaf dataset. It can be used to extract the relevant image parts for the classification to further improve the accuracy.

- projects/tensorflow/deeplab/Leaf_TensorflowDeeplapSegmenation.ipynb
- projects/tensorflow/deeplab/deeplab_demo.ipynb

## .txt files
Are used to save the projects and their labels. However, it is possible to start a new project and save images there, but the label.txt has not yet been implemented properly (only works with the leaf project).

