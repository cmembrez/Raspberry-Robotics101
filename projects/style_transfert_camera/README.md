# Project Style Transfert Camera


### Install Pytorch and Torchvision

Go to : https://github.com/nmilosev/pytorch-arm-builds   
Download the wheels for Pytorch and Torchvision (ARMv7 for Pi 3, Aarch64 for Pi 4).    
Install dependencies if needed.

`pip3 install <path of the wheels>`

### Run it!

`python neural_style.py eval --content-image </path/to/content/image> --model </path/to/saved/model> --output-image </path/to/output/image> --content-type f`

That's all, folks! Enjoy!

### Todo

* Test : Get image from Pi camera
* Test NCS
* Capturing timelapse sequences
