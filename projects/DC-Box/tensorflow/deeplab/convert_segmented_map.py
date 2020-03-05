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

FLAGS = tf.compat.v1.flags.FLAGS

tf.compat.v1.flags.DEFINE_string('original_gt_folder',
                                 './data/segmented',
                                 'Original ground truth annotations.')

tf.compat.v1.flags.DEFINE_string('segmentation_format', 'png', 'Segmentation format.')

tf.compat.v1.flags.DEFINE_string('output_dir_class_raw',
                                 './data/SegmentationClassRaw',
                                 'folder to save modified ground truth annotations.')

tf.compat.v1.flags.DEFINE_string('output_dir_class',
                                 './data/SegmentationClass',
                                 'folder to save modified ground truth annotations.')


def _remove_colormap(filename):
  """Removes the color map from the annotation.

  Args:
    filename: Ground truth annotation filename.

  Returns:
    Annotation without color map class id 0 or 1.
  """
  return np.array(Image.open(filename)).astype(np.uint8)


def _save_annotation(pil_image, filename):
  """Saves the annotation as png file.

  Args:
    annotation: Segmentation annotation.
    filename: Output filename.
  """
  with tf.io.gfile.GFile(filename, mode='w') as f:
    pil_image.save(f, 'PNG')


def main(unused_argv):
    
  # voc dataset color map
  palette = [2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1]
  colors = np.array([i for i in range(21)])[:, None] * palette
  colors = (colors % 255).astype("uint8")
      
  # Create the output directory if not exists.
  if not tf.io.gfile.isdir(FLAGS.output_dir_class_raw):
    tf.io.gfile.makedirs(FLAGS.output_dir_class_raw)
  if not tf.io.gfile.isdir(FLAGS.output_dir_class):
    tf.io.gfile.makedirs(FLAGS.output_dir_class)

  annotations = glob.glob(os.path.join(FLAGS.original_gt_folder,
                                       '*.' + FLAGS.segmentation_format))
  for annotation in annotations:
    raw_annotation = _remove_colormap(annotation)
    raw_image = Image.fromarray(raw_annotation)
    
    class_image =Image.fromarray(raw_annotation)     
    class_image.putpalette(colors)
    
    filename = os.path.basename(annotation)[:-4]
    _save_annotation(raw_image,
                     os.path.join(
                         FLAGS.output_dir_class_raw,
                         filename + '.' + FLAGS.segmentation_format))

    _save_annotation(class_image,
                     os.path.join(
                         FLAGS.output_dir_class,
                         filename + '.' + FLAGS.segmentation_format))



if __name__ == '__main__':
  tf.compat.v1.app.run()
