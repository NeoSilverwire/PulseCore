#!/usr/bin/env python3
"""Baut das animierte 'Matrix-Circles' Xcursor-Theme (Zielmarkierungs-Kreis,
inspiriert von 'Circles v2' fuer CursorXP) aus generierten SVG-Frames."""

import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

import math
import os
import subprocess

GREEN = "#00FF41"
THEME_DIR = os.path.expanduser("~/.local/share/icons/Matrix-Circles")
BUILD_DIR = os.path.join(THEME_DIR, ".build")
SIZES = [24, 32, 48]

os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(os.path.join(THEME_DIR, "cursors"), exist_ok=True)


def render(svg, size, out_path):
    tmp_svg = out_path + ".svg"
    with open(tmp_svg, "w") as f:
        f.write(svg)
    pb = GdkPixbuf.Pixbuf.new_from_file_at_size(tmp_svg, size, size)
    pb.savev(out_path, "png", [], [])
    os.remove(tmp_svg)


def svg_wrap(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{body}</svg>'


# --- Baustein: Basis-Ring + Punkt ------------------------------------------

def base_ring(r=32, sw=4, fill_opacity=0.2):
    return (
        f'<circle cx="50" cy="50" r="{r}" fill="{GREEN}" fill-opacity="{fill_opacity}" '
        f'stroke="{GREEN}" stroke-width="{sw}"/>'
    )


def base_dot(r=4):
    return f'<circle cx="50" cy="50" r="{r}" fill="{GREEN}"/>'


# --- State: default (atmender Glow) -----------------------------------------

def frames_default(n=24):
    frames = []
    for i in range(n):
        t = i / n
        glow = 0.08 + 0.18 * (0.5 + 0.5 * math.sin(2 * math.pi * t))
        glow_r = 36 + 4 * (0.5 + 0.5 * math.sin(2 * math.pi * t))
        body = (
            f'<circle cx="50" cy="50" r="{glow_r:.2f}" fill="none" stroke="{GREEN}" '
            f'stroke-width="2" stroke-opacity="{glow:.3f}"/>'
            + base_ring() + base_dot()
        )
        frames.append(svg_wrap(body))
    return frames


# --- Baustein: Kreisbogen-Pfad ----------------------------------------------

def arc_path(cx, cy, r, start_deg, sweep_deg):
    start = math.radians(start_deg)
    end = math.radians(start_deg + sweep_deg)
    x1, y1 = cx + r * math.cos(start), cy + r * math.sin(start)
    x2, y2 = cx + r * math.cos(end), cy + r * math.sin(end)
    large_arc = 1 if sweep_deg > 180 else 0
    return f'M {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f}'


# --- State: pointer/hand (Ring in 4 Segmente geteilt, dauerhaft offen, --
# --- rotiert langsam im Uhrzeigersinn) ---------------------------------

def frames_pointer(n=36):
    frames = []
    seg_sweep = 70  # Grad pro Segment, Luecke dazwischen = 90-70=20 Grad
    for i in range(n):
        rotation = (360 / n) * i
        arcs = ""
        for seg in range(4):
            seg_start = rotation + seg * 90
            arcs += (
                f'<path d="{arc_path(50, 50, 32, seg_start, seg_sweep)}" '
                f'fill="none" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
            )
        body = (
            f'<circle cx="50" cy="50" r="32" fill="{GREEN}" fill-opacity="0.2"/>'
            + arcs + base_dot()
        )
        frames.append(svg_wrap(body))
    return frames


def frames_wait(n=16):
    frames = []
    for i in range(n):
        angle = (360 / n) * i
        body = (
            f'<circle cx="50" cy="50" r="32" fill="{GREEN}" fill-opacity="0.08" '
            f'stroke="{GREEN}" stroke-width="2" stroke-opacity="0.15"/>'
            f'<path d="{arc_path(50, 50, 32, angle, 260)}" fill="none" stroke="{GREEN}" '
            f'stroke-width="5" stroke-linecap="round"/>'
            + base_dot()
        )
        frames.append(svg_wrap(body))
    return frames


# --- State: resize (geteilter Kreis, Haelften oszillieren) -----------------

def half_disc_path(side, r=32):
    # side: "left" oder "right" Haelfte, Schnitt entlang der vertikalen Mitte (x=50)
    cx, cy = 50, 50
    if side == "left":
        return f'M {cx} {cy - r} A {r} {r} 0 0 0 {cx} {cy + r} Z'
    else:
        return f'M {cx} {cy - r} A {r} {r} 0 0 1 {cx} {cy + r} Z'


def half_dot_path(side, r=4):
    cx, cy = 50, 50
    if side == "left":
        return f'M {cx} {cy - r} A {r} {r} 0 0 0 {cx} {cy + r} Z'
    else:
        return f'M {cx} {cy - r} A {r} {r} 0 0 1 {cx} {cy + r} Z'


def frames_split(n=20, rotate_deg=0, max_offset=6):
    """Kreis entlang einer vertikalen Linie geteilt, Haelften bewegen sich
    horizontal auseinander/zueinander. Per rotate_deg auf andere Achsen
    (horizontal-Split, diagonale Splits) gedreht."""
    frames = []
    for i in range(n):
        t = i / n
        offset = max_offset * (0.5 - 0.5 * math.cos(2 * math.pi * t))
        left = (
            f'<g transform="translate({-offset:.2f},0)">'
            f'<path d="{half_disc_path("left")}" fill="{GREEN}" fill-opacity="0.2" '
            f'stroke="{GREEN}" stroke-width="4"/>'
            f'<path d="{half_dot_path("left")}" fill="{GREEN}"/>'
            f'</g>'
        )
        right = (
            f'<g transform="translate({offset:.2f},0)">'
            f'<path d="{half_disc_path("right")}" fill="{GREEN}" fill-opacity="0.2" '
            f'stroke="{GREEN}" stroke-width="4"/>'
            f'<path d="{half_dot_path("right")}" fill="{GREEN}"/>'
            f'</g>'
        )
        body = f'<g transform="rotate({rotate_deg} 50 50)">{left}{right}</g>'
        frames.append(svg_wrap(body))
    return frames


# --- State: text (blinkender I-Beam) ----------------------------------------

def _split_open_halves(rotate_deg, offset=16):
    """Kreis dauerhaft (nicht oszillierend) geoeffnet - Basis fuer den
    Text-Cursor, der treu zum 'Circles'-Thema bleibt statt ein Fremdkoerper
    zu sein."""
    left = (
        f'<g transform="translate({-offset},0)">'
        f'<path d="{half_disc_path("left")}" fill="{GREEN}" fill-opacity="0.2" '
        f'stroke="{GREEN}" stroke-width="4"/>'
        f'<path d="{half_dot_path("left")}" fill="{GREEN}"/>'
        f'</g>'
    )
    right = (
        f'<g transform="translate({offset},0)">'
        f'<path d="{half_disc_path("right")}" fill="{GREEN}" fill-opacity="0.2" '
        f'stroke="{GREEN}" stroke-width="4"/>'
        f'<path d="{half_dot_path("right")}" fill="{GREEN}"/>'
        f'</g>'
    )
    return f'<g transform="rotate({rotate_deg} 50 50)">{left}{right}</g>'


def frames_text():
    halves = _split_open_halves(rotate_deg=0)
    beam = (
        f'<line x1="50" y1="30" x2="50" y2="70" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<line x1="44" y1="30" x2="56" y2="30" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<line x1="44" y1="70" x2="56" y2="70" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
    )
    on = svg_wrap(halves + beam)
    off = svg_wrap(halves)
    return [on, off]


def frames_vertical_text():
    halves = _split_open_halves(rotate_deg=90)
    beam = (
        f'<line x1="30" y1="50" x2="70" y2="50" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<line x1="30" y1="44" x2="30" y2="56" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<line x1="70" y1="44" x2="70" y2="56" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
    )
    on = svg_wrap(halves + beam)
    off = svg_wrap(halves)
    return [on, off]


# --- State: move (vier diagonal geschnittene "Tortenstuecke" N/O/S/W, ------
# --- oszillieren entlang ihrer eigenen Achse auseinander/zusammen) ---------

def compass_point(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def wedge_path(cx, cy, r, center_deg, sweep_deg=90):
    x1, y1 = compass_point(cx, cy, r, center_deg - sweep_deg / 2)
    x2, y2 = compass_point(cx, cy, r, center_deg + sweep_deg / 2)
    large_arc = 1 if sweep_deg > 180 else 0
    return f'M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z'


def frames_move(n=20):
    frames = []
    for i in range(n):
        t = i / n
        offset = 11 * (0.5 - 0.5 * math.cos(2 * math.pi * t))
        wedges = ""
        for center_deg in (0, 90, 180, 270):
            dx, dy = compass_point(0, 0, offset, center_deg)
            wedges += (
                f'<g transform="translate({dx:.2f},{dy:.2f})">'
                f'<path d="{wedge_path(50, 50, 32, center_deg)}" fill="{GREEN}" '
                f'fill-opacity="0.2" stroke="{GREEN}" stroke-width="4" stroke-linejoin="round"/>'
                f'</g>'
            )
        body = wedges + base_dot()
        frames.append(svg_wrap(body))
    return frames


# --- State: grab (offen) - vier Ticks wandern aus den vier Himmelsrichtungen
# --- Richtung Mittelpunkt und loesen sich dort auf (Endlosschleife) --------

def frames_grab_open(n=24):
    frames = []
    r_outer, r_inner, tick_len = 44, 10, 6
    for i in range(n):
        t = i / n
        r_center = r_outer - (r_outer - r_inner) * t
        opacity = math.sin(math.pi * t)
        ticks = ""
        for ang in (0, 90, 180, 270):
            x1, y1 = compass_point(50, 50, r_center - tick_len / 2, ang)
            x2, y2 = compass_point(50, 50, r_center + tick_len / 2, ang)
            ticks += (
                f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                f'stroke="{GREEN}" stroke-width="4" stroke-linecap="round" stroke-opacity="{opacity:.3f}"/>'
            )
        body = base_ring() + ticks + base_dot()
        frames.append(svg_wrap(body))
    return frames


# --- State: grabbing (geschlossen) - Fadenkreuz steht fest zwischen Ring ---
# --- und Punkt, Ring+Fadenkreuz rotieren gemeinsam im Uhrzeigersinn --------

def frames_grabbing(n=24):
    frames = []
    cross = ""
    for ang in (0, 90, 180, 270):
        x1, y1 = compass_point(50, 50, 13, ang)
        x2, y2 = compass_point(50, 50, 30, ang)
        cross += f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
    for i in range(n):
        rotation = (360 / n) * i
        body = f'<g transform="rotate({rotation:.2f} 50 50)">{base_ring()}{cross}</g>' + base_dot()
        frames.append(svg_wrap(body))
    return frames


# --- State: not-allowed (Ring + roter Verbotsschraeg) -----------------------

def frames_not_allowed():
    body = (
        base_ring() + base_dot()
        + f'<line x1="26" y1="26" x2="74" y2="74" stroke="#FF3B3B" stroke-width="5" stroke-linecap="round"/>'
    )
    return [svg_wrap(body)]


# --- State: crosshair (Ring, Reticle-Ticks umkreisen ihn wie Monde) --------

def frames_crosshair(n=28):
    frames = []
    for i in range(n):
        rotation = (360 / n) * i
        ticks = ""
        for ang in (0, 90, 180, 270):
            a = math.radians(ang + rotation)
            x1, y1 = 50 + 34 * math.sin(a), 50 - 34 * math.cos(a)
            x2, y2 = 50 + 46 * math.sin(a), 50 - 46 * math.cos(a)
            ticks += f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{GREEN}" stroke-width="2.5"/>'
        body = base_ring(r=28) + ticks + base_dot(r=2.5)
        frames.append(svg_wrap(body))
    return frames


# --- State: zoom-in / zoom-out (Lupe mit +/-) -------------------------------

def frames_zoom(zoom_in=True):
    sign = (
        f'<line x1="38" y1="46" x2="54" y2="46" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
    )
    if zoom_in:
        sign += f'<line x1="46" y1="38" x2="46" y2="54" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
    body = (
        f'<circle cx="46" cy="46" r="22" fill="{GREEN}" fill-opacity="0.15" stroke="{GREEN}" stroke-width="4"/>'
        + sign
        + f'<line x1="62" y1="62" x2="78" y2="78" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>'
    )
    return [svg_wrap(body)]


# --- State: copy (zwei Dokumente statt Punkt, wechseln Vorder-/Hintergrund) -

def frames_copy(n=24):
    frames = []
    for i in range(n):
        t = i / n
        phase = math.sin(2 * math.pi * t)
        off = phase * 4
        doc_a = (
            f'<rect x="{43 - off:.2f}" y="{41 - off:.2f}" width="14" height="18" rx="2" '
            f'fill="#0D0208" stroke="{GREEN}" stroke-width="2.5"/>'
        )
        doc_b = (
            f'<rect x="{43 + off:.2f}" y="{41 + off:.2f}" width="14" height="18" rx="2" '
            f'fill="#0D0208" stroke="{GREEN}" stroke-width="2.5"/>'
        )
        docs = (doc_b + doc_a) if phase >= 0 else (doc_a + doc_b)
        body = base_ring() + docs
        frames.append(svg_wrap(body))
    return frames


# --- State: alias (Verknuepfungs-Pfeil statt Punkt, Marker wandert entlang -
# --- der Kurve hin und her) -------------------------------------------------

def _bezier_q(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def frames_alias(n=20):
    p0, p1, p2 = (40, 60), (40, 40), (60, 40)
    curve = (
        f'<path d="M {p0[0]} {p0[1]} Q {p1[0]} {p1[1]} {p2[0]} {p2[1]}" fill="none" '
        f'stroke="{GREEN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 52 40 L 60 40 L 60 48" fill="none" stroke="{GREEN}" '
        f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    frames = []
    for i in range(n):
        half = n // 2
        t = (i / half) if i < half else (2 - i / half)
        mx, my = _bezier_q(p0, p1, p2, t)
        marker = f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="3" fill="{GREEN}"/>'
        body = base_ring() + curve + marker
        frames.append(svg_wrap(body))
    return frames


# --- State: help (Fragezeichen statt Punkt) ---------------------------------

def frames_help():
    mark = (
        f'<path d="M 44 42 a 6 6 0 1 1 9 5.5 c -2.5 1.5 -3.5 3 -3.5 5.5" fill="none" '
        f'stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<circle cx="49.5" cy="61" r="2.5" fill="{GREEN}"/>'
    )
    body = base_ring() + mark
    return [svg_wrap(body)]


# --- State: context-menu (Hamburger-Linien statt Punkt) ---------------------

def frames_context_menu():
    lines = (
        f'<line x1="38" y1="42" x2="62" y2="42" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<line x1="38" y1="50" x2="62" y2="50" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
        f'<line x1="38" y1="58" x2="62" y2="58" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>'
    )
    body = base_ring() + lines
    return [svg_wrap(body)]


# --- Zusammenbau -------------------------------------------------------------

STATES = {
    "default": {"frames": frames_default(), "delay": 60, "hot": 0.5},
    "pointer": {"frames": frames_pointer(), "delay": 80, "hot": 0.5},
    "wait": {"frames": frames_wait(), "delay": 60, "hot": 0.5},
    "ew-resize": {"frames": frames_split(rotate_deg=0), "delay": 50, "hot": 0.5},
    "ns-resize": {"frames": frames_split(rotate_deg=90), "delay": 50, "hot": 0.5},
    "nwse-resize": {"frames": frames_split(rotate_deg=45), "delay": 50, "hot": 0.5},
    "nesw-resize": {"frames": frames_split(rotate_deg=135), "delay": 50, "hot": 0.5},
    "text": {"frames": frames_text(), "delay": 530, "hot": 0.5},
    "vertical-text": {"frames": frames_vertical_text(), "delay": 530, "hot": 0.5},
    "move": {"frames": frames_move(), "delay": 60, "hot": 0.5},
    "grab": {"frames": frames_grab_open(), "delay": 70, "hot": 0.5},
    "grabbing": {"frames": frames_grabbing(), "delay": 70, "hot": 0.5},
    "not-allowed": {"frames": frames_not_allowed(), "delay": 1000, "hot": 0.5},
    "crosshair": {"frames": frames_crosshair(), "delay": 70, "hot": 0.5},
    "zoom-in": {"frames": frames_zoom(zoom_in=True), "delay": 1000, "hot": 0.46},
    "zoom-out": {"frames": frames_zoom(zoom_in=False), "delay": 1000, "hot": 0.46},
    "copy": {"frames": frames_copy(), "delay": 80, "hot": 0.5},
    "alias": {"frames": frames_alias(), "delay": 60, "hot": 0.5},
    "help": {"frames": frames_help(), "delay": 1000, "hot": 0.5},
    "context-menu": {"frames": frames_context_menu(), "delay": 1000, "hot": 0.5},
}

ALIASES = {
    "default": ["left_ptr", "arrow", "top_left_arrow", "left_arrow"],
    "pointer": ["hand1", "hand2", "hand", "pointing_hand"],
    "wait": ["watch", "progress", "left_ptr_watch"],
    "ew-resize": ["size_hor", "sb_h_double_arrow", "h_double_arrow", "col-resize"],
    "ns-resize": ["size_ver", "sb_v_double_arrow", "v_double_arrow", "row-resize", "n-resize", "s-resize"],
    "nwse-resize": ["size_fdiag", "nw-resize", "se-resize", "top_left_corner", "bottom_right_corner"],
    "nesw-resize": ["size_bdiag", "ne-resize", "sw-resize", "top_right_corner", "bottom_left_corner"],
    "text": ["xterm", "ibeam"],
    "not-allowed": ["no-drop"],
    "crosshair": ["cell"],
}

if __name__ == "__main__":
    cursors_out = os.path.join(THEME_DIR, "cursors")

    for state, cfg in STATES.items():
        frames = cfg["frames"]
        delay = cfg["delay"]
        hot_frac = cfg["hot"]
        state_dir = os.path.join(BUILD_DIR, state)
        os.makedirs(state_dir, exist_ok=True)

        config_lines = []
        for size in SIZES:
            hot = round(size * hot_frac)
            for fi, svg in enumerate(frames):
                png_path = os.path.join(state_dir, f"{size}_{fi:03d}.png")
                render(svg, size, png_path)
                config_lines.append(f"{size} {hot} {hot} {png_path} {delay}")

        config_path = os.path.join(state_dir, "config.in")
        with open(config_path, "w") as f:
            f.write("\n".join(config_lines) + "\n")

        out_cursor = os.path.join(cursors_out, state)
        subprocess.run(["xcursorgen", config_path, out_cursor], check=True)
        print(f"gebaut: {state} ({len(frames)} Frames x {len(SIZES)} Groessen)")

        for alias in ALIASES.get(state, []):
            alias_path = os.path.join(cursors_out, alias)
            if os.path.lexists(alias_path):
                os.remove(alias_path)
            os.symlink(state, alias_path)

    print("fertig.")
