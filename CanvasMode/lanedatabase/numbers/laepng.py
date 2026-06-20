import os
from PIL import Image


class LaePNG:
    def __init__(self, filename: str, r: str, width: int, height: int):
        self.r = r
        self.filename = filename
        self.width = int(width)      # pixels, 1 px = 1 Laegna unit
        self.height = int(height)

        self.img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.px = self.img.load()

    def add_point(self, i: int, j: int):
        x = int(i)
        y = int(j)
        if 0 <= x < self.width and 0 <= y < self.height:
            # y=0 at bottom in Laegna; invert for image
            self.px[x, self.height - 1 - y] = (0, 0, 0)

    def save(self):
        os.makedirs(self.r, exist_ok=True)
        path = os.path.join(self.r, self.filename)
        # 1 px = 1 cm → 2.54 dpi
        self.img.save(path, dpi=(2.54, 2.54))
