"""Generate assets/og.png (1200x630 social preview) with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#12324f")
d = ImageDraw.Draw(img)
d.rectangle([0, H - 18, W, H], fill="#d9631c")

def font(size, bold=True):
    for name in (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()

# flame mark
d.rounded_rectangle([80, 90, 200, 210], radius=26, fill="#1d4a72")
d.polygon([(140, 108), (175, 165), (168, 192), (112, 192), (105, 165), (128, 150)], fill="#d9631c")
d.text((80, 260), "Ashgrove Heating & Air", font=font(72), fill="white")
d.text((80, 360), "Furnace, heat pump & AC service in Ottawa", font=font(40, False), fill="#d6e2ee")
d.text((80, 470), "(613) 555-0142  ·  Concept project", font=font(32, False), fill="#f2b386")
out = Path(__file__).parent / "assets" / "og.png"
img.save(out, optimize=True)
print(out, out.stat().st_size)
