# PulseCore

A fully animated Xcursor theme built around a single idea: every cursor is
a **reticle** — a thin glowing ring with a center dot, like a target
marker in a game HUD. Each of the 20 covered states gets its own
purpose-built animation on top of that shared shape, instead of just
swapping colors on a stock icon set.

Inspired by the look and feel of **"Circles v2"**, an old cursor pack for
Stardock's CursorXP/CursorFX (Windows, mid-2000s) that is no longer
available anywhere online. This is not a port or a re-upload of that pack
— it's a from-scratch reimplementation based on a description of what it
looked like, built for modern Linux/Xcursor instead.

![Default](preview/default.gif)
![Link hover](preview/pointer.gif)
![Resize](preview/ew-resize.gif)
![Grab](preview/grab.gif)
![Crosshair](preview/crosshair.gif)
![Copy](preview/copy.gif)

## What's animated

20 states are custom-built; everything else falls back to your existing
cursor theme via `Inherits=` in `index.theme`.

| State | Behavior |
|---|---|
| `default` | Ring + dot, gently breathing outer glow |
| `pointer` (link hover) | Ring splits into 4 arcs, permanently open, slowly rotating clockwise |
| `wait` / `progress` | Dimmed ring track + a rotating 260° arc (classic spinner) |
| `text` / `vertical-text` | Ring opens permanently, a blinking I-beam sits in the gap |
| `ew-resize` / `ns-resize` | Ring splits in half, halves oscillate apart/together along that axis |
| `nwse-resize` / `nesw-resize` | Same, split along the diagonal |
| `move` | Ring cut into 4 diagonal pie slices, each oscillates outward along its own axis |
| `grab` | 4 ticks travel inward from the 4 compass points and fade into the center dot, on loop |
| `grabbing` | A fixed crosshair between ring and dot, ring+crosshair rotate together |
| `not-allowed` / `no-drop` | Ring + dot with a red diagonal slash |
| `crosshair` / `cell` | 4 reticle ticks orbit the ring like moons |
| `zoom-in` / `zoom-out` | Magnifying glass with a centered +/− |
| `copy` | Two overlapping document shapes swap foreground/background continuously |
| `alias` | A curved link arrow with a marker pulsing back and forth along it |
| `help` | Enlarged question mark, centered |
| `context-menu` | Enlarged hamburger lines, centered |

All built on a `viewBox="0 0 100 100"` canvas, rendered at 24/32/48px.

## Installation

### 1. Copy the theme

```bash
mkdir -p ~/.local/share/icons/PulseCore
cp -r cursors cursor.theme index.theme ~/.local/share/icons/PulseCore/
```

(For a system-wide install instead, use `/usr/share/icons/PulseCore` with
`sudo`.)

### 2. Activate it

**KDE Plasma**

```bash
plasma-apply-cursortheme PulseCore
```

Or: System Settings → Appearance → Cursors → select "PulseCore".

**GNOME**

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'PulseCore'
```

Or: GNOME Tweaks → Appearance → Cursor.

**Other X11 desktops / window managers**

```bash
mkdir -p ~/.icons/default
cat > ~/.icons/default/index.theme <<'EOF'
[Icon Theme]
Inherits=PulseCore
EOF
```

Then log out and back in (or restart your session) so apps that read the
cursor theme once at startup pick it up.

**GTK apps specifically** (if they don't follow your DE's setting)

In `~/.config/gtk-3.0/settings.ini` and `~/.config/gtk-4.0/settings.ini`:

```ini
[Settings]
gtk-cursor-theme-name=PulseCore
```

## Customizing / rebuilding

The whole theme is generated from Python, not hand-drawn frame by frame.
`generate.py` builds every SVG frame, rasterizes it, and compiles it with
`xcursorgen`.

Requirements:

```bash
# Fedora
sudo dnf install xcursorgen python3-gobject gdk-pixbuf2

# Debian/Ubuntu
sudo apt install xcursorgen python3-gi gir1.2-gdkpixbuf-2.0
```

Then, from the repo root:

```bash
python3 generate.py
```

This regenerates everything under `cursors/`. Open `generate.py` and tweak
constants (`GREEN`, frame counts, delays, offsets) or the per-state
`frames_*()` functions to change the look or timing of any state.

**Note on live-reloading while testing:** some desktop environments cache
the active cursor theme and won't notice a rebuild of the same theme name.
On KDE, the reliable way to force a reload is to switch to a different
theme and back:

```bash
plasma-apply-cursortheme Breeze
plasma-apply-cursortheme PulseCore
```

## License

CC0 1.0 — public domain. See [LICENSE](LICENSE). Do whatever you want
with it.
