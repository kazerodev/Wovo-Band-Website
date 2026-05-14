"""
WovoBand image processing — v2
Crops raw AliExpress images, removes text/banners, dark bg treatment.
"""
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os

DIR = r'C:\Users\akaga\wovoband\images'
BG = (8, 8, 16)  # site --bg: #080810

def dark_canvas(w=800, h=800):
    return Image.new('RGB', (w, h), BG)

def place_on_dark(crop, cw=800, ch=800, pad=0.06):
    """Scale crop to fill canvas with padding, centered."""
    max_w = int(cw * (1 - pad * 2))
    max_h = int(ch * (1 - pad * 2))
    scale = min(max_w / crop.width, max_h / crop.height)
    nw, nh = int(crop.width * scale), int(crop.height * scale)
    resized = crop.resize((nw, nh), Image.LANCZOS)
    canvas = dark_canvas(cw, ch)
    canvas.paste(resized, ((cw - nw) // 2, (ch - nh) // 2))
    return canvas

def vignette(img, strength=0.5):
    """Radial dark vignette — blends product edges into dark bg."""
    w, h = img.size
    overlay = dark_canvas(w, h)
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    steps = 50
    for i in range(steps):
        ratio = i / steps
        mx = int(w * ratio * 0.45)
        my = int(h * ratio * 0.45)
        a = int(255 * (ratio ** 1.6) * strength)
        draw.ellipse([mx, my, w - mx, h - my], fill=a)
    mask = mask.filter(ImageFilter.GaussianBlur(28))
    result = img.copy().convert('RGB')
    result.paste(overlay, mask=mask)
    return result

def radial_glow(w=800, h=800, inner=(22, 22, 32), spread=0.55):
    """Create a radial glow from center — gives product a background depth."""
    base = Image.new('RGB', (w, h), BG)
    glow = Image.new('RGB', (w, h), inner)
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    rw, rh = int(w * spread), int(h * spread)
    draw.ellipse([(w - rw) // 2, (h - rh) // 2, (w + rw) // 2, (h + rh) // 2], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(80))
    base.paste(glow, mask=mask)
    return base


# ─────────────────────────────────────────────────────────────
# IMAGE 1: HERO
# Use existing transparent PNG (BFS-processed, RGBA 800×524)
# Place on dark canvas with a subtle radial glow behind
# ─────────────────────────────────────────────────────────────
transparent = Image.open(os.path.join(DIR, 'wovo-product-transparent.png')).convert('RGBA')

canvas = radial_glow(800, 800, inner=(20, 20, 30), spread=0.65)
r, g, b, a = transparent.split()
# Boost product brightness slightly so dark bands are visible on dark bg
product_rgb = Image.merge('RGB', (r, g, b))
product_rgb = ImageEnhance.Brightness(product_rgb).enhance(1.20)
product_rgb = ImageEnhance.Contrast(product_rgb).enhance(1.08)
bright_transparent = Image.merge('RGBA', (*product_rgb.split(), a))

y_off = (800 - transparent.height) // 2  # 138px
canvas.paste(bright_transparent, (0, y_off), mask=a)
canvas = vignette(canvas, strength=0.35)
canvas.save(os.path.join(DIR, 'wovo-product-hero.png'), 'PNG', optimize=True)
print(f"Hero:      {os.path.getsize(os.path.join(DIR, 'wovo-product-hero.png'))//1024}KB")


# ─────────────────────────────────────────────────────────────
# IMAGE 2: SENSOR DETAIL  (raw_Sc21337 — green LED close-up)
# Crop: remove title (top 150px) and charts panel (right 315px)
# ─────────────────────────────────────────────────────────────
src = Image.open(os.path.join(DIR, 'raw_Sc21337691bf34929aea3d520e398f815e.jpg'))
crop = src.crop((0, 150, 485, 790))          # 485×640
crop = ImageEnhance.Contrast(crop).enhance(1.05)
img = place_on_dark(crop, pad=0.06)
img = vignette(img, strength=0.42)
img.save(os.path.join(DIR, 'wovo-clean-sensors.webp'), 'WEBP', quality=88)
print(f"Sensors:   {os.path.getsize(os.path.join(DIR, 'wovo-clean-sensors.webp'))//1024}KB")


# ─────────────────────────────────────────────────────────────
# IMAGE 3: LIFESTYLE / SLEEP  (raw_Sf82d6b — purple bedroom)
# Crop: remove black title banner AND icon overlay (top 275px total)
# ─────────────────────────────────────────────────────────────
src = Image.open(os.path.join(DIR, 'raw_Sf82d6b2021dc427ab9da3b54ae4564b42.jpg'))
crop = src.crop((0, 275, 800, 800))           # 800×525
crop = ImageEnhance.Contrast(crop).enhance(1.04)
# This is a full-width lifestyle shot — keep width, pad top/bottom
canvas = dark_canvas()
scale = 800 / crop.width
nh = int(crop.height * scale)
resized = crop.resize((800, nh), Image.LANCZOS)
y_off = (800 - nh) // 2
canvas.paste(resized, (0, y_off))
canvas = vignette(canvas, strength=0.40)
canvas.save(os.path.join(DIR, 'wovo-clean-lifestyle.webp'), 'WEBP', quality=88)
print(f"Lifestyle: {os.path.getsize(os.path.join(DIR, 'wovo-clean-lifestyle.webp'))//1024}KB")


# ─────────────────────────────────────────────────────────────
# IMAGE 4: WATERPROOF SHOT  (raw_S70eef — band on water splash)
# Crop: bottom-left region, text on the right so x:0-380
# ─────────────────────────────────────────────────────────────
src = Image.open(os.path.join(DIR, 'raw_S70eef5b39c724ee884c6db022e3ef868v.jpg'))
crop = src.crop((0, 415, 380, 755))           # 380×340
crop = ImageEnhance.Brightness(crop).enhance(1.06)
crop = ImageEnhance.Contrast(crop).enhance(1.10)
img = place_on_dark(crop, pad=0.07)
img = vignette(img, strength=0.38)
img.save(os.path.join(DIR, 'wovo-clean-waterproof.webp'), 'WEBP', quality=88)
print(f"Waterproof:{os.path.getsize(os.path.join(DIR, 'wovo-clean-waterproof.webp'))//1024}KB")


# Clean up temp preview
import pathlib
for f in ['_preview_water.jpg']:
    p = pathlib.Path(DIR) / f
    if p.exists(): p.unlink()

print("\nDone.")
