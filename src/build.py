"""TheBeautyCast — logo collection builder.

Every wordmark is emitted as outlined vector paths (no font dependency).
Palette and type are locked to the project's reel system.
"""
import math, os, textwrap
import typeset as ts

INK = "#0C0B0E"
CREAM = "#FAF7F3"
ACCENT = "#FF7A45"
MUTED = "#A8A29B"
# Same hue, darkened for light grounds: #FF7A45 on cream is only 2.4:1 and
# goes weak in print and at small sizes. This is 4.2:1.
ACCENT_DEEP = "#C2572C"
MUTED_DEEP = "#6F6A64"

OUT = "out"
os.makedirs(OUT, exist_ok=True)

NAME = "TheBeautyCast"
HANDLE = "@thebeautycast"


# ---------------------------------------------------------------- primitives

def arc(cx, cy, r, a0, a1):
    """Arc path from angle a0 to a1 (degrees, counter-clockwise on screen)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f"M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 {large} 0 {x1:.2f} {y1:.2f}")


def svg(w, h, body, bg=None, vb=None):
    vb = vb or f"0 0 {w} {h}"
    rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="{vb}">{rect}{body}</svg>')


# --------------------------------------------------------------------- marks

def signal(cx=100, cy=100, k=1.0, arcs=CREAM, dot=ACCENT, rings=2,
           single=(58, 22), dot_r=15):
    """The Signal C — a broadcast source inside an aperture that reads as 'C'.

    Two nested arcs, each open on the right, around a solid source dot.
    rings=1 is the small-size reduction: one heavier arc, no inner ring.
    """
    g = [f'<circle cx="{cx}" cy="{cy}" r="{dot_r*k:.2f}" fill="{dot}"/>']
    radii = [(44, 15), (73, 15)][:rings] if rings == 2 else [single]
    for r, sw in radii:
        g.append(f'<path d="{arc(cx, cy, r*k, 45, 315)}" fill="none" '
                 f'stroke="{arcs}" stroke-width="{sw*k:.2f}" stroke-linecap="round"/>')
    return "".join(g)


OVERLAP = 0.10  # em the C laps over the B


def _mono_ratio():
    s = 100.0
    return (ts.width("B", 900, s) + ts.width("C", 900, s) - OVERLAP * s) / s


def monogram(cx=100, cy=100, w=148.0, b_fill=CREAM, c_fill=ACCENT, knock=INK):
    """BC ligature cut from real Inter 900 letterforms, interlocked.

    The C laps the B by a tenth of an em — enough to interlock, little enough
    that the B's bowls stay intact and it never reads as an E. `w` is the
    total drawn width, so the mark can be fitted to any container.
    """
    s = w / _mono_ratio()
    wb = ts.width("B", 900, s)
    wc = ts.width("C", 900, s)
    overlap = OVERLAP * s
    total = wb + wc - overlap
    cap = ts.cap_height(900, s)
    x = cx - total / 2
    y = cy + cap / 2
    db, _ = ts.typeset("B", 900, s, 0, x, y)
    dc, _ = ts.typeset("C", 900, s, 0, x + wb - overlap, y)
    return (f'<path d="{db}" fill="{b_fill}"/>'
            f'<path d="{dc}" fill="{c_fill}" stroke="{knock}" '
            f'stroke-width="{0.055*s:.2f}" stroke-linejoin="round" '
            f'paint-order="stroke fill"/>')


def emblem(cx=100, cy=100, k=1.0, ring=ACCENT, text=CREAM, hair=MUTED,
           arcs=CREAM, dot=ACCENT):
    """Circular seal — the mark stamped with the name and the promise."""
    top, bot = "THE BEAUTY CAST", "BRANDS × CREATORS"
    r_txt = 73 * k
    span_top = ts.arc_span(top, 800, 14 * k, 0.15, r_txt)
    g = [
        f'<circle cx="{cx}" cy="{cy}" r="{94*k:.2f}" fill="none" stroke="{ring}" stroke-width="{3*k:.2f}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{86*k:.2f}" fill="none" stroke="{hair}" stroke-width="{1*k:.2f}" opacity="0.55"/>',
        f'<path d="{ts.typeset_arc(top, 800, 14*k, 0.15, r_txt, cx, cy, 0)}" fill="{text}"/>',
        f'<path d="{ts.typeset_arc(bot, 600, 9.5*k, 0.22, r_txt, cx, cy, 180, flip=True)}" fill="{hair}"/>',
    ]
    # separator diamonds sit just outside the ends of the longer arc of text
    for beta in (span_top / 2 + 16, -(span_top / 2 + 16)):
        px = cx + 74 * k * math.sin(math.radians(beta))
        py = cy - 74 * k * math.cos(math.radians(beta))
        g.append(f'<rect x="{px-3*k:.2f}" y="{py-3*k:.2f}" width="{6*k:.2f}" '
                 f'height="{6*k:.2f}" fill="{ring}" transform="rotate(45 {px:.2f} {py:.2f})"/>')
    g.append(signal(cx, cy, 0.46 * k, arcs, dot))
    return "".join(g)


def wordmark(x, y, size, the=MUTED, beauty=CREAM, cast=ACCENT, tracking=-0.025):
    """Tri-tone wordmark: the article recedes, the promise ('Cast') carries the accent."""
    parts, cursor, out = [("The", the), ("Beauty", beauty), ("Cast", cast)], x, []
    for txt, col in parts:
        d, adv = ts.typeset(txt, 900, size, tracking, cursor, y)
        out.append(f'<path d="{d}" fill="{col}"/>')
        cursor += adv
    return "".join(out), cursor - x - tracking * size


def wordmark_mono(x, y, size, fill=CREAM, tracking=-0.025):
    d, adv = ts.typeset(NAME, 900, size, tracking, x, y)
    return f'<path d="{d}" fill="{fill}"/>', adv - tracking * size


# --------------------------------------------------------------------- files

files = {}

# 1 — Wordmark, primary + variants -------------------------------------------
def build_wordmark(name, **kw):
    size, pad = 100, 24
    body, w = wordmark(pad, pad + ts.cap_height(900, size), size, **kw)
    h = pad * 2 + ts.cap_height(900, size) + size * 0.22
    files[name] = svg(round(w + pad * 2), round(h), body)

build_wordmark("wordmark-primary")                       # for dark grounds
build_wordmark("wordmark-light", the=MUTED_DEEP, beauty=INK, cast=ACCENT_DEEP)
size, pad = 100, 24
b, w = wordmark_mono(pad, pad + ts.cap_height(900, size), size, CREAM)
files["wordmark-mono-cream"] = svg(round(w + pad*2), round(pad*2 + ts.cap_height(900,size) + size*0.22), b)
b, w = wordmark_mono(pad, pad + ts.cap_height(900, size), size, INK)
files["wordmark-mono-ink"] = svg(round(w + pad*2), round(pad*2 + ts.cap_height(900,size) + size*0.22), b)

# 2 — Signal mark ------------------------------------------------------------
files["mark-signal"] = svg(200, 200, signal())
files["mark-signal-light"] = svg(200, 200, signal(arcs=INK, dot=ACCENT_DEEP))
files["mark-signal-tile"] = svg(
    200, 200,
    f'<rect width="200" height="200" rx="46" fill="{INK}"/>' + signal(k=0.92))
files["mark-signal-avatar"] = svg(
    200, 200,
    f'<circle cx="100" cy="100" r="100" fill="{INK}"/>' + signal(k=0.88))
files["mark-signal-avatar-accent"] = svg(
    200, 200,
    f'<circle cx="100" cy="100" r="100" fill="{ACCENT}"/>'
    + signal(k=0.88, arcs=INK, dot=CREAM))

# 3 — Monogram ---------------------------------------------------------------
files["monogram-bc"] = svg(200, 200, monogram(w=152))
files["monogram-bc-light"] = svg(200, 200, monogram(w=152, b_fill=INK,
                                                    c_fill=ACCENT_DEEP, knock=CREAM))
files["monogram-bc-tile"] = svg(
    200, 200,
    f'<rect width="200" height="200" rx="46" fill="{INK}"/>' + monogram(w=130))
files["monogram-bc-avatar"] = svg(
    200, 200,
    f'<circle cx="100" cy="100" r="100" fill="{ACCENT}"/>'
    + monogram(w=126, b_fill=INK, c_fill=CREAM, knock=ACCENT))

# 4 — Emblem -----------------------------------------------------------------
files["emblem-seal"] = svg(200, 200, emblem())
files["emblem-seal-avatar"] = svg(
    200, 200, f'<circle cx="100" cy="100" r="100" fill="{INK}"/>' + emblem(k=0.94))
files["emblem-seal-light"] = svg(
    200, 200, emblem(text=INK, arcs=INK, hair=MUTED_DEEP,
                     ring=ACCENT_DEEP, dot=ACCENT_DEEP))

# 5 — Lockups ----------------------------------------------------------------
def lockup_h(name, mark_fn, arcs=CREAM, the=MUTED, beauty=CREAM, cast=ACCENT):
    ms, gap, tsize = 96, 30, 62
    cap = ts.cap_height(900, tsize)
    pad = 22
    cy = pad + ms / 2
    body = [mark_fn(pad + ms / 2, cy, ms / 200)]
    wm, w = wordmark(pad + ms + gap, cy + cap / 2, tsize, the, beauty, cast)
    body.append(wm)
    files[name] = svg(round(pad * 2 + ms + gap + w), round(pad * 2 + ms), "".join(body))

lockup_h("lockup-horizontal", lambda cx, cy, k: signal(cx, cy, k))
lockup_h("lockup-horizontal-light",
         lambda cx, cy, k: signal(cx, cy, k, arcs=INK, dot=ACCENT_DEEP),
         the=MUTED_DEEP, beauty=INK, cast=ACCENT_DEEP)
lockup_h("lockup-horizontal-monogram",
         lambda cx, cy, k: monogram(cx, cy, 152 * k))

# stacked
ms, tsize, gap, pad = 128, 54, 26, 24
cap = ts.cap_height(900, tsize)
wm_w = ts.width(NAME, 900, tsize, -0.025) + 0.025 * tsize
W = round(max(ms, wm_w) + pad * 2)
H = round(pad * 2 + ms + gap + cap)
body = signal(W / 2, pad + ms / 2, ms / 200)
wm, _ = wordmark((W - wm_w) / 2, pad + ms + gap + cap, tsize)
files["lockup-stacked"] = svg(W, H, body + wm)
body_l = signal(W / 2, pad + ms / 2, ms / 200, arcs=INK, dot=ACCENT_DEEP)
wm_l, _ = wordmark((W - wm_w) / 2, pad + ms + gap + cap, tsize,
                   the=MUTED_DEEP, beauty=INK, cast=ACCENT_DEEP)
files["lockup-stacked-light"] = svg(W, H, body_l + wm_l)

# 6 — Favicon (reduced: one arc, one dot) ------------------------------------
files["favicon"] = svg(
    32, 32,
    f'<rect width="32" height="32" rx="7" fill="{INK}"/>'
    + signal(16, 16, 32 / 200 * 1.02, arcs=CREAM, dot=ACCENT, rings=1))
files["favicon-mark-only"] = svg(
    32, 32, signal(16, 16, 32 / 200 * 1.08, arcs=CREAM, dot=ACCENT, rings=1))
# 16px needs a heavier cut again — at that size a 22-unit stroke goes to mush
files["favicon-16"] = svg(
    16, 16,
    f'<rect width="16" height="16" rx="3.5" fill="{INK}"/>'
    + signal(8, 8, 16 / 200 * 1.06, arcs=CREAM, dot=ACCENT, rings=1,
             single=(52, 32), dot_r=17))

# 7 — Reel masthead badge ----------------------------------------------------
bh, bpad, bts = 64, 30, 26
cap26 = ts.cap_height(900, bts)
label = "CREATOR SPOTLIGHT"
lw = ts.width(label, 800, bts, 0.1) - 0.1 * bts
mk = 40
BW = round(bpad + mk + 18 + lw + bpad)
d, _ = ts.typeset(label, 800, bts, 0.1, bpad + mk + 18, bh / 2 + cap26 / 2)
files["masthead-badge"] = svg(
    BW, bh,
    f'<rect width="{BW}" height="{bh}" rx="{bh/2}" fill="{ACCENT}"/>'
    + signal(bpad + mk / 2, bh / 2, mk / 200 * 1.15, arcs=INK, dot=CREAM)
    + f'<path d="{d}" fill="{INK}"/>')

# 8 — Closing frame lockup (the locked sign-off) -----------------------------
CW, CH = 1080, 420
cap44 = ts.cap_height(900, 44)
l1, w1 = ts.typeset("Brands: we'll introduce you.", 900, 44, -0.02, 0, 0)
l2, w2 = ts.typeset("Creators: we'll get you paid.", 900, 44, -0.02, 0, 0)
h_d, h_w = ts.typeset(HANDLE, 600, 30, 0.02, 0, 0)
body = [
    f'<rect width="{CW}" height="{CH}" fill="{INK}"/>',
    signal(CW / 2, 96, 132 / 200),
    f'<g transform="translate({(CW-w1)/2:.1f},{206+cap44:.1f})"><path d="{l1}" fill="{CREAM}"/></g>',
    f'<g transform="translate({(CW-w2)/2:.1f},{206+cap44+62:.1f})"><path d="{l2}" fill="{ACCENT}"/></g>',
    f'<g transform="translate({(CW-h_w)/2:.1f},{CH-46:.1f})"><path d="{h_d}" fill="{MUTED}"/></g>',
]
files["closing-frame"] = svg(CW, CH, "".join(body))

for name, data in files.items():
    with open(f"{OUT}/{name}.svg", "w") as fh:
        fh.write(data)

print(f"wrote {len(files)} svgs")
for n in sorted(files):
    print(" ", n, len(files[n]), "bytes")
