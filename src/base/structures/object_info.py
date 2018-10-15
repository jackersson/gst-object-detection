
class ObjectInfo(object):
    """
        Stores information about object
    """

    def __init__(self, bounding_box, confidence=1.0, class_name=None):
        """
        Args:
            bounding_box: int[4] - [x, y, w, h]
            confidence: float - [0.0, 1.0]
            class_name: str
        """

        self.class_name = class_name
        self.bounding_box = bounding_box
        self.confidence = confidence
