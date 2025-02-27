import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL.ImageDraw import Draw


class Drawing:
    def __init__(self, base_img, scale):
        self._color = (255, 0, 0)
        self._tmp_color = (0, 0, 255)
        self._thickness = 3
        self.font = ImageFont.load_default()
        self._text_margin = 10
        self._scale_margin = 10

        if base_img:
            new_size = [int(x * scale) for x in base_img.size]
            self.base_img = base_img.copy().resize(new_size)
            self.canvas = self.base_img.copy()
        self.scale = scale

    def _draw_rect(self, dr, rect, width=4, color="red", text=""):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        for r in range(0, width):
            dr.rectangle([x1 + r, y1 + r, x2 - r, y2 - r], outline=color)
        dr.rectangle([x2 - self._scale_margin, y2 - self._scale_margin, x2, y2], fill=color)
        dr.text((x1 + self._text_margin, y1 + 5), text, fill="red", font=self.font)

    def _transformed_rect(self, rect):
        return [x * self.scale for x in rect]

    def draw_template(self, template, tmp_rect, editing_pos):
        draw = Draw(self.canvas)
        self.canvas.paste(self.base_img)
        for name, field in template.get_fields().items():
            rect = field.rect
            if editing_pos is not None and editing_pos[0] == rect[0] and editing_pos[1] == rect[1]:
                continue
            self._draw_rect(draw, self._transformed_rect(rect), text=name)

        if tmp_rect is not None:
            self._draw_rect(draw, self._transformed_rect(tmp_rect), color="blue")
        return self.canvas

    def resize(self, image, scale):
        mat = np.array(image)
        mat = cv2.resize(mat, None, None, scale, scale)
        return Image.fromarray(mat)

