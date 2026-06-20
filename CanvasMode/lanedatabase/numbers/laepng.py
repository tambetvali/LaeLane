# ============================
# laepng.py  (BASE GENERATOR)
# ============================

from PIL import Image
import os

class LaePNGBase:
    """
    Base class: knows ONLY
    - filename
    - folder
    - width/height
    - point list
    - saving PNG
    - saving CSV
    - drawing minimal 8-connected lines

    It does NOT know:
    - Laegna letters
    - I/O/A/E/U/V variants
    - naming rules
    """

    def __init__(self, filename, folder, width, height):
        self.filename = filename
        self.folder = folder
        self.width = width
        self.height = height
        self.points = []

        os.makedirs(folder, exist_ok=True)

    # -------------------------
    # Add a point (pixel-precise)
    # -------------------------
    def add_point(self, x, y):
        self.points.append((int(x), int(y)))

    # -------------------------
    # Minimal 8-connected Bresenham
    # -------------------------
    def _bresenham(self, x0, y0, x1, y1):
        pts = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        x, y = x0, y0

        if dx >= dy:
            err = dx // 2
            while x != x1:
                pts.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy // 2
            while y != y1:
                pts.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        pts.append((x1, y1))
        return pts

    # -------------------------
    # Draw black-on-transparent base
    # -------------------------
    def _render_base(self):
        img = Image.new("RGBA", (self.width, self.height), (0,0,0,0))
        px = img.load()

        for i in range(len(self.points)-1):
            x0, y0 = self.points[i]
            x1, y1 = self.points[i+1]
            for x, y in self._bresenham(x0, y0, x1, y1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    px[x, y] = (0,0,0,255)

        return img

    # -------------------------
    # Save PNG (single image)
    # -------------------------
    def save_png(self, outname, img):
        path = os.path.join(self.folder, outname)
        img.save(path)

    # -------------------------
    # Save CSV of points
    # -------------------------
    def save_csv(self, outname):
        path = os.path.join(self.folder, outname)
        with open(path, "w") as f:
            f.write("X,Y\n")
            for x, y in self.points:
                f.write(f"{x},{y}\n")

    # -------------------------
    # Hook for child class
    # -------------------------
    def save(self):
        """
        Child class overrides this.
        Base class does nothing.
        """
        pass



# ======================================
# laepng_client.py  (INHERITED GENERATOR)
# ======================================

from PIL import Image
import os
from laepng import LaePNGBase

class LaePNG(LaePNGBase):
    """
    Child class:
    - understands Laegna letters
    - generates I/O/A/E/U/V variants
    - uses super() for base rendering and saving
    """

    def __init__(self, filename, folder, width, height):
        super().__init__(filename, folder, width, height)

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
    # Style transforms
    # -------------------------
    def _style_I(self, base):
        return base

    def _style_E(self, base):
        w,h = base.size
        out = Image.new("RGBA", (w,h), (0,0,0,0))
        src = base.load()
        dst = out.load()
        for x in range(w):
            for y in range(h):
                r,g,b,a = src[x,y]
                if a > 0:
                    dst[x,y] = (255,255,255,255)
        return out

    def _style_O(self, base):
        w,h = base.size
        out = Image.new("RGB", (w,h), (255,255,255))
        src = base.load()
        dst = out.load()
        for x in range(w):
            for y in range(h):
                r,g,b,a = src[x,y]
                if a > 0:
                    dst[x,y] = (0,0,0)
        return out

    def _style_A(self, base):
        w,h = base.size
        out = Image.new("RGB", (w,h), (0,0,0))
        src = base.load()
        dst = out.load()
        for x in range(w):
            for y in range(h):
                r,g,b,a = src[x,y]
                if a > 0:
                    dst[x,y] = (255,255,255)
        return out

    # -------------------------
    # SAVE (main logic)
    # -------------------------
    def save(self):
        base = self._render_base()
        name = self._basename()
        first = self._first_letter()

        # 4 archetypes
        img_I = self._style_I(base)
        img_E = self._style_E(base)
        img_O = self._style_O(base)
        img_A = self._style_A(base)

        self.save_png(f"I_{name}.png", img_I)
        self.save_png(f"E_{name}.png", img_E)
        self.save_png(f"O_{name}.png", img_O)
        self.save_png(f"A_{name}.png", img_A)

        # U = copy of style matching first letter
        style_map = {"I":img_I, "E":img_E, "O":img_O, "A":img_A}
        U_img = style_map.get(first, img_I)
        self.save_png(f"U_{name}.png", U_img)

        # V = opposite letter
        opp = self._opposite(first)
        V_img = style_map.get(opp, img_I)
        self.save_png(f"V_{name}.png", V_img)

        # CSV
        self.save_csv(f"{name}.png.csv")



# ============================
# Example usage (client side)
# ============================

# from laepng_client import LaePNG
# renderer = LaePNG("AA_laesig.png", "output/", 128, 128)
# for (x,y) in [(10,10),(20,20),(30,10),(40,20)]:
#     renderer.add_point(x,y)
# renderer.save()
