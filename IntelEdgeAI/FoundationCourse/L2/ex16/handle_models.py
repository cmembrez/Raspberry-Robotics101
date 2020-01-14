import cv2
import numpy as np


def handle_pose(output, input_shape):
    '''
    Handles the output of the Pose Estimation model.
    Returns ONLY the keypoint heatmaps, and not the Part Affinity Fields.
    '''
    # dict_keys(['Mconv7_stage2_L1', 'Mconv7_stage2_L2'])

    # TODO 1: Extract only the second blob output (keypoint heatmaps)
    heatmap = output['Mconv7_stage2_L2']

    # TODO 2: Resize the heatmap back to the size of the input

    # output-map goes into an empty array
    heatmap_resized = np.zeros([heatmap.shape[1],
                                input_shape[0],
                                input_shape[1]
                                ])
    # iterate through the 18points heatmap and resize them
    # because cv2.resize handle only 1-3 dim and not more
    for point in range(len(heatmap[0])):
        heatmap_resized[point] = cv2.resize(heatmap[0][point],
                                            input_shape[0:2][::-1]
                                            )

    return heatmap_resized


def handle_text(output, input_shape):
    '''
    Handles the output of the Text Detection model.
    Returns ONLY the text/no text classification of each pixel,
        and not the linkage between pixels and their neighbors.
    '''
    # dict_keys(['model/segm_logits/add', 'model/link_logits_/add'])

    # TODO 1: Extract only the first blob output (text/no text classification)
    textNo = output["model/segm_logits/add"]
    # TODO 2: Resize this output back to the size of the input

    # prepare an empty array to store resized texts
    textNo_resized = np.zeros([textNo.shape[1],
                               input_shape[0],
                               input_shape[1]
                               ])
    # iterate and resize each text
    for txt in range(len(textNo[0])):
        textNo_resized[txt] = cv2.resize(textNo[0][txt],
                                         input_shape[0:2][::-1]
                                         )
    return textNo_resized


def handle_car(output, input_shape):
    '''
    Handles the output of the Car Metadata model.
    Returns two integers: the argmax of each softmax output.
    The first is for color, and the second for type.
    '''
    # TODO 1: Get the argmax of the "color" output
    color = output['color'].flatten()
    color_class = np.argmax(color)

    # TODO 2: Get the argmax of the "type" output
    car_type = output['type'].flatten()
    type_class = np.argmax(car_type)

    return color_class, type_class


def handle_output(model_type):
    '''
    Returns the related function to handle an output,
        based on the model_type being used.
    '''
    if model_type == "POSE":
        return handle_pose
    elif model_type == "TEXT":
        return handle_text
    elif model_type == "CAR_META":
        return handle_car
    else:
        return None


'''
The below function is carried over from the previous exercise.
You just need to call it appropriately in `app.py` to preprocess
the input image.
'''


def preprocessing(input_image, height, width):
    '''
    Given an input image, height and width:
    - Resize to width and height
    - Transpose the final "channel" dimension to be first
    - Reshape the image to add a "batch" of 1 at the start 
    '''
    image = np.copy(input_image)
    image = cv2.resize(image, (width, height))
    image = image.transpose((2, 0, 1))
    image = image.reshape(1, 3, height, width)

    return image