# Style Transfert Camera

Take a picture from the Raspberry Pi camera and apply style transfer.

![](images/style_transfert.png)

And create your own vision/style transfert box.

![](images/examples-box.png)

Raspberry Pi 3 and 4 could be used, but model with 1Gb memory will be limited in image input size. (limitation can be bypassed by augmenting the swap space, but this will masssively increase inference time) 

The code is initialy based on https://Github/Pytorch/examples/neural_style



### Required : Install Pytorch, Torchvision, and Opencv

Go to : https://github.com/nmilosev/pytorch-arm-builds   
Download the wheels for Pytorch and Torchvision (ARMv7 for Pi 3, Aarch64 for Pi 4).    
Install dependencies if needed.

`pip3 install <path of the wheels>`

### Run it! (Graphical User Interface) -- comming soon!

![](images/gui.png)

### Run it! (command line)

`python neural_style_inf.py eval --content-image </path/to/content/image> --model </path/to/saved/model> --output-image </path/to/output/image> --content-type f`


### Adding a new style

Use the code here :  Github/Pytorch/examples/neural_style

### Todo

* Make a lightweiht model
* Test NCS
* Capturing timelapse sequences

