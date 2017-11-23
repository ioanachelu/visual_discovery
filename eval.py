from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tools import _init_paths
# from model.config import cfg
from model.test import im_detect
from model.nms_wrapper import nms

from utils.timer import Timer
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os, cv2
import argparse
import os
import tensorflow as tf
from nets.vgg16 import vgg16

CLASSES = ('background',
'person', 'bicycle', 'car', 'motorcycle', 'airplane',
'bus','train', 'truck', 'boat', 'traffic light', 'fire hydrant',
'stop sign', 'parking meter','bench', 'bird', 'cat', 'dog',
'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
'backpack','umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
'skis', 'snowboard', 'sports ball', 'kite','baseball bat', 'baseball glove',
'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
'fork', 'knife', 'spoon', 'bowl','banana', 'apple', 'sandwich', 'orange',
'broccoli','carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
'potted plant', 'bed', 'dining table','toilet', 'tv', 'laptop', 'mouse', 'remote',
'keyboard', 'cell phone', 'microwave', 'oven','toaster', 'sink', 'refrigerator',
'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush')

def extract(sess, net, image_path):
  im = cv2.imread(image_path)
  scores, boxes, feature_maps = im_detect(sess, net, im)

  CONF_THRESH = 0.8
  NMS_THRESH = 0.3
  results = []
  for cls_ind, cls in enumerate(CLASSES[1:]):
    cls_ind += 1  # because we skipped background
    cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
    cls_scores = scores[:, cls_ind]
    dets = np.hstack((cls_boxes,
                      cls_scores[:, np.newaxis])).astype(np.float32)
    keep = nms(dets, NMS_THRESH)
    dets = dets[keep, :]
    feature_maps_nms = feature_maps[keep, :]
    results.append((dets, feature_maps_nms))
    # vis_detections(im, cls, dets, thresh=CONF_THRESH)
  print("end")

if __name__ == '__main__':
  tfmodel = '/Users/ioanaveronicachelu/visual_discovery/vgg_model_weights/vgg16_faster_rcnn_iter_1190000.ckpt'

  if not os.path.isfile(tfmodel + '.meta'):
    raise IOError('{:s} not found')

  tfconfig = tf.ConfigProto(allow_soft_placement=True)
  tfconfig.gpu_options.allow_growth = True

  # init session
  sess = tf.Session(config=tfconfig)
  # load network
  net = vgg16()

  net.create_architecture("TEST", 81,
                          tag='default', anchor_scales=[4, 8, 16, 32])
  saver = tf.train.Saver()
  saver.restore(sess, tfmodel)

  print('Loaded network {:s}'.format(tfmodel))

  im_path = '/Users/ioanaveronicachelu/visual_discovery/images/val2017/000000000885.jpg'
  extract(sess, net, im_path)

  plt.show()
