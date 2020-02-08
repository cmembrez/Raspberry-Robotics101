import argparse
import os
import sys
import time
import re

import numpy as np
import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms
import torch.onnx

import utils
from transformer_net import TransformerNet




style_model = TransformerNet()

state_dict = torch.load("D:/__AI_Courses_certif/__Udacity/__Projects/fast_neural_style/saved_models/candy.pth")
# remove saved deprecated running_* keys in InstanceNorm from the checkpoint
for k in list(state_dict.keys()):
    if re.search(r'in\d+\.running_(mean|var)$', k):
        del state_dict[k]           
style_model.load_state_dict(state_dict)
     
rand_input=torch.randn(1,3,224,224)
torch.onnx.export(style_model,rand_input,"candy.onnx") 