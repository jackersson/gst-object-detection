import numpy as np


class FrameData(object):
    """
        Stores information about frame

        Class is used as unified format to pass from model to model
    """

    def __init__(self, color, offset=0, objects=[]):
        """
        Args:
            color: np.ndarray - image of size [h, w, c], (RGB-colorspace, c=3)
            offset: int - frame number from the beginning
            objects: ObjectInfo[] - list of objects present on current frame
        """

        super(FrameData, self).__init__()

        self.color = color
        self.offset = offset

        self.objects = objects

    def has_color(self):
        """ Checks if FrameData contains color image

        Returns:
            bool: True (if FrameData contains color image), else - False
        """
        return isinstance(self.color, np.ndarray)
