#!/usr/bin/env python
"""
 Copyright (C) 2018-2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import numpy as np
import logging as log
from time import time
from openvino.inference_engine import IENetwork, IECore



def mrf(model,img):
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    #args = build_argparser().parse_args()
    model_xml = model
    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    # Plugin initialization for specified device and load extensions library if specified
    log.info("Creating Inference Engine")
    ie = IECore()
    #if args.cpu_extension and 'CPU' in args.device:
        #ie.add_extension(args.cpu_extension, "CPU")
    # Read IR
    log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
    net = IENetwork(model=model_xml, weights=model_bin)

    #if "CPU" in args.device:
        #supported_layers = ie.query_network(net, "CPU")
        #not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        ##if len(not_supported_layers) != 0:
            #log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      #format(args.device, ', '.join(not_supported_layers)))
            #log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      #or --cpu_extension command line argument")
            #sys.exit(1)

    assert len(net.inputs.keys()) == 1, "Sample supports only single input topologies"
    assert len(net.outputs) == 1, "Sample supports only single output topologies"

    log.info("Preparing input blobs")
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    net.batch_size = 1

    # Read and pre-process input images
    n, c, h, w = net.inputs[input_blob].shape
    images = np.ndarray(shape=(n, c, h, w))
    for i in range(n):
        image = cv2.imread(img)
        if image.shape[:-1] != (h, w):
            log.warning("Image {} is resized from {} to {}".format(img[i], image.shape[:-1], (h, w)))
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image
    log.info("Batch size is {}".format(n))

    # Loading model to the plugin
    log.info("Loading model to the plugin")
    exec_net = ie.load_network(network=net, device_name="MYRIAD")

    # Start sync inference
    log.info("Starting inference")
    res = exec_net.infer(inputs={input_blob: images})

    # Processing output blob
    log.info("Processing output blob")
    res = res[out_blob]
    # Post process output
    for batch, data in enumerate(res):
        # Clip values to [0, 255] range
        data = np.swapaxes(data, 0, 2)
        data = np.swapaxes(data, 0, 1)
        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        data[data < 0] = 0
        data[data > 255] = 255
        data = data[::] - (0, 0, 0)
        out_img = os.path.join(os.path.dirname(__file__), "out_{}.bmp".format(batch))
        cv2.imwrite(out_img, data)
        log.info("Result image was saved to {}".format(out_img))
    log.info("This sample is an API example, for any performance measurements please use the dedicated benchmark_app tool\n")

#mrf("nst_vgg19-symbol.xml","OldMonkey.jpg")
