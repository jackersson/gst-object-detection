from src.base.structures import FrameData


class Bin(object):

    def __init__(self, elements):
        self.elements = elements

    def process(self, item, **kwargs):
        data = item
        for element in self.elements:
            data = element.process(data, **kwargs)
            assert isinstance(data, FrameData), "Invalid type. {} != {}".format(
                type(data), FrameData.__class__.__name__)

        return data
