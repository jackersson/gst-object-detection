from .imodule import IModule
from .structures import FrameData


class FrameDataModule(IModule):
    """
        Check that incoming and outcoming data is FrameData.
        Specific for FrameData Pipelines
    """

    def __init__(self, module):
        """
        Args:
            module: IModule
        """
        super(FrameDataModule, self).__init__()

        self.module = module

    def process(self, data, **kwargs):
        """
        Args:
            data: structures.FrameData

        Returns:
            result: structures.FrameData
        """

        assert isinstance(data, FrameData), "Invalid type. {} != {}".format(
            type(data), FrameData.__class__.__name__)

        result = self.module.process(data, **kwargs)

        assert isinstance(result, FrameData), "Invalid type. {} != {}".format(
            type(result), FrameData.__class__.__name__)

        return result
