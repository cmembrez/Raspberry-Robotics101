import argparse
import os
import sys
import time
import re
import torch
from torchvision import transforms
import torch.onnx
import utils
from transformer_net import TransformerNet
#from picamera import PiCamera
from time import sleep

def check_paths(args):
    try:
        if not os.path.exists(args.save_model_dir):
            os.makedirs(args.save_model_dir)
        if args.checkpoint_model_dir is not None and not (os.path.exists(args.checkpoint_model_dir)):
            os.makedirs(args.checkpoint_model_dir)
    except OSError as e:
        print(e)
        sys.exit(1)


def stylize(args):   
    
    if args.content_type=="pi":
        #camera.start_preview()
        #sleep(5)
        #camera.capture('/home/pi/Desktop/image.jpg')
        #camera.stop_preview()
        content_image = '/home/pi/Desktop/image.jpg'
    else :
        content_image = utils.load_image(args.content_image, scale=args.content_scale)
    
    tstart=time.time()
    
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0)

 
    with torch.no_grad():
        style_model = TransformerNet()
        state_dict = torch.load(args.model)
        # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
            
        output = style_model(content_image)
    utils.save_image(args.output_image, output[0])

    tstop=time.time()
    print("Inference time : "+str(1000*(tstop-tstart))+" ms")

def main():
    main_arg_parser = argparse.ArgumentParser(description="parser for fast-neural-style")
    subparsers = main_arg_parser.add_subparsers(title="subcommands", dest="subcommand")


    eval_arg_parser = subparsers.add_parser("eval", help="parser for evaluation/stylizing arguments")
    eval_arg_parser.add_argument("--content-image", type=str, required=True,
                                 help="path to content image you want to stylize")
    eval_arg_parser.add_argument("--content-scale", type=float, default=None,
                                 help="factor for scaling down the content image")
    eval_arg_parser.add_argument("--output-image", type=str, required=True,
                                 help="path for saving the output image")
    eval_arg_parser.add_argument("--model", type=str, required=True,
                                 help="saved model to be used for stylizing the image.")
    eval_arg_parser.add_argument("--content-type", type=str, required=True,
                                 help="Pi camera image : pi, Image file: f ")

    args = main_arg_parser.parse_args()

    if args.subcommand is None:
        print("ERROR: specify either train or eval")
        sys.exit(1)
    
    stylize(args)


if __name__ == "__main__":
    main()
