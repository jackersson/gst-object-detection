import traceback

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject


class GstPipelinesController(object):

    def __init__(self):
        self.main_loop = GObject.MainLoop()
        self.pipelines_by_id = {}
        self.active_pipelines = []

    def append(self, pipeline):
        assert pipeline.idx not in self.pipelines_by_id
        self.pipelines_by_id[pipeline.idx] = pipeline

    def bus_call(self, bus, message, pipeline_id):
        if message.type == Gst.MessageType.EOS or \
                message.type == Gst.MessageType.ERROR or \
                message.type == Gst.MessageType.WARNING:

            assert pipeline_id in self.pipelines_by_id
            self.active_pipelines.remove(pipeline_id)

            if not self.active_pipelines:
                self.stop()

        return True

    def run(self):
        pipelines = list(self.pipelines_by_id.values())
        for p in pipelines:
            p.bus().connect("message", self.bus_call, p.idx)
            p.start()

            self.active_pipelines.append(p.idx)

        try:
            self.main_loop.run()
        except:
            traceback.print_exc()
            self.stop()

    def stop(self):
        pipelines = list(self.pipelines_by_id.values())

        for p in pipelines:
            p.stop()

        self.active_pipelines = []
        self.main_loop.quit()