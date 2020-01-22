# Style Transfer Camera

Apply style transfer to picture taken from the Raspberry Pi camera.

![](utils/style_transfer.png)

And create your own style transfer camera/box.

![](utils/examples-box.png)

The Raspberry Pi 3 and 4 can be used, but models with 1 GB of memory will be limited in image input size. (the limitation can be overcome by increasing the swap space, but this will greatly increase the inference time)

The code is based on https://Github/Pytorch/examples/neural_style



### Required : Install Pytorch, Torchvision, and Opencv

Go to : https://github.com/nmilosev/pytorch-arm-builds   
Download the wheels for Pytorch and Torchvision (ARMv7 for Pi 3, Aarch64 for Pi 4).    
Install dependencies if needed.

`pip3 install <path of the wheels>`

### Run it! (Graphical User Interface) -- comming soon!

![](utils/GUI.png)

For more information on adding a push button (Box), go to the wiki page : 

### Run it! (command line)

`python neural_style_inf.py eval --content-image </path/to/content/image> --model </path/to/saved/model> --output-image </path/to/output/image> --content-type f`


### Adding a new style

Use the code here :  https://Github/Pytorch/examples/neural_style

### Todo

* Make a lightweiht model
* Test Intel Neural Compute Stick
* Capturing timelapse sequences

