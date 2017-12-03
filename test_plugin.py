from elasticsearch import Elasticsearch
from elasticsearch import helpers
import numpy as np

ES_INDEX_NAME = 'visual_discovery'
ES_DOC_TYPE = 'image_index'

es = Elasticsearch(hosts='0.0.0.0:9200')



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
  query = QUERY.replace('##fea##', phash)
  search_results = es.search(index=ES_INDEX_NAME, doc_type=ES_DOC_TYPE, body=query)

  return search_results

actions = []
v = np.packbits(np.asarray([1, 1, 1, 1, 1, 1, 1, 0, 0, 0])).view("uint32")
actions = push_image(v, actions)
v = np.packbits([1, 1, 1, 1, 1, 1, 1, 1, 0, 0]).view("uint32")
actions = push_image(v, actions)
v = np.packbits([1, 1, 1, 1, 1, 1, 1, 1, 1, 0]).view("uint32")
actions = push_image(v, actions)
helpers.bulk(es, actions)

v = np.packbits([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).view("uint32")
search_results = search_image(v)
print(search_results)
