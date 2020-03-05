# DCbox (Detection-Classification) Box
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/DC-Box.jpg)
## Story
AI on the edge is becoming increasingly important. A Raspberry PI in combination with an Intel NC2 stick is a real power horse, especially for real-time applications, slower Internet connections or security concerns.

The DCbox is an inexpensive and easy way to start deep learning. All you need is a Raspberry PI, an Intel NC2 stick, a Picamera, some acrylic and you can start your project. We provide a leaf classification template, but you are welcome to start whatever you want.
With the DCbox you can take good training photos. They are resized, processed and ready for training. The training part takes place in a Jupyter notebook. We also offer the trained leaf classification model, but as I said, train your own data and simply change the .XML and .bin files. After implementing the leaf model files, you can classify 185 tree species. So take a trip "into the woods" and get a tree expert.

### Things used in this project:

#### Hardware components:
- Raspberry PI 3 (PI 4 with 4GB is recommanded)
- PI Camera (optional)
- Intel Neural Compute Stick NCS 2
- Lasercutter (optional)
- LED (optional)

![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Hardware.png)

#### Software:
To run the project, you need to install the following software.

- Python 3
https://www.raspberrypi.org/documentation/linux/software/python.md
-	OpenCV
https://www.learnopencv.com/install-opencv-4-on-raspberry-pi/
-	Openvino
https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_raspbian.html
-	numpy
https://www.raspberrypi.org/forums/viewtopic.php?t=207058
- PIL
https://www.pkimber.net/howto/python/modules/pillow.html


### 1) Housing (Optional)

#### Things used for the housing:
- 4mm acrylic glass 600x400mm
- laser cutter
- screws and nuts for Raspberry PI
- hot glue gun

![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_01.jpg)
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_03.jpg) ![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_02.jpg)
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_04.jpg) ![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_05.jpg)
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_07.jpg)

##### Short description:

1) All parts are glued together
2) The nuts are fastened in the housing.
3) The Raspberry PI is screwed in.
4) The PIcamera is assembled.
5) LED (lights are recommended, but are not part of the showcase)
6) Done

### 2) Install pretrained models:

1) First, be sure you have installed all the recommende software.
2) Download: dcbox_v1.py, picture.py, segmentation.py, classifier.py
3) Create folder: openvino
4) Download in openvino: labels.txt, voc.names
5) Downnload the models and copy it into the openvino folder: .xml, .bin

[classification model](https://drive.google.com/drive/folders/1wUgWwVYkGkXe6_noGpI24l3Pv4C3Z5R)

[segmentation model](https://drive.google.com/open?id=1LeClOcnVulWA0Z8ngMvnPUC9dgUmTMc_)

6) You are ready to go!

### 3) Label new image
1) Start dcbox_v1.py in LXTerminal
2) Select Project: e.g.: leaf
3) Select image size (not implemented yet)
4) Press Preview or start Live-Preview
5) Select Label
6) Save image: Side 1 and Side 2
7) Images are saved in the project folder

### 4) Image Classification/Segmentation/Detection
1) Start dcbox_v1.py in LXTerminal
2) Select Project: leaf
3) Press Preview, start Live-Preview or upload image
4) Press Classification -> result will be displayed in the LXTerminal
5) Press Segmentation -> result will be displayed in the LXTerminal
6) Press Detection -> Not implemented yet!

![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/GUI_DCbox.jpg)

### 5) Training

#### Dataset
As a starting point, for our project, we used a dataset from Columbia University and the University of Maryland, containing 30866 images of 185 tree species form the Northeastern United States. For our training we preprocessed existing images:
- normalized
- centred
- resized 
- cropped

#### Classification Model
Our custom CNN model with several convolutional, pooling and fully-connected layers performed rather poorly, so the decision was to exercise the pre-trained VGG model. The VGG-19 model gave us 94% accuracy result on the test set and VGG=19_bn outperformed by 1.2%, producing a 95.2% accuracy level.

- projects/DC-Box/pytorch/pytorch2onnx.ipynb
- projects/DC-Box/pytorch/Leaf_dataset.ipynb

#### Segmentation Model
A tensorflow deeplab model was trained on the leaf dataset. It can be used to extract the relevant image parts for the classification to further improve the accuracy

- projects/tensorflow/deeplab/Leaf_TensorflowDeeplapSegmenation.ipynb
- projects/tensorflow/deeplab/deeplab_demo.ipynb
