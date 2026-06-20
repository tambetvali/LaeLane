# ============================
# converter.py  (FINAL VERSION)
# ============================

import os
import json

from laepng import LaePNG
from laesvg import LaeSVG
from laejson import LaeJSON

# Script is INSIDE numbers/
R_FOLDERS = ["0.5", "1", "2", "3", "4"]

MODES = {
    "SigLae": ("Ten", "Signed"),
    "UnsigLae": ("Ten", "UnSigned"),
    "SigDec": ("Dec", "Signed"),
    "UnsigDec": ("Dec", "UnSigned")
}


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def extract_points_mode(data, axe, sign):
    """
    Extract ONLY top-level indices: "1", "2", "3", ...
    Ignore nested "1" inside "1".
    """
    pts = []
    for idx in sorted(data.keys(), key=lambda k: int(k) if k.isdigit() else 999999):
        if not idx.isdigit():
            continue
        node = data[idx]
        x = node[axe][sign]["X"]
        y = node[axe][sign]["Y"]
        pts.append((int(x), int(y)))
    return pts


# ---------------------------------------------------------
# STEP 1 — Compute boundaries for all R and all 4 modes
# ---------------------------------------------------------
def compute_boundaries():
    boundaries = {"R": {}}

    for r in R_FOLDERS:
        if not os.path.isdir(r):
            continue

        boundaries["R"][r] = {
            "Modes": {},
            "WidthSquares": None,
            "HeightSquares": None
        }

        for mode_name, (axe, sign) in MODES.items():
            all_pts = []

            for fname in os.listdir(r):
                if not fname.lower().endswith(".json"):
                    continue
                if fname.startswith("U_"):
                    continue

                data = load_json(os.path.join(r, fname))
                pts = extract_points_mode(data, axe, sign)
                all_pts.extend(pts)

            if not all_pts:
                continue

            xs = [p[0] for p in all_pts]
            ys = [p[1] for p in all_pts]

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            width = max_x - min_x
            height = max_y - min_y

            boundaries["R"][r]["Modes"][mode_name] = {
                "minX": min_x,
                "maxX": max_x,
                "minY": min_y,
                "maxY": max_y,
                "widthSquares": width,
                "heightSquares": height,
                "projection": [[1, 0], [0, 1]],
                "explanation": (
                    "Pixel index i = x - minX, j = y - minY. "
                    "SVG center = minX + 0.5 + i, minY + 0.5 + j."
                )
            }

        # global width/height for this R
        ws = []
        hs = []
        for m in boundaries["R"][r]["Modes"].values():
            ws.append(m["widthSquares"])
            hs.append(m["heightSquares"])

        if ws and hs:
            boundaries["R"][r]["WidthSquares"] = max(ws)
            boundaries["R"][r]["HeightSquares"] = max(hs)

    # WRITE boundaries.json
    with open("boundaries.json", "w") as f:
        json.dump(boundaries, f, indent=4)

    # WRITE boundaries.md
    lines = []
    lines.append("# LaeLane Boundaries\n")
    for r, rdata in boundaries["R"].items():
        lines.append(f"## R={r}\n")
        lines.append(f"- Global width: {rdata['WidthSquares']}\n")
        lines.append(f"- Global height: {rdata['HeightSquares']}\n\n")

        for mode_name, b in rdata["Modes"].items():
            lines.append(f"### Mode {mode_name}\n")
            lines.append(f"- minX: {b['minX']}")
            lines.append(f"- maxX: {b['maxX']}")
            lines.append(f"- minY: {b['minY']}")
            lines.append(f"- maxY: {b['maxY']}")
            lines.append(f"- widthSquares: {b['widthSquares']}")
            lines.append(f"- heightSquares: {b['heightSquares']}")
            lines.append(f"- projection: [[1,0],[0,1]]")
            lines.append(f"- explanation: {b['explanation']}\n")

    with open("boundaries.md", "w") as f:
        f.write("\n".join(lines))

    return boundaries


# ---------------------------------------------------------
# Coordinate transforms
# ---------------------------------------------------------
def laegna_to_pixel(x, y, b):
    return x - b["minX"], y - b["minY"]


def pixel_to_svg_center(i, j, b):
    return b["minX"] + 0.5 + i, b["minY"] + 0.5 + j


# ---------------------------------------------------------
# STEP 2 — Generate all PNG/SVG/JSON/CSV
# ---------------------------------------------------------
def generate_all(boundaries):
    gen_record = []
    readme = []

    for r in R_FOLDERS:
        if not os.path.isdir(r):
            continue

        rdata = boundaries["R"][r]
        modes_bound = rdata["Modes"]

        global_w = rdata["WidthSquares"] or 1
        global_h = rdata["HeightSquares"] or 1

        for fname in os.listdir(r):
            if not fname.lower().endswith(".json"):
                continue
            if fname.startswith("U_"):
                continue

            data = load_json(os.path.join(r, fname))

            base = os.path.splitext(fname)[0]
            num = base[1:] if base.startswith("L") else base

            readme.append(f"# {num} (R={r})\n")

            for mode_name, (axe, sign) in MODES.items():
                if mode_name not in modes_bound:
                    continue

                b = modes_bound[mode_name]
                pts_lae = extract_points_mode(data, axe, sign)
                if not pts_lae:
                    continue

                pts_pix = [laegna_to_pixel(x, y, b) for (x, y) in pts_lae]

                # ensure single point draws a dot
                if len(pts_pix) == 1:
                    pts_pix = [pts_pix[0], pts_pix[0]]

                readme.append(f"## {num} / {mode_name}\n")
                for i, (x, y) in enumerate(pts_lae, 1):
                    readme.append(f"- Laegna {i}: ({x}, {y})")
                for i, (px, py) in enumerate(pts_pix, 1):
                    readme.append(f"  - Pixel {i}: ({px}, {py})")

                suffix = {
                    "SigLae": "_st",
                    "UnsigLae": "_ut",
                    "SigDec": "_sd",
                    "UnsigDec": "_ud"
                }[mode_name]

                width = max(global_w, b["widthSquares"]) or 1
                height = max(global_h, b["heightSquares"]) or 1

                # PNG
                png_name = f"{num}{suffix}.png"
                png = LaePNG(png_name, r, width, height)
                for (px, py) in pts_pix:
                    png.add_point(px, py)
                png.save()

                # SVG
                svg_name = f"{num}{suffix}.svg"
                svg = LaeSVG(svg_name, r, width, height)
                for (px, py) in pts_pix:
                    sx, sy = pixel_to_svg_center(px, py, b)
                    svg.add_point(sx, sy)
                svg.save()

                # JSON meta
                json_name = f"{num}{suffix}.json"
                jj = LaeJSON(json_name, r, width, height)
                for (px, py) in pts_pix:
                    jj.add_point(px, py)
                jj.save()

                gen_record.append(f"{num}{suffix} generated in R={r}, mode={mode_name}")

    with open("gen_record.md", "w") as f:
        f.write("\n".join(gen_record))

    with open("README.md", "w") as f:
        f.write("\n".join(readme))


def main():
    boundaries = compute_boundaries()
    generate_all(boundaries)


if __name__ == "__main__":
    main()
