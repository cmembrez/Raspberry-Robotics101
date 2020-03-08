#!/bin/bash
python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model pbmodel/yolov3-tiny-leaf-train_best.graph --log_level=ERROR --reverse_input_channels --tensorflow_use_custom_operations_config yolo_v3_tiny-leaf.json --framework tf -b 1
