import os
import tensorflow as tf
import numpy as np


def is_gpu(device):
    return "gpu" in device.lower()


def create_config(device='/device:CPU:0',
                  per_process_gpu_memory_fraction=0.0,
                  log_device_placement=False):

    if is_gpu(device):
        config = tf.ConfigProto(log_device_placement=log_device_placement)
        if per_process_gpu_memory_fraction > 0.0:
            config.gpu_options.per_process_gpu_memory_fraction = per_process_gpu_memory_fraction
        else:
            config.gpu_options.allow_growth = True
    else:
        config = tf.ConfigProto(
            log_device_placement=log_device_placement, device_count={'GPU': 0})

    return config


def parse_graph_def(model_path):
    model_path = os.path.abspath(model_path)
    assert os.path.isfile(model_path), "Invalid filename {}".format(model_path)
    with tf.gfile.GFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    return graph_def


def import_graph(graph_def, device, name=""):
    with tf.device(device):
        graph = tf.Graph()
        with graph.as_default():
            tf.import_graph_def(graph_def, name=name)
            return graph


class TfObjectDetectionModel(object):

    def __init__(self, weights,
                 threshold=0.5,
                 device='/device:CPU:0',
                 per_process_gpu_memory_fraction=0.0,
                 log_device_placement=False,
                 labels=[]):

        # TODO Docs

        # self.weights = weights

        graph_def = parse_graph_def(weights)
        config = create_config(device,
                               log_device_placement=log_device_placement,
                               per_process_gpu_memory_fraction=per_process_gpu_memory_fraction)
        graph = import_graph(graph_def, device)

        self.session = tf.Session(graph=graph, config=config)

        # Taken from official website
        self.input = graph.get_tensor_by_name("image_tensor:0")

        # Taken from official website
        output_names = ["detection_classes:0",
                        "detection_boxes:0", "detection_scores:0"]
        self.output = [graph.get_tensor_by_name(name) for name in output_names]

        self.threshold = threshold
        self.labels = labels

        # warm up
        self.process(np.zeros((1, 1, 3), dtype=np.uint8))

    def process(self, image, **kwargs):

        # For profiling
        options = kwargs["options"] if "options" in kwargs else None
        run_metadata = kwargs["run_metadata"] if "run_metadata" in kwargs else None

        classes, boxes, scores = self.session.run(self.output,
                                                  feed_dict={
                                                      self.input: np.expand_dims(image, 0)},
                                                  options=options, run_metadata=run_metadata)

        h, w = image.shape[:2]
        box_scaler = np.array([h, w, h, w])

        objects = []
        for i in range(len(boxes)):
            for class_id, box, score in zip(classes[i], boxes[i], scores[i]):

                if class_id not in self.labels:
                    continue

                if score < self.threshold:
                    continue

                ymin, xmin, ymax, xmax = box * box_scaler

                object_info = {'confidence': float(score),
                               'bounding_box': [int(xmin), int(ymin), int(xmax - xmin), int(ymax - ymin)],
                               'class_name': self.labels[class_id]}

                objects.append(object_info)
        return objects

    def release(self):
        """
            Releases model
            tf.Session should be closed/released
        """

        if self.session is not None:
            self.session.close()

    def __del__(self):
        """
            Releases model when object deleted
        """
        self.release()
