"""The master logo + watermark set.

One official lockup: the Signal C over/beside the wordmark. Everything else in
the collection is a derivative of this file.
"""
import os, math
import typeset as ts
from build import (INK, CREAM, ACCENT, ACCENT_DEEP, MUTED, MUTED_DEEP,
                   signal, wordmark, svg, NAME, HANDLE)

OUT = "out"
os.makedirs(OUT, exist_ok=True)
files = {}

TAG = "BRANDS × CREATORS"


def justify(text, size, target, weight=600):
    """Letterspace text to an exact width — proper tracking, never a scale
    transform, which would squash the letterforms."""
    base = ts.width(text, weight, size, 0.0)
    n = max(1, len(text) - 1)
    return (target - base) / (size * n)


# --------------------------------------------------------------- master H
def master_h(mark_d=104, gap=32, wm_size=68, pad=26,
             arcs=CREAM, dot=ACCENT, the=MUTED, beauty=CREAM, cast=ACCENT,
             tagline=None, tag_col=MUTED):
    """Horizontal master lockup. Optional tagline sits under the wordmark,
    left-aligned to it and locked to its width."""
    cap = ts.cap_height(900, wm_size)
    wm_w = ts.width(NAME, 900, wm_size, -0.025) + 0.025 * wm_size
    tag_size = wm_size * 0.208
    tag_gap = wm_size * 0.20
    block_h = cap + (tag_gap + ts.cap_height(900, tag_size) if tagline else 0)
    h = max(mark_d, block_h) + pad * 2
    cy = h / 2
    body = [signal(pad + mark_d / 2, cy, mark_d / 200, arcs, dot)]
    x = pad + mark_d + gap
    top = cy - block_h / 2
    wm, _ = wordmark(x, top + cap, wm_size, the, beauty, cast)
    body.append(wm)
    if tagline:
        tr = justify(tagline, tag_size, wm_w)
        d, _ = ts.typeset(tagline, 600, tag_size, tr, x,
                          top + cap + tag_gap + ts.cap_height(900, tag_size))
        body.append(f'<path d="{d}" fill="{tag_col}"/>')
    return "".join(body), round(pad * 2 + mark_d + gap + wm_w), round(h)


# --------------------------------------------------------------- master V
def master_v(mark_d=150, wm_size=62, pad=26,
             arcs=CREAM, dot=ACCENT, the=MUTED, beauty=CREAM, cast=ACCENT,
             tagline=None, tag_col=MUTED, rule=None):
    cap = ts.cap_height(900, wm_size)
    wm_w = ts.width(NAME, 900, wm_size, -0.025) + 0.025 * wm_size
    tag_size = wm_size * 0.215
    gap1 = mark_d * 0.17
    W = round(max(mark_d, wm_w) + pad * 2)
    y = pad + mark_d
    body = [signal(W / 2, pad + mark_d / 2, mark_d / 200, arcs, dot)]
    base = y + gap1 + cap
    wm, _ = wordmark((W - wm_w) / 2, base, wm_size, the, beauty, cast)
    body.append(wm)
    bottom = base
    if rule:
        ry = base + wm_size * 0.42
        rw = wm_w * 0.30
        body.append(f'<rect x="{(W-rw)/2:.1f}" y="{ry:.1f}" width="{rw:.1f}" '
                    f'height="{max(2, wm_size*0.032):.1f}" fill="{rule}"/>')
        bottom = ry + 4
    if tagline:
        ty = bottom + wm_size * (0.52 if rule else 0.42) + ts.cap_height(900, tag_size)
        tr = justify(tagline, tag_size, wm_w * 0.86)
        d, _ = ts.typeset(tagline, 600, tag_size, tr,
                          (W - wm_w * 0.86) / 2, ty)
        body.append(f'<path d="{d}" fill="{tag_col}"/>')
        bottom = ty
    return "".join(body), W, round(bottom + pad)


# ------------------------------------------------------------------- cuts
b, w, h = master_h()
files["LOGO-MASTER"] = svg(w, h, b)
b, w, h = master_h(the=MUTED_DEEP, beauty=INK, cast=ACCENT_DEEP,
                   arcs=INK, dot=ACCENT_DEEP)
files["LOGO-MASTER-light"] = svg(w, h, b)
b, w, h = master_h(tagline=TAG)
files["LOGO-MASTER-tagline"] = svg(w, h, b)
b, w, h = master_h(tagline=TAG, the=MUTED_DEEP, beauty=INK, cast=ACCENT_DEEP,
                   arcs=INK, dot=ACCENT_DEEP, tag_col=MUTED_DEEP)
files["LOGO-MASTER-tagline-light"] = svg(w, h, b)
b, w, h = master_h(arcs=CREAM, dot=CREAM, the=CREAM, beauty=CREAM, cast=CREAM)
files["LOGO-MASTER-1c-cream"] = svg(w, h, b)
b, w, h = master_h(arcs=INK, dot=INK, the=INK, beauty=INK, cast=INK)
files["LOGO-MASTER-1c-ink"] = svg(w, h, b)

b, w, h = master_v(tagline=TAG, rule=ACCENT)
files["LOGO-MASTER-stacked"] = svg(w, h, b)
b, w, h = master_v(tagline=TAG, rule=ACCENT_DEEP, the=MUTED_DEEP, beauty=INK,
                   cast=ACCENT_DEEP, arcs=INK, dot=ACCENT_DEEP, tag_col=MUTED_DEEP)
files["LOGO-MASTER-stacked-light"] = svg(w, h, b)


# ------------------------------------------------------------- watermarks
def watermark(kind, colour, shadow, opacity=0.82):
    """Single-colour watermark with a baked soft shadow so it holds over any
    footage. Never tri-tone — a watermark must survive compression."""
    if kind == "lockup":
        b, w, h = master_h(mark_d=104, gap=30, wm_size=68, pad=18,
                           arcs=colour, dot=colour, the=colour,
                           beauty=colour, cast=colour)
    else:
        w = h = 200
        b = signal(100, 100, 0.86, arcs=colour, dot=colour)
    fil = (f'<filter id="s" x="-30%" y="-30%" width="160%" height="160%">'
           f'<feDropShadow dx="0" dy="{h*0.018:.1f}" stdDeviation="{h*0.030:.1f}" '
           f'flood-color="{shadow}" flood-opacity="0.55"/></filter>')
    return svg(w, h, f'<defs>{fil}</defs>'
                     f'<g filter="url(#s)" opacity="{opacity}">{b}</g>')


files["WATERMARK-lockup-cream"] = watermark("lockup", CREAM, "#000000")
files["WATERMARK-lockup-ink"] = watermark("lockup", INK, "#FFFFFF")
files["WATERMARK-mark-cream"] = watermark("mark", CREAM, "#000000")
files["WATERMARK-mark-ink"] = watermark("mark", INK, "#FFFFFF")

for name, data in files.items():
    open(f"{OUT}/{name}.svg", "w").write(data)
print(f"wrote {len(files)} master/watermark svgs")
