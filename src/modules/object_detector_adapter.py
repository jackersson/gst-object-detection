import numpy as np

from src.base.structures import ObjectInfo, FrameData
from src.base import IModule


class ObjectDetectorAdapter(IModule):

    def __init__(self, model, frames_to_skip=0):
        self.model = model

        # Warm up model (First launch is too slow)
        self.model.process(np.zeros((1, 1, 3), dtype=np.uint8))

        self.counter = 0
        self.frames_to_skip = frames_to_skip

    def process(self, data, **kwargs):
        assert isinstance(data, FrameData), "Invalid type. {} != {}".format(
            type(data), FrameData.__class__.__name__)

        if self.counter < self.frames_to_skip:
            self.counter += 1
            return data

        assert data.has_color(), "Frame Data has no color image"
        result = self.model.process(data.color)
        self.counter = 0

        for obj in result:
            object_info = ObjectInfo(
                bounding_box=obj["bounding_box"], confidence=obj["confidence"], class_name=obj["class_name"])
            data.objects.append(object_info)

        return data
