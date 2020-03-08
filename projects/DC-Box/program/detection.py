#!/usr/bin/env python
import sys
import os
import cv2
import numpy as np
import logging as log
from openvino.inference_engine import IENetwork, IECore
from PIL import ImageTk, Image
import threading
from tinyyolov3 import TinyYOLOv3,TinyYOLOV3Params

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


class Detector:
    def __init__(self, modelpath, device, cpu_extension):
        
        self.model_xml = modelpath
        self.model_bin = os.path.splitext(modelpath)[0] + ".bin"
        self.device = device
        self.cpu_extension = cpu_extension
        
        self.mean = np.array([0.485, 0.456, 0.406])        
        self.std = np.array([0.229, 0.224, 0.225])
        
        self.labels_map = {}
        self.labels_map[0] = 'backround'
        self.labels_map[1] = 'leaf'
        self.labels_map[2] = 'other'
        self.iou_threshold = 0.1
        self.prob_threshold = 0.1
        self.anchors = [10.0, 13.0, 16.0, 30.0, 33.0, 23.0, 30.0, 61.0, 62.0, 45.0, 59.0, 119.0, 116.0, 90.0,
                                  156.0, 198.0, 373.0, 326.0]
            
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
                
    def detection(self,imagepath):
        self.init_device()
        orig = cv2.imread(imagepath)
        imagesize =  orig.shape
        image = self.process_image(orig)
        
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
        
#        output = infer_request.outputs[out_blob][0]
        
#        print(output.shape)
        
        objects = []

        # loop over the output items
        for (layerName, outBlob) in infer_request.outputs.items():
            # create a new object which contains the required tinyYOLOv3
            # parameters
            layerParams = TinyYOLOV3Params(self.net.layers[layerName].params,
                outBlob.shape[2])
    
            # parse the output region
            detection = TinyYOLOv3.parse_yolo_region(outBlob,
                image.shape[1:], imagesize[:-1], layerParams,
                self.prob_threshold)
            objects += detection 
    
        # loop over each of the objects
        for i in range(len(objects)):
            # check if the confidence of the detected object is zero, if
            # it is, then skip this iteration, indicating that the object
            # should be ignored
            if objects[i]["confidence"] == 0:
                continue
    
            # loop over remaining objects
            for j in range(i + 1, len(objects)):
                # check if the IoU of both the objects exceeds a
                # threshold, if it does, then set the confidence of that
                # object to zero
                if TinyYOLOv3.intersection_over_union(objects[i],
                    objects[j]) > self.iou_threshold:
                    objects[j]["confidence"] = 0
    
        # filter objects by using the probability threshold -- if a an
        # object is below the threshold, ignore it
        objects = [obj for obj in objects if obj['confidence'] >= \
            self.prob_threshold]
    
        # store the height and width of the original frame
        (endY, endX) = imagesize[:-1]
    
        # loop through all the remaining objects
        label='None'
        for obj in objects:
            # validate the bounding box of the detected object, ensuring
            # we don't have any invalid bounding boxes
#            if obj["xmax"] > endX or obj["ymax"] > endY or obj["xmin"] \
#                < 0 or obj["ymin"] < 0:
#                continue
    
            # build a label consisting of the predicted class and
            # associated probability
            label = "{}: {:.2f}%".format(self.labels_map[obj["class_id"]],
                obj["confidence"] * 100)
            
#            print(label,obj)
    
            # calculate the y-coordinate used to write the label on the
            # frame depending on the bounding box coordinate
            y = obj["ymin"] - 15 if obj["ymin"] - 15 > 15 else \
                obj["ymin"] + 15
    
            # draw a bounding box rectangle and label on the frame
            cv2.rectangle(orig, (obj["xmin"], obj["ymin"]), (obj["xmax"], obj["ymax"]), (0, 0, 255), 2)
#            cv2.putText(orig, label, (obj["xmin"], y),
#                cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS[obj["class_id"]], 3)
                    
        #orig.resize((300, 200))
        orig = cv2.cvtColor(orig, cv2.COLOR_RGB2BGR)
        orig = cv2.resize(orig, (300,200))
        return (Image.fromarray(orig),label)
        
    def process_image(self, image):
        log.info("Process image")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        return image                

