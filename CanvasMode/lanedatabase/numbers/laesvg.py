# ============================
# laesvg.py  (SVG GENERATOR)
# ============================

import os

class LaeSVG:
    """
    Stand-alone SVG generator.
    Same interface as PNG generator:
        - __init__(filename, folder, width, height)
        - add_point(x, y)
        - save()

    Produces:
        I_name.svg  (black line, transparent bg)
        E_name.svg  (white line, transparent bg)
        O_name.svg  (black line, white bg)
        A_name.svg  (white line, black bg)
        U_name.svg  (copy of style matching first letter)
        V_name.svg  (copy of opposite letter style)
        name.svg.csv (point list)

    Pixel-precision integer coordinates.
    No smoothing, no AA (SVG uses straight segments).
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
        return os.path.splitext(os.path.basename(self.filename))[0]

    def _first_letter(self):
        return self._basename()[0]

    def _opposite(self, L):
        return {"A":"O", "O":"A", "E":"I", "I":"E"}.get(L, L)

    # -------------------------
    # SVG template generator
    # -------------------------
    def _svg_template(self, stroke_color, bg_color):
        """
        stroke_color: "#000000" or "#FFFFFF"
        bg_color: None (transparent) or "#000000"/"#FFFFFF"
        """

        # Build polyline points
        pts = " ".join(f"{x},{y}" for x, y in self.points)

        # Background rect if needed
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
    # Save SVG
    # -------------------------
    def _save_svg(self, outname, svg_text):
        path = os.path.join(self.folder, outname)
        with open(path, "w") as f:
            f.write(svg_text)

    # -------------------------
    # Save CSV
    # -------------------------
    def _save_csv(self, outname):
        path = os.path.join(self.folder, outname)
        with open(path, "w") as f:
            f.write("X,Y\n")
            for x, y in self.points:
                f.write(f"{x},{y}\n")

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

        self._save_svg(f"I_{name}.svg", svg_I)
        self._save_svg(f"E_{name}.svg", svg_E)
        self._save_svg(f"O_{name}.svg", svg_O)
        self._save_svg(f"A_{name}.svg", svg_A)

        # U = copy of style matching first letter
        style_map = {
            "I": svg_I,
            "E": svg_E,
            "O": svg_O,
            "A": svg_A
        }
        U_svg = style_map.get(first, svg_I)
        self._save_svg(f"U_{name}.svg", U_svg)

        # V = opposite letter
        opp = self._opposite(first)
        V_svg = style_map.get(opp, svg_I)
        self._save_svg(f"V_{name}.svg", V_svg)

        # CSV
        self._save_csv(f"{name}.svg.csv")



# ============================
# Example usage
# ============================

# from laesvg import LaeSVG
# renderer = LaeSVG("AA_laesig.svg", "output/", 128, 128)
# for (x,y) in [(10,10),(20,20),(30,10),(40,20)]:
#     renderer.add_point(x,y)
# renderer.save()
