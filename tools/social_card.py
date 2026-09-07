"""Build the 1200x630 social card the site had no image for.

Sharing whaletailworks.net anywhere — X, Discord, Facebook, Slack — produced a
bare link with no preview, because the page carried no Open Graph or Twitter
card tags and there was no image at the right aspect to point them at. This
composes one from art already on the site: the two games side by side under the
studio wordmark.

  python tools/social_card.py
"""
import os
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / 'img'
W, H = 1200, 630
OUT = IMG / 'social_card.jpg'


def cover(im, w, h):
    """Scale to fill w x h and centre-crop."""
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


card = Image.new('RGB', (W, H), (8, 14, 26))

# the two games, one either side, meeting on a soft seam
left = cover(Image.open(IMG / 'xeno_hero.jpg').convert('RGB'), W // 2, H)
right = cover(Image.open(IMG / 'gw_shot_wyrm.jpg').convert('RGB'), W // 2, H)
card.paste(left, (0, 0))
card.paste(right, (W // 2, 0))

# push both back so the wordmark reads: darken, then a vignette toward centre
card = Image.blend(card, Image.new('RGB', (W, H), (7, 13, 24)), 0.52)
scrim = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(scrim)
d.ellipse((-W * 0.25, -H * 0.45, W * 1.25, H * 1.45), fill=170)
scrim = scrim.filter(ImageFilter.GaussianBlur(90))
card = Image.composite(Image.new('RGB', (W, H), (6, 12, 22)), card, scrim)

# a hairline where the two games meet, so it reads as deliberate
d = ImageDraw.Draw(card)
d.line([(W // 2, 0), (W // 2, H)], fill=(58, 92, 120), width=2)

# the studio wordmark, centred
word = Image.open(IMG / 'logo_word.png').convert('RGBA')
ww = int(W * 0.56)
word = word.resize((ww, int(word.height * ww / word.width)), Image.LANCZOS)
card.paste(word, ((W - ww) // 2, int(H * 0.34)), word)

# the whale above it
whale = Image.open(IMG / 'logo_whale.png').convert('RGBA')
hw = int(W * 0.17)
whale = whale.resize((hw, int(whale.height * hw / whale.width)), Image.LANCZOS)
card.paste(whale, ((W - hw) // 2, int(H * 0.13)), whale)

# the two titles under the wordmark, drawn as plates so no font file is needed
d = ImageDraw.Draw(card, 'RGBA')
try:
    from PIL import ImageFont
    f = ImageFont.truetype('seguisb.ttf', 30)
except Exception:
    f = None
label = 'XENODEX   ·   THE GREENWOOD WAY'
if f:
    bb = d.textbbox((0, 0), label, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = (W - tw) // 2, int(H * 0.66)
    d.rounded_rectangle((x - 26, y - 16, x + tw + 26, y + th + 18), 22,
                        fill=(10, 20, 34, 205), outline=(70, 116, 148, 210), width=2)
    d.text((x, y), label, font=f, fill=(214, 234, 246))
else:
    print('  note: no TrueType font found — card built without the title plate')

card.save(OUT, 'JPEG', quality=88, optimize=True, progressive=True)
print('%s  %dx%d  %.0f KB' % (OUT.name, W, H, os.path.getsize(OUT) / 1024))
