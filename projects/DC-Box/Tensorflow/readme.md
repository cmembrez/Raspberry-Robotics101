# Tensorflow

In this section we would like to train a tensorflow model and run it throught the openvino model optimizer.

## Transfer Learning

In this section we train a model with a standard dataset. ImageNet, Mnist ...
After that we freeze the last layer and train it with our own dataset.

### Notebook with MobileNet v2

- Import tensorflow_hub
- Download flowers Dataset using TensorFlow Datasets
- Print Information about Flower Dataset
- Reformat images and create Batches
- Transfer Learning with TensorFlow Hub
- Load Mobile Net v2, Create a Feature Extractor
- Freeze the Pre-Trained Model
- Attach a classification head
- Train the model
- Plot Training and Validation Graphs
- Check Predictions
- Plot Model Predictions

l06c03_exercise_flowers_with_transfer_learning_solution.ipynb

### ToDo

- Export tensorflow model (saved_model.pb)
- Convert into openvino model

## New model

In this section we would like to train a completely new Tensorflow model. 
