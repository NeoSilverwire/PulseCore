#!/usr/bin/env python3
"""Rendert ALLE Zustaende als animierte GIFs/PNGs fuer STATES.md."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import generate as gen  # noqa: E402

from PIL import Image
import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

SIZE = 96
BG = (13, 2, 8, 255)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "states")
os.makedirs(OUT, exist_ok=True)


def render_png(svg, size):
    tmp_svg = os.path.join(OUT, "_frame.svg")
    with open(tmp_svg, "w") as f:
        f.write(svg)
    pb = GdkPixbuf.Pixbuf.new_from_file_at_size(tmp_svg, size, size)
    tmp_png = os.path.join(OUT, "_frame.png")
    pb.savev(tmp_png, "png", [], [])
    return Image.open(tmp_png).convert("RGBA")


def flatten(im):
    bg = Image.new("RGBA", im.size, BG)
    bg.alpha_composite(im)
    return bg.convert("RGB")


def save(name, cfg):
    pil_frames = [flatten(render_png(svg, SIZE)) for svg in cfg["frames"]]
    if len(pil_frames) == 1:
        pil_frames[0].save(os.path.join(OUT, f"{name}.png"), format="PNG")
        return "png"
    pil_frames[0].save(
        os.path.join(OUT, f"{name}.gif"), format="GIF", save_all=True,
        append_images=pil_frames[1:], duration=cfg["delay"], loop=0,
    )
    return "gif"


if __name__ == "__main__":
    exts = {}
    for name, cfg in gen.STATES.items():
        exts[name] = save(name, cfg)
        print("gerendert:", name, exts[name])
    for f in ("_frame.svg", "_frame.png"):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            os.remove(p)

    import json
    with open(os.path.join(OUT, "_exts.json"), "w") as f:
        json.dump(exts, f)
