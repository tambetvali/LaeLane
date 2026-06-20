# ============================
# laejson.py  (JSON DRIVER)
# ============================

import os
import json

class LaeJSON:
    """
    Stand-alone JSON generator.
    Same external interface as PNG and SVG generators:
        - __init__(filename, folder, width, height)
        - add_point(x, y)
        - save()

    JSON contains:
        {
            "width": ...,
            "height": ...,
            "points": [[x,y], ...],
            "csv": "X,Y\n0,0\n128,-74\n...",
            "svg": {
                "I": "<svg ...>",
                "E": "<svg ...>",
                "O": "<svg ...>",
                "A": "<svg ...>",
                "U": "<svg ...>",
                "V": "<svg ...>"
            },
            "files": {
                "png": {
                    "I": "I_name.png",
                    "E": "E_name.png",
                    "O": "O_name.png",
                    "A": "A_name.png",
                    "U": "U_name.png",
                    "V": "V_name.png"
                },
                "svg": {
                    "I": "I_name.svg",
                    "E": "E_name.svg",
                    "O": "O_name.svg",
                    "A": "A_name.svg",
                    "U": "U_name.svg",
                    "V": "V_name.svg"
                },
                "csv": "name.csv"
            }
        }

    No inheritance. Pure JSON + SVG + CSV.
    """

    def __init__(self, filename, folder, width, height):
        self.filename = filename
        self.folder = folder
        self.width = width
        self.height = height
        self.points = []

        os.makedirs(folder, exist_ok=True)

    # -------------------------
    # Add pixel-precise point
    # -------------------------
    def add_point(self, x, y):
        self.points.append((int(x), int(y)))

    # -------------------------
    # Helpers
    # -------------------------
    def _basename(self):
        base = os.path.basename(self.filename)
        if base.lower().endswith(".json"):
            base = base[:-5]
        return base

    def _first_letter(self):
        return self._basename()[0]

    def _opposite(self, L):
        return {"A":"O", "O":"A", "E":"I", "I":"E"}.get(L, L)

    # -------------------------
    # SVG template (same as laesvg)
    # -------------------------
    def _svg_template(self, stroke_color, bg_color):
        pts = " ".join(f"{x},{y}" for x, y in self.points)

        if bg_color is None:
            bg = ""
        else:
            bg = f'<rect width="{self.width}" height="{self.height}" fill="{bg_color}" />'

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="{self.width}" height="{self.height}"
     viewBox="0 0 {self.width} {self.height}">
{bg}
<polyline points="{pts}"
    fill="none"
    stroke="{stroke_color}"
    stroke-width="1"
    stroke-linejoin="miter"
    stroke-linecap="butt" />
</svg>'''
        return svg

    # -------------------------
    # CSV multiline string
    # -------------------------
    def _csv_string(self):
        lines = ["X,Y"]
        for x, y in self.points:
            lines.append(f"{x},{y}")
        return "\n".join(lines)

    # -------------------------
    # Main save()
    # -------------------------
    def save(self):
        name = self._basename()
        first = self._first_letter()

        # 4 archetypes
        svg_I = self._svg_template("#000000", None)        # black on transparent
        svg_E = self._svg_template("#FFFFFF", None)        # white on transparent
        svg_O = self._svg_template("#000000", "#FFFFFF")   # black on white
        svg_A = self._svg_template("#FFFFFF", "#000000")   # white on black

        # U = copy of style matching first letter
        style_map = {
            "I": svg_I,
            "E": svg_E,
            "O": svg_O,
            "A": svg_A
        }
        svg_U = style_map.get(first, svg_I)

        # V = opposite letter
        opp = self._opposite(first)
        svg_V = style_map.get(opp, svg_I)

        # CSV
        csv_text = self._csv_string()

        # Filenames (PNG + SVG + CSV)
        png_files = {
            "I": f"I_{name}.png",
            "E": f"E_{name}.png",
            "O": f"O_{name}.png",
            "A": f"A_{name}.png",
            "U": f"U_{name}.png",
            "V": f"V_{name}.png"
        }

        svg_files = {
            "I": f"I_{name}.svg",
            "E": f"E_{name}.svg",
            "O": f"O_{name}.svg",
            "A": f"A_{name}.svg",
            "U": f"U_{name}.svg",
            "V": f"V_{name}.svg"
        }

        csv_file = f"{name}.csv"

        # JSON structure
        data = {
            "width": self.width,
            "height": self.height,
            "points": [[x, y] for x, y in self.points],
            "csv": csv_text,
            "svg": {
                "I": svg_I,
                "E": svg_E,
                "O": svg_O,
                "A": svg_A,
                "U": svg_U,
                "V": svg_V
            },
            "files": {
                "png": png_files,
                "svg": svg_files,
                "csv": csv_file
            }
        }

        # Save JSON
        outpath = os.path.join(self.folder, f"{name}.json")
        with open(outpath, "w") as f:
            json.dump(data, f, indent=4)



# ============================
# Example usage
# ============================

# from laejson import LaeJSON
# renderer = LaeJSON("AE.json", "output/", 128, 128)
# for (x,y) in [(0,0),(128,-74),(64,32)]:
#     renderer.add_point(x,y)
# renderer.save()
