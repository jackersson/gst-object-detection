from src.base import IModule
from src.base.structures import FrameData


class FrameDataSource(IModule):

    def __init__(self):
        self.offset = -1

    def process(self, data, **kwargs):
        self.offset += 1
        return FrameData(None, offset=self.offset, objects=[])
