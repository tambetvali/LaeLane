import os
from xml.etree.ElementTree import Element, SubElement, ElementTree


class LaeSVG:
    def __init__(self, filename: str, r: str, width: int, height: int, min_x: int, min_y: int):
        self.r = r
        self.filename = filename
        self.width = int(width)      # Laegna units
        self.height = int(height)    # Laegna units
        self.min_x = int(min_x)
        self.min_y = int(min_y)
        self.points = []  # (x_center, y_center) in Laegna coords

    def add_point(self, x_center: float, y_center: float):
        self.points.append((float(x_center), float(y_center)))

    def save(self):
        os.makedirs(self.r, exist_ok=True)
        path = os.path.join(self.r, self.filename)

        # 1 Laegna unit = 1 cm
        svg = Element(
            "svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "version": "1.1",
                "width": f"{self.width}cm",
                "height": f"{self.height}cm",
                "viewBox": f"{self.min_x} {self.min_y} {self.width} {self.height}",
            },
        )

        if self.points:
            # Lines between centers (if ≥2)
            if len(self.points) >= 2:
                d = []
                for idx, (x, y) in enumerate(self.points):
                    cmd = "M" if idx == 0 else "L"
                    d.append(f"{cmd} {x} {y}")
                SubElement(
                    svg,
                    "path",
                    {
                        "d": " ".join(d),
                        "stroke": "black",
                        "fill": "none",
                        "stroke-width": "0.05",  # 0.05 cm
                    },
                )

            # Dots at centers
            for (x, y) in self.points:
                SubElement(
                    svg,
                    "circle",
                    {
                        "cx": str(x),
                        "cy": str(y),
                        "r": "0.25",  # 0.25 cm radius
                        "fill": "black",
                    },
                )

        tree = ElementTree(svg)
        tree.write(path, encoding="utf-8", xml_declaration=True)
