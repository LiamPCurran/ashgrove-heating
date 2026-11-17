"""Crop and compress the Unsplash stock photos used on the Ashgrove site.

Originals live in ../_stock/u_<UnsplashID>.jpg (Unsplash License: free to use, no attribution required).
Output: assets/img/<name>-<width>.webp
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
SRC = ROOT.parent / "_stock"
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# name: (unsplash id, crop box on the 1600px-wide original or None, output widths)
PHOTOS = {
    "hero":       ("L5sEqpQukJI", (0, 330, 1470, 1157), (800, 1440)),   # technician servicing outdoor unit (logo cropped out)
    "furnace":    ("AlhRs3I8f7M", (100, 0, 1500, 1050), (480, 800, 1440)),    # gloved hands repairing a unit
    "heatpump":   ("kblddocwPa0", (100, 0, 1500, 1050), (480, 800, 1440)),
    "ac":         ("-nbWCvUiFJA", (0, 0, 1424, 1067), (480, 800, 1440)),
    "thermostat": ("3_nf1qKJGf4", (60, 0, 1484, 1067), (480, 800, 1440)),
    "gauges":     ("8RbiLgfqoqQ", (0, 0, 1600, 1067), (800, 1440)),
    "ductless":   ("BsHycOlU6Bg", (0, 200, 1600, 2200), (640, 1000)),   # mini-split in a living room (4:5)
    "cozy":       ("Tnx-t6CTg5o", (0, 0, 1600, 900), (640, 800, 1000, 1440)),
    "winter":     ("mk9kC-klh5o", (0, 900, 1600, 1800), (800, 1440)),   # chimney smoke on a cold morning
}

for name, (pid, box, widths) in PHOTOS.items():
    im = Image.open(SRC / f"u_{pid}.jpg").convert("RGB")
    if box:
        im = im.crop(box)
    for w in widths:
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(OUT / f"{name}-{w}.webp", "WEBP", quality=72, method=6)
    print(name, im.size, "->", widths)
