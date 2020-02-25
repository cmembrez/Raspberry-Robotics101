#!/usr/bin/env python
import sys
import os
import cv2
import numpy as np
import logging as log
from openvino.inference_engine import IENetwork, IECore
from PIL import ImageTk, Image
import threading

class InferReqWrap:
    def __init__(self, request, id):
        self.id = id
        self.request = request
        self.cur_iter = 0
        self.cv = threading.Condition()
        self.request.set_completion_callback(self.callback, self.id)

    def callback(self, statusCode, userdata):
        if (userdata != self.id):
            log.error("Request ID {} does not correspond to user data {}".format(self.id, userdata))
        elif statusCode != 0:
            log.error("Request {} failed with status code {}".format(self.id, statusCode))
        self.cur_iter += 1
        log.info("Completed {} Async request execution".format(self.cur_iter))
        if self.cur_iter < self.num_iter:
            # here a user can read output containing inference results and put new input
            # to repeat async request again
            self.request.async_infer(self.input)
        else:
            # continue sample execution after last Asynchronous inference request execution
            self.cv.acquire()
            self.cv.notify()
            self.cv.release()

    def execute(self, mode, input_data):
        if (mode == "async"):
            log.info("Start inference (Asynchronous executions)")
            self.input = input_data
            # Start async request for the first time. Wait all repetitions of the async request
            self.request.async_infer(input_data)
            self.cv.acquire()
            self.cv.wait()
            self.cv.release()
        elif (mode == "sync"):
            log.info("Start inference (Synchronous executions)")
            # here we start inference synchronously and wait for
            # last inference request execution
            self.request.infer(input_data)
            log.info("Completed Sync request execution")
        else:
            log.error("wrong inference mode is chosen. Please use \"sync\" or \"async\" mode")


class Segmentation:
    def __init__(self, modelpath, device, cpu_extension,labelspath):
        
        self.model_xml = modelpath
        self.model_bin = os.path.splitext(modelpath)[0] + ".bin"
        self.device = device
        self.cpu_extension = cpu_extension
        
        self.mean = np.array([0.485, 0.456, 0.406])        
        self.std = np.array([0.229, 0.224, 0.225])
        
        
        palette = [2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1]
        self.colors = np.array([i for i in range(21)])[:, None] * palette
        self.colors = (self.colors % 255).astype("uint8")
        
        
        #read labels map fromn file
        self.labels_map = None
        if not labelspath is None: 
            log.info("Read Labels File")
            with open(labelspath, 'r') as f:
                self.labels_map = [x.split(sep=' ', maxsplit=1)[-1].strip() for x in f]
        else:
            log.info("No Labels are defined")
            
    def init_device(self):        
        log.info("Creating Inference Engine")
        self.ie = IECore()
        if self.cpu_extension and 'CPU' in self.device:
            self.ie.add_extension(self.cpu_extension, "CPU")
            log.info("Added CPU extension")
        
        log.info("Loading network files:\n\t{}\n\t{}".format(self.model_xml, self.model_bin))
        self.net = IENetwork(model=self.model_xml, weights=self.model_bin)

        if "CPU" in self.device:
            supported_layers = self.ie.query_network(self.net, "CPU")
            not_supported_layers = [l for l in self.net.layers.keys() if l not in supported_layers]
            if len(not_supported_layers) != 0:
                log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(self.device, ', '.join(not_supported_layers)))
                log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
                
                self.ie = None
                self.net = None
                
    def segmentation(self,imagepath):
        self.init_device()
        image = cv2.imread(imagepath)
        imagesize =  image.shape
        image = self.process_image(image)
        log.info("Preparing input blobs")
        input_blob = next(iter(self.net.inputs))
        out_blob = next(iter(self.net.outputs))
        self.net.batch_size = 1

        # Read and pre-process input images
        n, c, h, w = self.net.inputs[input_blob].shape

        exec_net = self.ie.load_network(network=self.net, device_name=self.device)

        # create one inference request for asynchronous execution
        request_id = 0
        infer_request = exec_net.requests[request_id];

        #prepare image
        request_wrap = InferReqWrap(infer_request, request_id)
        images = np.ndarray(shape=(1, c, h, w))
        
        if image.shape[:-1] != (h, w):
            log.warning("Image is resized from {} to {}".format(image.shape[:-1], (h, w)))
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[0] = image
        
        # Start inference request execution. Wait for last execution being completed
        request_wrap.execute("sync", {input_blob: images})

        # Processing output blob
        log.info("Processing output blob")
        
        output = infer_request.outputs[out_blob][0]
        
        output_predictions = output.argmax(0).astype("uint8")

        hs,_ = np.histogram(output_predictions.flatten(),bins=len(self.labels_map)+1,range=(0,len(self.labels_map)+1))
        classification = np.argmax(hs[1:])
        print(hs)

        print("predicted",classification,self.labels_map[classification])

#        segmented_image = cv2.resize(output_predictions,(250, 160))
        segmented_image =Image.fromarray(output_predictions)     
        segmented_image.putpalette(self.colors)
        self.ie = None
        self.net = None
            
        return (segmented_image.resize((250, 160)),self.labels_map[classification])
        
    def process_image(self, image):
        log.info("Process image")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #do the same preproccessing as in the trained model
        image = cv2.resize(image, (513,513))
        #normalize to [0,1]
        image  = image  / image.max()# max value to one    
          
        #normalize mean , std of the model        
        image -= self.mean
        image /= self.std

#        imean = np.mean(image, axis=tuple(range(image.ndim-1)))
#        istd = np.std(image, axis=tuple(range(image.ndim-1)))
        print(image.shape)
        
        return image                
