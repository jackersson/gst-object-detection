import cv2

from src.base import IModule
from src.base.structures import ObjectInfo, FrameData

# from .color_picker import ColorPicker


class OverlayOpenCV(IModule):

    def __init__(self, colors, line_thickness=1,
                 text_color=[255, 255, 255],
                 text_thickness=1):

        self.colors = colors

        self.text_color = text_color
        self.line_thickness = line_thickness
        self.text_thickness = text_thickness

        self.tracks = {}

    def process(self, data, **kwargs):

        assert isinstance(data, FrameData), "Invalid type. {} != {}".format(
            type(data), FrameData.__class__.__name__)

        assert data.has_color(), "FrameData has no color image"

        image = data.color
        self.line_thickness = int(sum(image.shape[:2]) // 800)
        self.text_thickness = int(sum(image.shape[:2]) // 800)

        for obj in data.objects:

            assert isinstance(obj, ObjectInfo), "Invalid type. {} != {}".format(
                type(data), ObjectInfo.__class__.__name__)

            color = self.colors.get(obj.class_name)

            # draw main rectangles
            x, y, w, h = list(map(lambda x: int(x), obj.bounding_box))
            cv2.rectangle(image, (x, y), (x + w, y + h),
                          color, self.line_thickness)

            # draw tableu
            tableu_offset = 30
            top_table = y - tableu_offset
            cv2.rectangle(image, (x, top_table), (x + w, y), color, cv2.FILLED)

            cv2.putText(image, obj.class_name, (x, y),
                cv2.FONT_HERSHEY_TRIPLEX, 1, self.text_color, self.text_thickness)

        return data

