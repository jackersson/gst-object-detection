import os

from .utils import get_media_source_type, MediaSourceType


def bool_to_string(flag):
    """
        Converts bool to string

        Args:
            flag: bool

        Returns:
            result: str ("true"/"false")
    """
    return "true" if flag else "false"


def to_gst_pipeline(source, modules=[], index=0, show_window=False, show_fps=False, sync=False):
    source_type = get_media_source_type(source)

    if source_type == MediaSourceType.FILE:
        return gst_pipeline_from_file(source, modules, index=index, show_window=show_window, show_fps=show_fps, sync=sync)

    raise NotImplementedError("Gst Pipeline Not Implemented")


def gst_pipeline_from_file(filename, modules=[], index=0, show_window=False, show_fps=False, sync=False):

    assert os.path.isfile(filename)

    plugins = "filesrc location={} ! ".format(filename)
    plugins += "decodebin ! "
    plugins += "videoconvert ! "
    plugins += "video/x-raw,format=RGB ! "
    plugins += "videoconvert ! "

    for module in modules:
        plugins += "gstplugin_py name={} ! ".format(module)

    plugins += "videoconvert ! "

    is_sync = "sync=True" if sync else "sync=False"
    sink = "gtksink" if show_window else "fakesink"

    if show_fps:
        fps_plugin_name = "fps_{}".format(index)
        plugins += "fpsdisplaysink video-sink=={} sync={} name={} ".format(
            sink, bool_to_string(sync), fps_plugin_name)
    else:
        plugins += "{} sync={} ".format(sink, bool_to_string(sync))

    return plugins
