#!/usr/bin/env python
import sys
import os
import cv2
import numpy as np
import logging as log
from openvino.inference_engine import IENetwork, IECore
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


class Classifier:
    def __init__(self, modelpath, device, cpu_extension,labelspath):
        
        self.model_xml = modelpath
        self.model_bin = os.path.splitext(modelpath)[0] + ".bin"
        self.device = device
        
        self.mean = np.array([0.485, 0.456, 0.406])
        self.std = np.array([0.229, 0.224, 0.225])
        
        #read labels map fromn file
        self.labels_map = None
        if not labelspath is None: 
            log.info("Read Labels File")
            with open(labelspath, 'r') as f:
                self.labels_map = [x.split(sep=' ', maxsplit=1)[-1].strip() for x in f]
        else:
            log.info("No Labels are defined")
            
        
        log.info("Creating Inference Engine")
        self.ie = IECore()
        if cpu_extension and 'CPU' in device:
            self.ie.add_extension(cpu_extension, "CPU")
            log.info("Added CPU extension")
        
        log.info("Loading network files:\n\t{}\n\t{}".format(self.model_xml, self.model_bin))
        self.net = IENetwork(model=self.model_xml, weights=self.model_bin)

        if "CPU" in device:
            supported_layers = self.ie.query_network(self.net, "CPU")
            not_supported_layers = [l for l in self.net.layers.keys() if l not in supported_layers]
            if len(not_supported_layers) != 0:
                log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(device, ', '.join(not_supported_layers)))
                log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
                
                self.ie = None
                self.net = None
                
    def classify(self,imagepath, number_top, printResult):
        image = cv2.imread(imagepath)
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
        
        res = infer_request.outputs[out_blob]
        
        if printResult:
            self.printResult(res,number_top)
            
        prob = np.max(np.squeeze(res))
        classid = np.argmax(np.squeeze(res))
        classlabel = self.labels_map[classid] if self.labels_map else "{}".format(id)
        
        return (prob,classlabel)
        
    def printResult(self, res,number_top):
        log.info("Top {} results: ".format(number_top))
        classid_str = "classid"
        probability_str = "probability"
        for i, probs in enumerate(res):
            probs = np.squeeze(probs)
            top_ind = np.argsort(probs)[number_top:][::-1]
            print(classid_str, probability_str)
#            print("{} {}".format('-' * len(classid_str), '-' * len(probability_str)))
            j=0
            for id in top_ind:
                det_label = self.labels_map[id] if self.labels_map else "{}".format(id)
                label_length = len(det_label)
                space_num_after = 20 - label_length
                space_num_before_prob = (8 - len(str(probs[id])))
                print("{:20}{:.7f}".format(det_label,probs[id]))
                j+=1
                if j >= number_top:
                    return
                
    def process_image(self, image):
        log.info("Process image")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #do the same preproccessing as in the trained model
        image = cv2.resize(image, (256,256))
        upper_pixel = (256 - 224) // 2
        left_pixel = (256 - 224) // 2        
        image = image[upper_pixel:224, left_pixel:224]
        #normalize to 0,1 mean, std
        image  = image  / image.max() # max value to one    
          
        imean = np.mean(image, axis=tuple(range(image.ndim-1)))
        istd = np.std(image, axis=tuple(range(image.ndim-1)))
        print(imean,istd)

        #normalize to 0 mean std 1        
        image -= imean   
        image  /= istd 
         
        #mean , std of the model        
        image *= self.std
        image += self.mean
    
        return image                
