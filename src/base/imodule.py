from abc import ABCMeta, abstractmethod


class IModule(metaclass=ABCMeta):
    """
        Interface for Modules, that could be injected in pipeline
    """

    def __init__(self):
        super(IModule, self).__init__()

    @abstractmethod
    def process(self, data, **kwargs):
        """
            :param data:
            :type data: object

            :param kwargs:
            :type kwargs: any custom parameters
        """
        raise NotImplementedError('process', self.__class__.__name__)
