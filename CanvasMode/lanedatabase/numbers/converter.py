# ============================
# converter.py  (diagnostic, boundary-aware, L-only)
# ============================

import os
import json

from laepng import LaePNG
from laesvg import LaeSVG
from laejson import LaeJSON

# ---------------------------------
# Configuration
# ---------------------------------

# Script lives INSIDE numbers/
R_FOLDERS = ["0.5", "1", "2", "3", "4"]

# Modes: (axis, sign)
MODES = {
    "SigLae": ("Ten", "Signed"),
    "UnsigLae": ("Ten", "UnSigned"),
    "SigDec": ("Dec", "Signed"),
    "UnsigDec": ("Dec", "UnSigned"),
}

# Output suffixes per mode
MODE_SUFFIX = {
    "SigLae": "_st",
    "UnsigLae": "_ut",
    "SigDec": "_sd",
    "UnsigDec": "_ud",
}

# Logging
VERBOSE = True
LOGFILE = "converter.log"


# ---------------------------------
# Logging helpers
# ---------------------------------

def log(msg: str) -> None:
    """Write a line to converter.log and optionally print it."""
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    if VERBOSE:
        print(msg)


# Clear old log at start
with open(LOGFILE, "w", encoding="utf-8") as f:
    f.write("=== Converter run started ===\n")


# ---------------------------------
# JSON helpers
# ---------------------------------

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_points_mode(data, axe: str, sign: str):
    """
    Extract ONLY top-level numeric indices: "1", "2", "3", ...
    Ignore nested "1" inside "1".
    """
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


# ---------------------------------
# Coordinate transforms
# ---------------------------------

def laegna_to_pixel(x: int, y: int, b: dict):
    """
    Map Laegna coord (x,y) to pixel index (i,j) using boundaries.

    Boundaries (minX, maxX, minY, maxY) describe the *exteriors* of unit squares.
    Squares are [minX,minX+1), [minX+1,minX+2), ...
    Pixel index i corresponds to square [minX+i, minX+i+1).

    So:
      i = x - minX
      j = y - minY
    """
    return x - b["minX"], y - b["minY"]


def pixel_to_svg_center(i: int, j: int, b: dict):
    """
    Pixel index (i,j) -> Laegna coord of pixel center.

    Center of square k is minX + 0.5 + k.
    So:
      x_center = minX + 0.5 + i
      y_center = minY + 0.5 + j

    Examples:
      x = 1   -> center 0.5
      x = -1  -> center -0.5
      x = 100 -> center 99.5
    """
    x = b["minX"] + 0.5 + i
    y = b["minY"] + 0.5 + j
    return x, y


# ---------------------------------
# STEP 1 — Compute boundaries
# ---------------------------------

def compute_boundaries():
    """
    Scan R folders, read L-prefixed JSON files, compute boundaries per mode,
    and write boundaries.json + boundaries.md.

    Structure (Option B):

    {
      "R": {
        "0.5": {
          "Modes": {
            "SigLae": { ... },
            "UnsigLae": { ... },
            ...
          },
          "WidthSquares": ...,
          "HeightSquares": ...
        },
        "1": { ... },
        ...
      }
    }
    """
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
                # Only L-prefixed JSON files
                if not fname.startswith("L"):
                    log(f"    Skipped (not L-prefixed): {fname}")
                    continue
                if not fname.lower().endswith(".json"):
                    log(f"    Skipped (not .json): {fname}")
                    continue

                log(f"    Accepted JSON: {fname}")
                fpath = os.path.join(r, fname)

                try:
                    data = load_json(fpath)
                    log(f"      Loaded JSON OK: {fname}")
                except Exception as e:
                    log(f"      ERROR loading JSON {fname}: {e}")
                    continue

                pts = extract_points_mode(data, axe, sign)
                log(f"      Extracted {len(pts)} points from {fname}")
                all_pts.extend(pts)

            if not all_pts:
                log(f"  Mode {mode_name}: no points collected in R={r}, skipping mode")
                continue

            xs = [p[0] for p in all_pts]
            ys = [p[1] for p in all_pts]

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            # Boundaries describe exteriors of unit squares.
            # WidthSquares = maxX - minX, HeightSquares = maxY - minY
            width = max_x - min_x
            height = max_y - min_y

            log(
                f"  Boundaries for R={r}, mode={mode_name}: "
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

        # Global width/height for this R (max over modes)
        ws = []
        hs = []
        for m in boundaries["R"][r]["Modes"].values():
            ws.append(m["widthSquares"])
            hs.append(m["heightSquares"])

        if ws and hs:
            boundaries["R"][r]["WidthSquares"] = max(ws)
            boundaries["R"][r]["HeightSquares"] = max(hs)
            log(
                f"  Global R={r} widthSquares={boundaries['R'][r]['WidthSquares']}, "
                f"heightSquares={boundaries['R'][r]['HeightSquares']}"
            )
        else:
            log(f"  WARNING: R={r} has no modes with points")

    # Write boundaries.json
    with open("boundaries.json", "w", encoding="utf-8") as f:
        json.dump(boundaries, f, indent=4)
    log("Wrote boundaries.json")

    # Write boundaries.md
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


# ---------------------------------
# STEP 2 — Generate all outputs
# ---------------------------------

def generate_all(boundaries: dict):
    gen_record = []
    readme = []

    for r in R_FOLDERS:
        log(f"Generating outputs for R={r}")
        if not os.path.isdir(r):
            log(f"  WARNING: folder {r} does not exist, skipping")
            continue

        rdata = boundaries["R"].get(r)
        if not rdata:
            log(f"  WARNING: no boundaries for R={r}, skipping")
            continue

        modes_bound = rdata["Modes"]
        global_w = rdata["WidthSquares"] or 1
        global_h = rdata["HeightSquares"] or 1

        try:
            files = os.listdir(r)
        except Exception as e:
            log(f"  ERROR reading folder {r}: {e}")
            continue

        for fname in files:
            # Only L-prefixed JSON files
            if not fname.startswith("L"):
                log(f"  Skipped (not L-prefixed): {fname}")
                continue
            if not fname.lower().endswith(".json"):
                log(f"  Skipped (not .json): {fname}")
                continue

            fpath = os.path.join(r, fname)
            log(f"  Processing source JSON: {fname}")

            try:
                data = load_json(fpath)
                log(f"    Loaded JSON OK: {fname}")
            except Exception as e:
                log(f"    ERROR loading JSON {fname}: {e}")
                continue

            base = os.path.splitext(fname)[0]  # e.g. "LIE"
            num = base[1:] if base.startswith("L") else base  # "IE" or full name if needed

            readme.append(f"# {num} (R={r})\n")

            for mode_name, (axe, sign) in MODES.items():
                b = modes_bound.get(mode_name)
                if not b:
                    log(f"    No boundaries for mode={mode_name} in R={r}, skipping")
                    continue

                pts_lae = extract_points_mode(data, axe, sign)
                log(f"    Mode={mode_name} has {len(pts_lae)} Laegna points")
                if not pts_lae:
                    continue

                pts_pix = [laegna_to_pixel(x, y, b) for (x, y) in pts_lae]

                # Ensure single-point numbers draw a visible dot (duplicate point)
                if len(pts_pix) == 1:
                    pts_pix = [pts_pix[0], pts_pix[0]]
                    log("    Single-point number: duplicated point for visibility")

                readme.append(f"## {num} / {mode_name}\n")
                for i, (x, y) in enumerate(pts_lae, 1):
                    readme.append(f"- Laegna {i}: ({x}, {y})")
                for i, (px, py) in enumerate(pts_pix, 1):
                    readme.append(f"  - Pixel {i}: ({px}, {py})")

                suffix = MODE_SUFFIX[mode_name]

                # Use max of global and mode-specific width/height
                width = max(global_w, b["widthSquares"]) or 1
                height = max(global_h, b["heightSquares"]) or 1

                # ---------------- PNG ----------------
                png_name = f"{num}{suffix}.png"
                log(f"    Writing PNG: {png_name} (width={width}, height={height})")
                png = LaePNG(png_name, r, width, height)
                for (px, py) in pts_pix:
                    png.add_point(px, py)
                png.save()

                # ---------------- SVG ----------------
                # SVG canvas: width/height in squares; coordinates can be negative.
                svg_name = f"{num}{suffix}.svg"
                log(f"    Writing SVG: {svg_name} (width={width}, height={height})")
                svg = LaeSVG(svg_name, r, width, height)
                for (px, py) in pts_pix:
                    sx, sy = pixel_to_svg_center(px, py, b)
                    svg.add_point(sx, sy)
                svg.save()

                # ---------------- JSON meta ----------------
                json_name = f"{num}{suffix}.json"
                log(f"    Writing JSON meta: {json_name} (width={width}, height={height})")
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


# ---------------------------------
# Main
# ---------------------------------

def main():
    boundaries = compute_boundaries()
    generate_all(boundaries)
    log("=== Converter run finished ===")


if __name__ == "__main__":
    main()
