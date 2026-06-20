# ============================
# converter.py  (CO-GENERATOR)
# ============================

import os
import json

from laepng import LaePNG
from laesvg import LaeSVG
from laejson import LaeJSON


R_FOLDERS = ["0.5", "1", "2", "3", "4"]


def load_laejson(path):
    with open(path, "r") as f:
        return json.load(f)


def extract_points(data, fmt):
    """
    fmt: one of "st", "ut", "sd", "ud"
    st = Signed Ten
    ut = UnSigned Ten
    sd = Signed Dec
    ud = UnSigned Dec

    Returns list of (x, y) in index order: "1", "2", ...
    """
    points = []
    for idx in sorted(data.keys(), key=lambda k: int(k)):
        if not idx.isdigit():
            continue
        node = data[idx]
        if fmt == "st":
            x = node["Ten"]["Signed"]["X"]
            y = node["Ten"]["Signed"]["Y"]
        elif fmt == "ut":
            x = node["Ten"]["UnSigned"]["X"]
            y = node["Ten"]["UnSigned"]["Y"]
        elif fmt == "sd":
            x = node["Dec"]["Signed"]["X"]
            y = node["Dec"]["Signed"]["Y"]
        elif fmt == "ud":
            x = node["Dec"]["UnSigned"]["X"]
            y = node["Dec"]["UnSigned"]["Y"]
        else:
            raise ValueError(f"Unknown format: {fmt}")
        points.append((int(x), int(y)))
    return points


def bounding_box(all_points):
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    return min(xs), max(xs), min(ys), max(ys)


def pixel_to_svg_coord(x, y):
    # pixel (n, m) -> center of pixel: (n-0.5, m-0.5)
    return x - 0.5, y - 0.5


def process_file(r_folder, json_file, gen_record_lines, readme_lines):
    folder = r_folder
    path = os.path.join(folder, json_file)
    data = load_laejson(path)

    # base name: remove leading "L" and ".json" (case-insensitive)
    base = os.path.splitext(json_file)[0]
    if base.startswith("L"):
        num = base[1:]
    else:
        num = base

    # formats
    formats = ["st", "ut", "sd", "ud"]

    # collect all points for bounding box
    all_points_for_R = []

    # README chapter for this number
    readme_lines.append(f"# {num}\n")

    for fmt in formats:
        suffix = f"_{fmt}"
        points = extract_points(data, fmt)
        all_points_for_R.extend(points)

        # record points in README
        readme_lines.append(f"## {num}{suffix}\n")
        for i, (x, y) in enumerate(points, start=1):
            readme_lines.append(f"- Point {i}: ({x}, {y})\n")

        # PNG
        png_name = f"{num}{suffix}.png"
        png_renderer = LaePNG(png_name, folder, 256, 256)
        for x, y in points:
            png_renderer.add_point(x, y)
        png_renderer.save()

        # SVG
        svg_name = f"{num}{suffix}.svg"
        svg_renderer = LaeSVG(svg_name, folder, 256, 256)
        for x, y in points:
            # convert to SVG center coordinates
            sx, sy = pixel_to_svg_coord(x, y)
            svg_renderer.add_point(sx, sy)
        svg_renderer.save()

        # JSON meta
        json_name = f"{num}{suffix}.json"
        json_renderer = LaeJSON(json_name, folder, 256, 256)
        for x, y in points:
            json_renderer.add_point(x, y)
        json_renderer.save()

        # gen_record entry
        gen_record_lines.append(f"## {num}{suffix}\n")
        gen_record_lines.append(f"- Points: {len(points)}\n")
        gen_record_lines.append(f"- PNG/SVG/JSON/CSV generated for {fmt}\n")

    # bounding box for this R-folder (number range)
    if all_points_for_R:
        min_x, max_x, min_y, max_y = bounding_box(all_points_for_R)
        gen_record_lines.append(f"# R={r_folder}, Number={num}\n")
        gen_record_lines.append(f"- Bounding box X: {min_x} .. {max_x}\n")
        gen_record_lines.append(f"- Bounding box Y: {min_y} .. {max_y}\n")

        # pixel and SVG coords
        sx_min, sy_min = pixel_to_svg_coord(min_x, min_y)
        sx_max, sy_max = pixel_to_svg_coord(max_x, max_y)
        gen_record_lines.append(f"- SVG box approx: ({sx_min}, {sy_min}) .. ({sx_max}, {sy_max})\n")


def main():
    gen_record_lines = []
    readme_lines = []

    for r in R_FOLDERS:
        if not os.path.isdir(r):
            continue

        for fname in os.listdir(r):
            if not fname.lower().endswith(".json"):
                continue
            if fname.startswith("U_"):
                continue  # skip already-generated U_ variants

            process_file(r, fname, gen_record_lines, readme_lines)

    # write gen_record.md
    with open("gen_record.md", "w") as f:
        f.write("\n".join(gen_record_lines))

    # write README.md
    with open("README.md", "w") as f:
        f.write("\n".join(readme_lines))


if __name__ == "__main__":
    main()
