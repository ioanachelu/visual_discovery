from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from tools import _init_paths
from model.config import cfg
from model.test import im_detect
from model.nms_wrapper import nms
from math import ceil
from utils.timer import Timer
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import os
import tensorflow as tf
from nets.vgg16 import vgg16
# from utils.im_util import read_img_base64

ES_INDEX_NAME = 'visual_discovery'
ES_DOC_TYPE = 'image_index'

es = Elasticsearch(hosts='0.0.0.0:9200')


def _binarize_fea(x, thresh):
  '''binary and pack feature vector'''
  binary_vec = np.where(x >= thresh, 1, 0)
  f_len = binary_vec.shape[0]
  if f_len % 32 != 0:
    new_size = int(ceil(f_len / 32.) * 32)
    num_pad = new_size - f_len
    binary_vec = np.pad(binary_vec, (num_pad, 0), 'constant')

  return np.packbits(binary_vec).view('uint32')


def push_image(phash, actions):
  doc = {
    "hash": phash
  }
  action = {
    "_index": ES_INDEX_NAME,
    "_type": ES_DOC_TYPE,
    "_source": doc
  }
  actions.append(action)
  return actions


def search_image(phash):
  QUERY = """
  {
  "query": {
    "function_score" : {
      "query" : {
        "match_all" : {
          "boost" : 1.0
        }
      },
      "functions" : [
        {
          "filter" : {
            "match_all" : {
              "boost" : 1.0
            }
          },
          "script_score" : {
            "script" : {
              "inline" : "hamming_distance",
              "lang" : "native",
              "params" : {
                "field" : "hash",
                "hash" : "##fea##",
                "verbose" : true
              }
            }
          }
        }
      ],
      "score_mode" : "sum",
      "boost_mode" : "replace",
      "max_boost" : 3.4028235E38,
      "boost" : 1.0
    }
  }
  }
  """
  # phash_str = ','.join([str(int(t)) for t in phash])
  query = QUERY.replace('##fea##', phash_str)
  search_results = es.search(index=ES_INDEX_NAME, doc_type=ES_DOC_TYPE, body=query)

  return search_results

# pow2=2**np.range(64,dtype=np.uint32)
#
# @jit("uint64(uint64[:])")
# def convert3(arr):
#     y = 0
#     for i in range(arr.size):
#         y= y + pow2[i] * arr[i]
#     return y


actions = []

# v = np.array([1, 1, 0, 1, 1, 0, 1, 1])
# v = int.from_bytes(np.packbits(v), byteorder='big')

v = np.array([1] * 4093 + [0, 0, 0])
output = _binarize_fea(v, thresh=0.1)
phash_str = ','.join([str(int(t)) for t in output])
actions = push_image(phash_str, actions)
v = np.array([1] * 4093 + [1, 0, 0])
output = _binarize_fea(v, thresh=0.1)
phash_str = ','.join([str(int(t)) for t in output])
actions = push_image(phash_str, actions)
v = np.array([1] * 4093 + [1, 1, 0])
output = _binarize_fea(v, thresh=0.1)
phash_str = ','.join([str(int(t)) for t in output])
actions = push_image(phash_str, actions)
helpers.bulk(es, actions)

v = np.array([1] * 4093 + [1, 1, 1])
output = _binarize_fea(v, thresh=0.1)
phash_str = ','.join([str(int(t)) for t in output])
search_results = search_image(phash_str)
print(search_results)
