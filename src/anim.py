"""The intro sting — 3 seconds, built from the same geometry as the logo.

Beats:  the source lands · the signal sweeps out · the name rises ·
        the rule sets · the promise · the signal pulses and holds.
"""
import os, math, shutil, subprocess, sys
import typeset as ts
from build import INK, CREAM, ACCENT, MUTED, arc, NAME

FPS = 30
DUR = 3.0
NF = int(FPS * DUR)
TAG = "BRANDS × CREATORS"


# ------------------------------------------------------------------ easing
def clamp01(x):
    return 0.0 if x < 0 else (1.0 if x > 1 else x)


def seg(t, a, b):
    """Normalised progress of t through the window [a, b] in seconds."""
    return clamp01((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)


def out_cubic(t):
    return 1 - (1 - t) ** 3


def out_quart(t):
    return 1 - (1 - t) ** 4


def out_back(t, s=1.55):
    return 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2


def out_expo(t):
    return 1.0 if t >= 1 else 1 - 2 ** (-9 * t)


# ------------------------------------------------------------------ layout
def layout(W, H, d_ratio):
    D = min(W, H) * d_ratio
    wm_size = D * 0.245
    cap = ts.cap_height(900, wm_size)
    wm_w = ts.width(NAME, 900, wm_size, -0.025) + 0.025 * wm_size
    tag_size = wm_size * 0.215
    tag_cap = ts.cap_height(900, tag_size)
    rule_h = max(2.0, wm_size * 0.034)
    rule_w = wm_w * 0.30

    gap1 = D * 0.17
    gap2 = wm_size * 0.42
    gap3 = wm_size * 0.52
    group_h = D + gap1 + cap + gap2 + rule_h + gap3 + tag_cap
    gy = (H - group_h) / 2

    return dict(
        W=W, H=H, D=D, cx=W / 2, mark_cy=gy + D / 2,
        wm_size=wm_size, cap=cap, wm_w=wm_w,
        wm_base=gy + D + gap1 + cap,
        rule_y=gy + D + gap1 + cap + gap2, rule_h=rule_h, rule_w=rule_w,
        tag_size=tag_size,
        tag_base=gy + D + gap1 + cap + gap2 + rule_h + gap3 + tag_cap,
    )


def justify(text, size, target, weight=600):
    base = ts.width(text, weight, size, 0.0)
    return (target - base) / (size * max(1, len(text) - 1))


# ------------------------------------------------------------------- frame
def frame(t, L):
    W, H, D, cx, cy = L["W"], L["H"], L["D"], L["cx"], L["mark_cy"]
    k = D / 200.0
    g = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']

    # --- the source dot lands ------------------------------------------
    p = seg(t, 0.00, 0.34)
    dot_s = out_back(p) if p < 1 else 1.0
    dot_o = seg(t, 0.00, 0.12)
    if dot_s > 0:
        # soft accent glow, keyed to the dot
        gr = 15 * k * dot_s * 4.6
        g.append(f'<defs><radialGradient id="glow"><stop offset="0" '
                 f'stop-color="{ACCENT}" stop-opacity="{0.30*dot_o:.3f}"/>'
                 f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>'
                 f'</radialGradient></defs>')
        g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{gr:.1f}" fill="url(#glow)"/>')
        g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{15*k*dot_s:.2f}" '
                 f'fill="{ACCENT}" opacity="{dot_o:.3f}"/>')

    # --- the signal sweeps out ------------------------------------------
    for r_u, sw_u, a, b in ((44, 15, 0.18, 0.95), (73, 15, 0.32, 1.08)):
        pr = out_quart(seg(t, a, b))
        if pr <= 0:
            continue
        r = r_u * k
        length = 2 * math.pi * r * 0.75
        g.append(f'<path d="{arc(cx, cy, r, 45, 315)}" fill="none" '
                 f'stroke="{CREAM}" stroke-width="{sw_u*k:.2f}" stroke-linecap="round" '
                 f'stroke-dasharray="{length:.2f} {length:.2f}" '
                 f'stroke-dashoffset="{length*(1-pr):.2f}"/>')

    # --- the name rises --------------------------------------------------
    words = [("The", MUTED, 1.00), ("Beauty", CREAM, 1.08), ("Cast", ACCENT, 1.16)]
    cursor = cx - L["wm_w"] / 2
    for txt, col, start in words:
        d, adv = ts.typeset(txt, 900, L["wm_size"], -0.025, cursor, L["wm_base"])
        pw = seg(t, start, start + 0.38)
        if pw > 0:
            e = out_cubic(pw)
            dy = (1 - e) * L["wm_size"] * 0.26
            g.append(f'<g transform="translate(0,{dy:.2f})" opacity="{e:.3f}">'
                     f'<path d="{d}" fill="{col}"/></g>')
        cursor += adv

    # --- the rule sets ---------------------------------------------------
    pr = out_expo(seg(t, 1.46, 1.80))
    if pr > 0:
        w = L["rule_w"] * pr
        g.append(f'<rect x="{cx-w/2:.1f}" y="{L["rule_y"]:.1f}" width="{w:.1f}" '
                 f'height="{L["rule_h"]:.1f}" fill="{ACCENT}"/>')

    # --- the promise -----------------------------------------------------
    pt = seg(t, 1.64, 2.00)
    if pt > 0:
        e = out_cubic(pt)
        tr = justify(TAG, L["tag_size"], L["wm_w"] * 0.86)
        d, _ = ts.typeset(TAG, 600, L["tag_size"], tr,
                          cx - L["wm_w"] * 0.86 / 2, L["tag_base"])
        g.append(f'<g transform="translate(0,{(1-e)*L["tag_size"]*0.5:.2f})" '
                 f'opacity="{e:.3f}"><path d="{d}" fill="{MUTED}"/></g>')

    # --- the signal pulses ------------------------------------------------
    for start in (1.92, 2.16):
        pp = seg(t, start, start + 0.78)
        if 0 < pp < 1:
            r = 15 * k + (D * 0.72 - 15 * k) * out_cubic(pp)
            g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
                     f'stroke="{ACCENT}" stroke-width="{max(1.5, 3*k):.2f}" '
                     f'opacity="{0.5*(1-pp)**1.6:.3f}"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">{"".join(g)}</svg>')


# ------------------------------------------------------------------ render
FORMATS = [("vertical", 1080, 1920, 0.33),
           ("square", 1080, 1080, 0.30),
           ("landscape", 1920, 1080, 0.28)]


def render(only=None):
    import cairosvg
    os.makedirs("out/video", exist_ok=True)
    for name, W, H, dr in FORMATS:
        if only and name != only:
            continue
        L = layout(W, H, dr)
        fd = f"frames_{name}"
        shutil.rmtree(fd, ignore_errors=True)
        os.makedirs(fd)
        for i in range(NF):
            t = i / FPS
            cairosvg.svg2png(bytestring=frame(t, L).encode(),
                             write_to=f"{fd}/{i:04d}.png",
                             output_width=W, output_height=H)
        mp4 = f"out/video/intro-{name}-{W}x{H}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", f"{fd}/%04d.png", "-c:v", "libx264", "-preset", "slow",
                        "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        mp4], check=True)
        print("  ", mp4, os.path.getsize(mp4) // 1024, "KB")
    # a small looping GIF from the square cut, for email and web previews
    if not only or only == "square":
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", "frames_square/%04d.png",
                        "-vf", "fps=15,scale=480:-1:flags=lanczos,split[a][b];"
                               "[a]palettegen=stats_mode=diff[p];[b][p]paletteuse",
                        "out/video/intro-480.gif"], check=True)
        print("   out/video/intro-480.gif",
              os.path.getsize("out/video/intro-480.gif") // 1024, "KB")


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else None)
