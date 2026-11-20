#!/usr/bin/env python3
"""Generate the application icon and the installer artwork.

    python3 resources/make_art.py

Creates:
    resources/app.ico        multi-resolution Windows icon (16..256 px)
    resources/app.png        256 px PNG (e.g. for Linux desktop files)
    installer/welcome.bmp    164x314 welcome/finish page image (NSIS)
    installer/header.bmp     150x57 page header image (NSIS)

Requires Pillow (pip install pillow).
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SS = 4  # supersampling factor for smooth edges


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def vertical_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGBA", size)
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, h - 1)) + (255,))
    return img


def star_points(cx, cy, r_out, r_in, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_motif(size):
    """The logo: overlapping translucent cards and a star (like the drawing window)."""
    s = size * SS
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))

    # rounded blue background tile
    bg = vertical_gradient((s, s), (66, 133, 244), (25, 60, 150))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.2), fill=255)
    layer.paste(bg, (0, 0), mask)

    # three translucent "windows"
    cards = [((255, 82, 82), 0.14, 0.22), ((76, 175, 80), 0.27, 0.36), ((255, 255, 255), 0.40, 0.50)]
    for colour, x, y in cards:
        over = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(over)
        box = [s * x, s * y, s * (x + 0.46), s * (y + 0.34)]
        d.rounded_rectangle(box, radius=int(s * 0.05), fill=colour + (170,),
                            outline=(255, 255, 255, 230), width=max(1, s // 64))
        layer = Image.alpha_composite(layer, over)

    # yellow star top-right
    over = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    d.polygon(star_points(s * 0.72, s * 0.27, s * 0.20, s * 0.085), fill=(255, 202, 40, 255),
              outline=(200, 120, 0, 255))
    layer = Image.alpha_composite(layer, over)

    return layer.resize((size, size), Image.LANCZOS)


def make_icon():
    big = draw_motif(256)
    res = ROOT / "resources"
    big.save(res / "app.png")
    sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
    # render every size separately for crisp small icons
    frames = [draw_motif(n) for n in sizes]
    frames[-1].save(res / "app.ico", sizes=[(n, n) for n in sizes], append_images=frames[:-1])


def make_installer_bitmaps():
    inst = ROOT / "installer"
    inst.mkdir(exist_ok=True)

    # welcome / finish page: 164x314, logo on a gradient
    w, h = 164, 314
    img = vertical_gradient((w, h), (30, 70, 160), (12, 30, 80))
    d = ImageDraw.Draw(img)
    for i in range(8):  # subtle decorative circles
        r = 30 + i * 22
        d.ellipse([w - r, h - r, w + r, h + r], outline=(255, 255, 255, 18 + i * 3), width=2)
    logo = draw_motif(112)
    img.alpha_composite(logo, ((w - 112) // 2, 60))
    img.convert("RGB").save(inst / "welcome.bmp")

    # header: 150x57, logo right-aligned on white
    w, h = 150, 57
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    logo = draw_motif(48)
    img.alpha_composite(logo, (w - 48 - 6, (h - 48) // 2))
    img.convert("RGB").save(inst / "header.bmp")


if __name__ == "__main__":
    make_icon()
    make_installer_bitmaps()
    print("artwork written")
