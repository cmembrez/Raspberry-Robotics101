#!/bin/bash
python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py \
--input_model pbmodel/frozen_inference_graph.pb \
--input ImageTensor \
--output SemanticPredictions \
--input_shape [1,513,513,3] \
--output_dir openvino \
--data_type FP16

cp openvino/frozen_inference_graph.xml ../../openvino/model_leaf_segmentation_02.xml
cp openvino/frozen_inference_graph.bin ../../openvino/model_leaf_segmentation_02.bin
