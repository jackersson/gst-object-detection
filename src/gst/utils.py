import os

VIDEO_FILES_EXTESIONS = ['.mpg', '.avi', '.mov', '.mp4']


class MediaSourceType:
    FILE = "file"
    WEBCAMERA = "camera"
    RTSP = "rtsp"
    HTTP = "http"


def get_media_source_type(source):
    source = str(source)

    if MediaSourceType.RTSP in source:
        return MediaSourceType.RTSP

    if MediaSourceType.HTTP in source:
        return MediaSourceType.HTTP

    filename = os.path.basename(source)
    _, ext = os.path.splitext(filename)

    if ext.lower() in VIDEO_FILES_EXTESIONS:
        return MediaSourceType.FILE

    return MediaSourceType.WEBCAMERA
