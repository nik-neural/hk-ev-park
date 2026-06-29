#!/usr/bin/env python3
"""Generate PWA PNG icons from vector specs."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent / "icons"
BG = (15, 23, 42, 255)
GREEN = (5, 150, 105, 255)
GREEN_DARK = (4, 120, 87, 255)
WHITE = (255, 255, 255, 255)


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)
    pad = int(size * 0.094)
    radius = int(size * 0.1875)
    rounded_rect(draw, (pad, pad, size - pad, size - pad), radius, GREEN)

    # subtle inner highlight
    inset = int(size * 0.12)
    rounded_rect(draw, (inset, inset, size - inset, size - inset), int(radius * 0.85), GREEN_DARK)

    # lightning bolt
    cx, cy = size * 0.5, size * 0.46
    s = size
    bolt = [
        (cx + s * 0.04, cy - s * 0.20),
        (cx - s * 0.13, cy + s * 0.04),
        (cx - s * 0.02, cy + s * 0.04),
        (cx - s * 0.08, cy + s * 0.22),
        (cx + s * 0.15, cy - s * 0.02),
        (cx + s * 0.03, cy - s * 0.02),
    ]
    draw.polygon(bolt, fill=WHITE)

    # parking badge
    badge_r = int(size * 0.10)
    bx, by = int(size * 0.75), int(size * 0.75)
    draw.ellipse((bx - badge_r, by - badge_r, bx + badge_r, by + badge_r), fill=(15, 23, 42, 180))
    font_size = max(12, int(size * 0.11))
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    draw.text((bx, by), "P", fill=WHITE, font=font, anchor="mm")

    return img


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for name, size in [("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)]:
        draw_icon(size).save(ROOT / name, optimize=True)
        print("wrote", ROOT / name)


if __name__ == "__main__":
    main()