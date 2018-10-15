
from .gst_pipeline_base import GstPipelineBase
from .gst_pipeline_builders import to_gst_pipeline


class GstPipeline(object):

    _COUNTER = 0

    def __init__(self, source, modules, **kwargs):
        if "index" in kwargs:
            self.idx = kwargs.pop("index")
        else:
            self.idx = self._COUNTER
            self._COUNTER += 1

        modules = modules
        names = ["{}_{}".format(m.name, self.idx) for m in modules]

        gst_plugins = to_gst_pipeline(source, names, index=self.idx, **kwargs)
        pipeline = GstPipelineBase(gst_plugins)

        for name, module in zip(names, modules):
            ret, element = pipeline.get_element(name)
            if ret:
                element.set_property("model", module.module)

        fps_name = "fps_{}".format(self.idx)
        ret, element = pipeline.get_element(fps_name)
        if ret:
            element.set_property("signal-fps-measurements", True)
            element.connect('fps-measurements', self.on_fps)

        self.pipeline = pipeline

    def on_fps(self, element, fps, droprate, avgfps):
        print("Pipeline ({}):  current: {} average: {} ".format(
            self.idx, fps, avgfps))

    def bus(self):
        return self.pipeline._bus

    def start(self):
        self.pipeline.start()

    def stop(self):
        self.pipeline.stop()
