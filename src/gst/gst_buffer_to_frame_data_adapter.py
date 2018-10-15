import cv2
import numpy as np

from pygst_utils import map_gst_memory, Gst

from src.base import IModule
from src.base.structures import FrameData


class GstBufferToFrameDataAdapter(IModule):
    """
        Converts Gst.Buffer to np.ndarray (RGB-colorspace)
    """

    _CHANNELS = 3

    def __init__(self):
        super(GstBufferToFrameDataAdapter, self).__init__()

    def process(self, data, **kwargs):
        """
        Args:
            data: structures.FrameData

        Returns:
            result: structures.FrameData
        """

        # Required fields
        buffer = kwargs.pop('buffer')
        width = kwargs.pop("width")
        height = kwargs.pop("height")

        memory = buffer.get_memory(0)
        if not memory:
            return data

        with map_gst_memory(memory, Gst.MapFlags.READ) as mapped:
            frame = np.ndarray(
                (height, width, self._CHANNELS), buffer=mapped, dtype=np.uint8)  # 3 = RGB
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # Set stuctures.FrameData color to parsed from Gst.Buffer Image
        data.color = frame

        return data
