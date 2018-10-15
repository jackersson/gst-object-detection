import os
import json
import tensorflow as tf

from google.protobuf import text_format
from data.protos import string_int_label_map_pb2

'''
def load_labels_pbtxt(filename):
    assert os.path.isfile(filename), "File not exists: {}".format(filename)

    labels = {}
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            try:
                loaded = json.loads(line)
                labels[loaded["id"]] = loaded["display_name"]
            except Exception as e:
                print(i, e)
        return labels
'''


def load_labels_pbtxt(path):
    """Loads label map proto.
    Args:
      path: path to StringIntLabelMap proto text file.
    Returns:
      a StringIntLabelMapProto
    """
    with tf.gfile.GFile(path, 'r') as fid:
        label_map_string = fid.read()
        label_map = string_int_label_map_pb2.StringIntLabelMap()
        try:
            text_format.Merge(label_map_string, label_map)
        except text_format.ParseError:
            label_map.ParseFromString(label_map_string)
    # _validate_label_map(label_map)

    result = {}
    for item in label_map.item:
        if item.id < 0:
            raise ValueError('Label map ids should be >= 0.')
        if (item.id == 0 and item.name != 'background' and
                item.display_name != 'background'):
            raise ValueError(
                'Label map id 0 is reserved for the background label')
        result[item.id] = item.display_name
    return result
