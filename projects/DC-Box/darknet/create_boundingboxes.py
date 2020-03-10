"""Removes the color map from segmentation annotations.

Removes the color map from the ground truth segmentation annotations and save
the results to output_dir.
"""
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
import glob
import os.path
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2

FLAGS = tf.compat.v1.flags.FLAGS

tf.compat.v1.flags.DEFINE_string('original_gt_folder',
                                 './data/images',
                                 'Original ground truth annotations.')

tf.compat.v1.flags.DEFINE_string('output_dir_boundingbox',
                                 './data',
                                 'folder to save modified ground truth annotations.')


def _remove_colormap(filename):
  """Removes the color map from the annotation.

  Args:
    filename: Ground truth annotation filename.

  Returns:
    Annotation without color map class id 0 or 1.
  """
  return np.array(Image.open(filename)).astype(np.uint8)


def boundingbox(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray= cv2.GaussianBlur(gray, (7,7),0)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,17,2)
    edges = cv2.Canny(thresh,50,150)

    kernel = np.ones((5,5), dtype=np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    _,contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(cnt)
    return(x,y,w,h)

def process(imagepath):
    image = cv2.imread(imagepath)
    (x,y,w,h)=boundingbox(image)
    if x == 0 or y == 0:
        imgcropped = image[50:image.shape[0]-50, 50:image.shape[1]]
        (x,y,w,h) = boundingbox(imgcropped)
        x+=50
        y+=50
    
    height,width,_ = image.shape
#    print(x,y,w,h,width,height)
    xm=(x+(w*0.5))/width
    ym=(y+(h*0.5))/height
    wr=w/width
    hr=h/height
#    print(x,y,w,h)
#    print(xm,ym,wr,hr)
    if x == 0 or y == 0:
        print("bad bunding box:",x,y,w,h,width,height)
        return None
	
    return (xm,ym,wr,hr)
    

def main(unused_argv):
    

  annotations = glob.glob(os.path.join(FLAGS.original_gt_folder,'*.jpg'))
  for annotation in annotations:
    try:
        raw_annotation = _remove_colormap(annotation)
        (x1,y1,x2,y2) = process(annotation)
        line = '1 {0} {1} {2} {3}'.format(x1,y1,x2,y2)
    
        annotion_path = annotation[:-3]+'txt'
        with open(annotion_path, "w") as f:
            f.writelines([line])
    except:
        print("skip "+annotation)
    

if __name__ == '__main__':
  tf.compat.v1.app.run()
