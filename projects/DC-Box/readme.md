# DCbox (Detection-Classification) Box
![](DC-Box.jpg)
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

![](Hardware.png)

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

How the housing was build. including some pictures
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_01.jpg)
![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_02.jpg) ![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/projects/DC-Box/images/Housing_03.jpg)

### 2) Software Installation:
![](GUI_DCbox.jpg)

Installation of the software.


### 3) Training

jupyter notebook

Classification

https://drive.google.com/drive/folders/1wUgWwVYkGkXe6_noGpI24l3Pv4C3Z5RM

Segmentation

https://drive.google.com/file/d/1qJEYwBqI1eHG8b8IC-Y9w9ZqXDsIWalI

### 4) Result

How get Results. (Upload or Picamera)
