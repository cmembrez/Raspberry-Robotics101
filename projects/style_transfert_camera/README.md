# Picamera Style Transfer

**Apply style transfer to picture taken from the Raspberry Pi camera (or usb camera, files).**

![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/images/utils/style_transfer.jpg)

**And create your own style transfer camera/box.**

![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/images/utils/examples-box.png)

Usable Raspberry Pi model : Pi 3/4. (Models with 1 GB memory will be limited in image input size. The limitation can be overcome by increasing the swap space, but this will greatly increase the inference time)

Image size limitation :
* Pi 3/ Pi 4, 1GB : ~200x200px
* Pi 4, 4GB : ~640 × 480px

The code is based on https://github.com/pytorch/examples/tree/master/fast_neural_style


### Required : Pytorch, Torchvision, and Opencv

Go to : https://github.com/nmilosev/pytorch-arm-builds   
Download the wheels for Pytorch and Torchvision (ARMv7 for Pi 3, Aarch64 for Pi 4).    
Install dependencies if needed.

`pip3 install <path of the wheels>`

### Run it! (Graphical User Interface) -- comming soon!

![](https://github.com/cmembrez/Raspberry-Robotics101/blob/master/images/utils/GUI.png)

* adding a push button (Box) : 

Check the box to add a push button. Use pin 3.3v and n10. See image bellow :

<img src="https://raspberrypihq.com/wp-content/uploads/2018/02/02_Push-button_bb-min.jpg" alt="button" width="300"/>

### Run it! (command line)

`python neural_style_inf.py eval --content-image </path/to/content/image> --model </path/to/saved/model> --output-image </path/to/output/image> --content-type f --content-scale 2` 


### Adding a new style

Use the code here :  https://github.com/pytorch/examples/tree/master/fast_neural_style

### Todo

* Make a lightweiht model
* Test Intel Neural Compute Stick
* Capturing timelapse sequences
