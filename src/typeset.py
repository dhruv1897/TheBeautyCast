"""Turn Inter text into pure SVG path data — no font dependency in the output."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.misc.transform import Transform

FONTS = {}
DIR = "node_modules/@fontsource/inter/files/inter-latin-%s-normal.woff"


def font(weight):
    if weight not in FONTS:
        FONTS[weight] = TTFont(DIR % weight)
    return FONTS[weight]


def typeset(text, weight=900, size=100, tracking=0.0, x=0.0, y=0.0):
    """Return (path_data, advance_width).

    tracking is in em units (0.01 == 10 units per 1000). y is the baseline.
    Kerning from the font's kern/GPOS pairs is applied where available.
    """
    f = font(weight)
    upem = f["head"].unitsPerEm
    scale = size / upem
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f["hmtx"]
    kern = _kern_table(f)

    pen_out = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
    cursor = 0.0
    prev = None
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            cursor += upem * 0.3
            prev = None
            continue
        if prev is not None:
            cursor += kern.get((prev, gname), 0)
        t = Transform(scale, 0, 0, -scale, x + cursor * scale, y)
        tp = TransformPen(pen_out, t)
        gs[gname].draw(tp)
        cursor += hmtx[gname][0] + tracking * upem
        prev = gname
    return pen_out.getCommands(), cursor * scale


def _kern_table(f):
    """Flatten GPOS pair kerning into a {(left, right): value} dict."""
    cache = getattr(f, "_flat_kern", None)
    if cache is not None:
        return cache
    pairs = {}
    if "GPOS" in f:
        try:
            for lookup in f["GPOS"].table.LookupList.Lookup:
                if lookup.LookupType != 2:
                    continue
                for st in lookup.SubTable:
                    if st.Format == 1:
                        cov = st.Coverage.glyphs
                        for i, ps in enumerate(st.PairSet):
                            for pv in ps.PairValueRecord:
                                v = getattr(pv.Value1, "XAdvance", 0) or 0
                                if v:
                                    pairs[(cov[i], pv.SecondGlyph)] = v
                    elif st.Format == 2:
                        cov = set(st.Coverage.glyphs)
                        c1 = st.ClassDef1.classDefs
                        c2 = st.ClassDef2.classDefs
                        by1, by2 = {}, {}
                        for g, c in c1.items():
                            by1.setdefault(c, []).append(g)
                        for g, c in c2.items():
                            by2.setdefault(c, []).append(g)
                        for i, rec in enumerate(st.Class1Record):
                            for j, r2 in enumerate(rec.Class2Record):
                                v = getattr(r2.Value1, "XAdvance", 0) or 0
                                if not v:
                                    continue
                                for g1 in by1.get(i, []):
                                    if g1 not in cov:
                                        continue
                                    for g2 in by2.get(j, []):
                                        pairs[(g1, g2)] = v
        except Exception:
            pass
    f._flat_kern = pairs
    return pairs


def width(text, weight=900, size=100, tracking=0.0):
    return typeset(text, weight, size, tracking)[1]


def centered(text, weight=900, size=100, tracking=0.0, cx=0.0, y=0.0):
    """Typeset horizontally centred on cx."""
    w = width(text, weight, size, tracking) - tracking * size
    d, _ = typeset(text, weight, size, tracking, x=cx - w / 2, y=y)
    return d, w


import math


def typeset_arc(text, weight=700, size=100, tracking=0.0, radius=200.0,
                cx=0.0, cy=0.0, beta=0.0, flip=False):
    """Typeset text along a circle. beta is the tilt of the text's midpoint in
    degrees clockwise from the top of the circle: 0 across the top, 180 across
    the bottom. flip=True (use for bottom text) keeps glyphs upright when read
    from outside the circle.
    """
    f = font(weight)
    upem = f["head"].unitsPerEm
    scale = size / upem
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f["hmtx"]

    advances = []
    for ch in text:
        gname = cmap.get(ord(ch))
        adv = (hmtx[gname][0] if gname else upem * 0.3) + tracking * upem
        advances.append((gname, adv * scale))

    total = sum(a for _, a in advances) - tracking * size
    span_deg = math.degrees(total / radius)
    step = -1 if flip else 1
    b = beta - step * span_deg / 2

    pen_out = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
    for gname, adv in advances:
        adv_deg = math.degrees(adv / radius)
        if gname is None:
            b += step * adv_deg
            continue
        centre = b + step * adv_deg / 2
        t = Transform().translate(cx, cy).rotate(math.radians(centre))
        t = t.translate(0, -radius)
        if flip:
            t = t.rotate(math.pi)
        t = t.translate(-adv / 2, 0).scale(scale, -scale)
        gs[gname].draw(TransformPen(pen_out, t))
        b += step * adv_deg
    return pen_out.getCommands()


def arc_span(text, weight=700, size=100, tracking=0.0, radius=200.0):
    """Degrees of arc the text will occupy at this radius."""
    return math.degrees((width(text, weight, size, tracking) - tracking * size) / radius)


def cap_height(weight=900, size=100):
    f = font(weight)
    upem = f["head"].unitsPerEm
    os2 = f["OS/2"]
    ch = getattr(os2, "sCapHeight", None) or int(upem * 0.727)
    return ch / upem * size
