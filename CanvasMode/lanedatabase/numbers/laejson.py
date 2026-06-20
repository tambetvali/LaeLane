# laejson.py

import os
import json


class LaeJSON:
    def __init__(self, filename: str, r: str, width: int, height: int):
        self.r = r
        self.filename = filename
        self.width = int(width)
        self.height = int(height)
        self.points = []  # list of (i, j)

    def add_point(self, i: int, j: int):
        self.points.append((int(i), int(j)))

    def save(self):
        out_dir = self.r
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, self.filename)

        data = {
            "R": self.r,
            "WidthSquares": self.width,
            "HeightSquares": self.height,
            "Points": [
                {"i": i, "j": j}
                for (i, j) in self.points
            ],
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
