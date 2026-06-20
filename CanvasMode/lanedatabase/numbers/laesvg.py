# laesvg.py

import os
from xml.etree.ElementTree import Element, SubElement, ElementTree


class LaeSVG:
    def __init__(self, filename: str, r: str, width: int, height: int):
        self.r = r
        self.filename = filename
        self.width = int(width)
        self.height = int(height)
        self.points = []  # list of (x_center, y_center) in Laegna coords

    def add_point(self, x_center: float, y_center: float):
        self.points.append((float(x_center), float(y_center)))

    def save(self):
        out_dir = self.r
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, self.filename)

        svg = Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "version": "1.1",
                "viewBox": f"0 0 {self.width} {self.height}",
            },
        )

        # Map Laegna centers to SVG coordinates:
        # For simplicity, we map them into [0,width]x[0,height] by shifting
        # relative to min center; converter already ensured tight bounds.
        # Here we just draw circles at normalized positions.

        if self.points:
            xs = [p[0] for p in self.points]
            ys = [p[1] for p in self.points]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            span_x = max(max_x - min_x, 1e-9)
            span_y = max(max_y - min_y, 1e-9)

            def norm(px, py):
                nx = (px - min_x) / span_x * (self.width - 1)
                ny = (py - min_y) / span_y * (self.height - 1)
                return nx, self.height - 1 - ny

            # Draw lines connecting points in order
            if len(self.points) >= 2:
                d = []
                for idx, (px, py) in enumerate(self.points):
                    sx, sy = norm(px, py)
                    cmd = "M" if idx == 0 else "L"
                    d.append(f"{cmd} {sx} {sy}")
                path_el = SubElement(
                    svg,
                    "path",
                    {
                        "d": " ".join(d),
                        "stroke": "black",
                        "fill": "none",
                        "stroke-width": "0.1",
                    },
                )

            # Draw dots for each point
            for (px, py) in self.points:
                sx, sy = norm(px, py)
                SubElement(
                    svg,
                    "circle",
                    {
                        "cx": str(sx),
                        "cy": str(sy),
                        "r": "0.2",
                        "fill": "black",
                    },
                )

        tree = ElementTree(svg)
        tree.write(path, encoding="utf-8", xml_declaration=True)
