"""Rasterise the profile/favicon assets with Chromium and zip the collection."""
import os, asyncio, zipfile, shutil, glob
from playwright.async_api import async_playwright

RASTER = [
    ("mark-signal-avatar", 1024), ("mark-signal-avatar-accent", 1024),
    ("monogram-bc-avatar", 1024), ("emblem-seal-avatar", 1024),
    ("mark-signal-tile", 1024), ("monogram-bc-tile", 1024),
    ("favicon", 180), ("favicon", 32), ("favicon-16", 16),
    ("closing-frame", 1080),
]
os.makedirs("out/png", exist_ok=True)


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for name, size in RASTER:
            src = open(f"out/{name}.svg").read()
            # keep the intrinsic aspect ratio
            import re
            vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src)
            vw, vh = float(vb.group(1)), float(vb.group(2))
            w, h = size, round(size * vh / vw)
            page = await b.new_page(viewport={"width": w, "height": h})
            await page.set_content(
                f'<style>html,body{{margin:0}}svg{{display:block;width:{w}px;height:{h}px}}'
                f'</style>{src}')
            out = f"out/png/{name}-{size}.png"
            await page.screenshot(path=out, omit_background=True)
            await page.close()
            print("  ", out)
        await b.close()

asyncio.run(main())

with zipfile.ZipFile("TheBeautyCast-logos.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(glob.glob("out/*.svg")):
        z.write(p, f"TheBeautyCast-logos/svg/{os.path.basename(p)}")
    for p in sorted(glob.glob("out/png/*.png")):
        z.write(p, f"TheBeautyCast-logos/png/{os.path.basename(p)}")
    z.write("README.txt", "TheBeautyCast-logos/README.txt")
print("zipped", os.path.getsize("TheBeautyCast-logos.zip"), "bytes")
