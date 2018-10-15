import os
import logging
import tensorflow as tf

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

GObject.threads_init()
Gst.init(None)

from src.gst import GstPipeline as Pipeline
from src.gst import GstPipelinesController as PipelinesController
from src.gst import GstBufferToFrameDataAdapter

from src.base import ModuleInfo
from src.modules import *

from view import ColorPicker, OverlayOpenCV

from tf_object_detection_model import TfObjectDetectionModel

from utils import load_labels_pbtxt

tf.logging.set_verbosity(tf.logging.ERROR)
logging.basicConfig(level=0)

# Create object that launches Gstreamer Pipelines
pipelines_controller = PipelinesController()

# VIDEO FILENAME
filename = "video.mp4"
# LABELS FILE
labels_file = os.path.join("data/mscoco_label_map.pbtxt")

# WEIGHTS
weights = "data/models/ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb"

# Load labels
labels = load_labels_pbtxt(labels_file)

# Create Object Detector
object_detector = TfObjectDetectionModel(
    weights, device='/device:GPU:0', threshold=0.1, labels=labels)

# Simple bin of elements
module_bin = Bin([
    FrameDataSource(),  # Create Frame Data
    GstBufferToFrameDataAdapter(),  # Convert Gst.Buffer to image and update FrameData.color
    ObjectDetectorAdapter(object_detector),  # Run Object Detection on frame and fill FrameData.objects
    OverlayOpenCV(ColorPicker(n_colors=len(labels)))  # Draw objects on frame
])

# Wrap bin with ModuleInfo (so additional meta data could be added)
modules = [ModuleInfo(module=module_bin)]

# Create pipeline
pipeline = Pipeline(source=filename, modules=modules,
                    show_window=True, show_fps=True)

# Add pipeline to PipelinesController
pipelines_controller.append(pipeline)

# Launch all pipelines
pipelines_controller.run()