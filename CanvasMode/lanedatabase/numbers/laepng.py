# laepng.py

import os
from PIL import Image  # Pillow


class LaePNG:
    def __init__(self, filename: str, r: str, width: int, height: int):
        self.r = r
        self.filename = filename
        self.width = int(width)
        self.height = int(height)

        # White background, black foreground
        self.img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.px = self.img.load()

    def add_point(self, i: int, j: int):
        x = int(i)
        y = int(j)
        if 0 <= x < self.width and 0 <= y < self.height:
            # Note: y axis direction depends on your convention.
            self.px[x, self.height - 1 - y] = (0, 0, 0)

    def save(self):
        out_dir = self.r
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, self.filename)
        self.img.save(path)
