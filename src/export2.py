"""Rasterise the master logo and watermarks to transparent PNGs (real renderer,
so feDropShadow and paint-order survive)."""
import os, re, asyncio
from playwright.async_api import async_playwright

JOBS = [
    ("LOGO-MASTER", 2000), ("LOGO-MASTER-light", 2000),
    ("LOGO-MASTER-tagline", 2000), ("LOGO-MASTER-tagline-light", 2000),
    ("LOGO-MASTER-stacked", 1400), ("LOGO-MASTER-stacked-light", 1400),
    ("LOGO-MASTER-1c-cream", 2000), ("LOGO-MASTER-1c-ink", 2000),
    ("WATERMARK-lockup-cream", 1400), ("WATERMARK-lockup-ink", 1400),
    ("WATERMARK-mark-cream", 600), ("WATERMARK-mark-ink", 600),
]
os.makedirs("out/png", exist_ok=True)


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for name, width in JOBS:
            src = open(f"out/{name}.svg").read()
            vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src)
            vw, vh = float(vb.group(1)), float(vb.group(2))
            w, h = width, round(width * vh / vw)
            page = await b.new_page(viewport={"width": w, "height": h})
            await page.set_content(
                f'<style>html,body{{margin:0;background:transparent}}'
                f'svg{{display:block;width:{w}px;height:{h}px}}</style>{src}')
            out = f"out/png/{name}-{w}.png"
            await page.screenshot(path=out, omit_background=True)
            await page.close()
            print("  ", out, os.path.getsize(out) // 1024, "KB")
        await b.close()

asyncio.run(main())
