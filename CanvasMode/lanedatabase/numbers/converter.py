# converter.py

import os
import json

from laepng import LaePNG
from laesvg import LaeSVG
from laejson import LaeJSON

R_FOLDERS = ["0.5", "1", "2", "3", "4"]

MODES = {
    "SigLae": ("Ten", "Signed"),
    "UnsigLae": ("Ten", "UnSigned"),
    "SigDec": ("Dec", "Signed"),
    "UnsigDec": ("Dec", "UnSigned"),
}

MODE_SUFFIX = {
    "SigLae": "_st",
    "UnsigLae": "_ut",
    "SigDec": "_sd",
    "UnsigDec": "_ud",
}

VERBOSE = True
LOGFILE = "converter.log"


def log(msg: str) -> None:
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    if VERBOSE:
        print(msg)


with open(LOGFILE, "w", encoding="utf-8") as f:
    f.write("=== Converter run started ===\n")


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_points_mode(data, axe: str, sign: str):
    pts = []
    keys = sorted(
        [k for k in data.keys() if k.isdigit()],
        key=lambda k: int(k)
    )
    for idx in keys:
        node = data[idx]
        try:
            x = node[axe][sign]["X"]
            y = node[axe][sign]["Y"]
        except KeyError as e:
            log(f"      WARNING: missing key {e} in index {idx}")
            continue
        pts.append((int(x), int(y)))
    return pts


def laegna_to_pixel(x: int, y: int, b: dict):
    return x - b["minX"], y - b["minY"]


def pixel_to_svg_center(i: int, j: int, b: dict):
    x = b["minX"] + 0.5 + i
    y = b["minY"] + 0.5 + j
    return x, y


def compute_boundaries():
    boundaries = {"R": {}}

    for r in R_FOLDERS:
        log(f"Scanning R folder: {r}")
        if not os.path.isdir(r):
            log(f"  WARNING: folder {r} does not exist, skipping")
            continue

        try:
            files = os.listdir(r)
        except Exception as e:
            log(f"  ERROR reading folder {r}: {e}")
            continue

        log(f"  Files found: {files}")

        boundaries["R"][r] = {
            "Modes": {},
            "WidthSquares": None,
            "HeightSquares": None,
        }

        for mode_name, (axe, sign) in MODES.items():
            log(f"  Mode: {mode_name} (axe={axe}, sign={sign})")
            all_pts = []

            for fname in files:
                if not fname.startswith("L"):
                    continue
                if not fname.lower().endswith(".json"):
                    continue

                fpath = os.path.join(r, fname)
                try:
                    data = load_json(fpath)
                except Exception as e:
                    log(f"      ERROR loading JSON {fname}: {e}")
                    continue

                pts = extract_points_mode(data, axe, sign)
                all_pts.extend(pts)

            if not all_pts:
                log(f"  Mode {mode_name}: no points in R={r}, skipping")
                continue

            xs = [p[0] for p in all_pts]
            ys = [p[1] for p in all_pts]

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            width = max_x - min_x or 1
            height = max_y - min_y or 1

            log(
                f"  Boundaries R={r}, mode={mode_name}: "
                f"minX={min_x}, maxX={max_x}, minY={min_y}, maxY={max_y}, "
                f"widthSquares={width}, heightSquares={height}"
            )

            boundaries["R"][r]["Modes"][mode_name] = {
                "minX": min_x,
                "maxX": max_x,
                "minY": min_y,
                "maxY": max_y,
                "widthSquares": width,
                "heightSquares": height,
                "projection": [[1, 0], [0, 1]],
                "explanation": (
                    "Boundaries describe exteriors of unit squares. "
                    "Pixel index i = x - minX, j = y - minY. "
                    "SVG center = minX + 0.5 + i, minY + 0.5 + j."
                ),
            }

        ws = []
        hs = []
        for m in boundaries["R"][r]["Modes"].values():
            ws.append(m["widthSquares"])
            hs.append(m["heightSquares"])

        if ws and hs:
            boundaries["R"][r]["WidthSquares"] = max(ws)
            boundaries["R"][r]["HeightSquares"] = max(hs)
        else:
            log(f"  WARNING: R={r} has no modes with points")

    with open("boundaries.json", "w", encoding="utf-8") as f:
        json.dump(boundaries, f, indent=4)
    log("Wrote boundaries.json")

    lines = []
    lines.append("# LaeLane Boundaries\n")
    for r, rdata in boundaries["R"].items():
        lines.append(f"## R={r}\n")
        lines.append(f"- Global width (squares): {rdata['WidthSquares']}")
        lines.append(f"- Global height (squares): {rdata['HeightSquares']}\n")
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

    with open("boundaries.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log("Wrote boundaries.md")

    return boundaries


def generate_all(boundaries: dict):
    gen_record = []
    readme = []

    for r in R_FOLDERS:
        log(f"Generating outputs for R={r}")
        if not os.path.isdir(r):
            continue

        rdata = boundaries["R"].get(r)
        if not rdata:
            continue

        modes_bound = rdata["Modes"]

        try:
            files = os.listdir(r)
        except Exception as e:
            log(f"  ERROR reading folder {r}: {e}")
            continue

        for fname in files:
            if not fname.startswith("L"):
                continue
            if not fname.lower().endswith(".json"):
                continue

            fpath = os.path.join(r, fname)
            try:
                data = load_json(fpath)
            except Exception as e:
                log(f"    ERROR loading JSON {fname}: {e}")
                continue

            base = os.path.splitext(fname)[0]
            num = base[1:] if base.startswith("L") else base

            readme.append(f"# {num} (R={r})\n")

            for mode_name, (axe, sign) in MODES.items():
                b = modes_bound.get(mode_name)
                if not b:
                    continue

                pts_lae = extract_points_mode(data, axe, sign)
                if not pts_lae:
                    continue

                pts_pix = [laegna_to_pixel(x, y, b) for (x, y) in pts_lae]

                if len(pts_pix) == 1:
                    log(f"    {num} R={r} mode={mode_name}: single-point dot")

                readme.append(f"## {num} / {mode_name}\n")
                for i, (x, y) in enumerate(pts_lae, 1):
                    readme.append(f"- Laegna {i}: ({x}, {y})")
                for i, (px, py) in enumerate(pts_pix, 1):
                    readme.append(f"  - Pixel {i}: ({px}, {py})")

                suffix = MODE_SUFFIX[mode_name]
                width = b["widthSquares"] or 1
                height = b["heightSquares"] or 1

                png_name = f"{num}{suffix}.png"
                png = LaePNG(png_name, r, width, height)
                for (px, py) in pts_pix:
                    png.add_point(px, py)
                png.save()

                svg_name = f"{num}{suffix}.svg"
                svg = LaeSVG(svg_name, r, width, height)
                for (px, py) in pts_pix:
                    sx, sy = pixel_to_svg_center(px, py, b)
                    svg.add_point(sx, sy)
                svg.save()

                json_name = f"{num}{suffix}.json"
                jj = LaeJSON(json_name, r, width, height)
                for (px, py) in pts_pix:
                    jj.add_point(px, py)
                jj.save()

                gen_record.append(
                    f"{num}{suffix} generated in R={r}, mode={mode_name}, "
                    f"width={width}, height={height}"
                )

    with open("gen_record.md", "w", encoding="utf-8") as f:
        f.write("\n".join(gen_record))
    log("Wrote gen_record.md")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme))
    log("Wrote README.md")


def main():
    boundaries = compute_boundaries()
    generate_all(boundaries)
    log("=== Converter run finished ===")


if __name__ == "__main__":
    main()
