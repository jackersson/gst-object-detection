

class ModuleInfo(object):
    """
        Stores information about module
    """

    def __init__(self, module, name="module", init_function=None):
        """
        Args:
            module: IModule - (any implementations of image processing)
            name: str - (unique module name)
            init_function: function pointer - IModule constructor/lambda function
        """

        self.name = name
        self.module = module
        self.init_function = init_function
