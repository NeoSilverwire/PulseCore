# All States

Full gallery of every state PulseCore ships with its own design for.
Everything not listed here falls back to whatever cursor theme you had
before, via `Inherits=` in `index.theme`.

## Basics

| State | Animation |
|---|---|
| `default` (+ `left_ptr`, `arrow`, `top_left_arrow`, `left_arrow`) | ![default](preview/states/default.gif) |
| `pointer` — link hover (+ `hand1`, `hand2`, `hand`, `pointing_hand`) | ![pointer](preview/states/pointer.gif) |
| `wait` — busy (+ `watch`, `progress`, `left_ptr_watch`) | ![wait](preview/states/wait.gif) |
| `text` — text field (+ `xterm`, `ibeam`) | ![text](preview/states/text.gif) |
| `vertical-text` | ![vertical-text](preview/states/vertical-text.gif) |

## Window edges (resize)

| State | Animation |
|---|---|
| `ew-resize` — width (+ `size_hor`, `sb_h_double_arrow`, `h_double_arrow`, `col-resize`) | ![ew-resize](preview/states/ew-resize.gif) |
| `ns-resize` — height (+ `size_ver`, `sb_v_double_arrow`, `v_double_arrow`, `row-resize`, `n-resize`, `s-resize`) | ![ns-resize](preview/states/ns-resize.gif) |
| `nwse-resize` — corner ↖ ↘ (+ `size_fdiag`, `nw-resize`, `se-resize`, `top_left_corner`, `bottom_right_corner`) | ![nwse-resize](preview/states/nwse-resize.gif) |
| `nesw-resize` — corner ↗ ↙ (+ `size_bdiag`, `ne-resize`, `sw-resize`, `top_right_corner`, `bottom_left_corner`) | ![nesw-resize](preview/states/nesw-resize.gif) |

## Move & drag

| State | Animation |
|---|---|
| `move` | ![move](preview/states/move.gif) |
| `grab` | ![grab](preview/states/grab.gif) |
| `grabbing` | ![grabbing](preview/states/grabbing.gif) |
| `not-allowed` (+ `no-drop`) | ![not-allowed](preview/states/not-allowed.png) |

## Other

| State | Animation |
|---|---|
| `crosshair` (+ `cell`) | ![crosshair](preview/states/crosshair.gif) |
| `zoom-in` | ![zoom-in](preview/states/zoom-in.png) |
| `zoom-out` | ![zoom-out](preview/states/zoom-out.png) |
| `copy` | ![copy](preview/states/copy.gif) |
| `alias` | ![alias](preview/states/alias.gif) |
| `help` | ![help](preview/states/help.png) |
| `context-menu` | ![context-menu](preview/states/context-menu.png) |

---

Generated with `preview/build_all_states.py` (renders every `frames_*()`
function in `generate.py` at 96px instead of the Xcursor target sizes, for
a crisper README preview).
