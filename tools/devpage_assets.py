r"""Build the Google Play developer-page images for Whale Tail Works.

Play requires, for the public developer page:
  developer icon   512 x 512    JPEG or 24-bit PNG, NOT transparent, <= 1 MB
  header image    4096 x 2304   JPEG or 24-bit PNG, NOT transparent, <= 1 MB

⚠ "Not transparent" is the trap: logo_whale.png and logo_word.png are both RGBA
with real alpha. Uploading them directly fails. Everything here is composited onto
an opaque field and saved as RGB.

⚠ 1 MB at 4096x2304 is tight — that is 9.4 megapixels. It only fits because the art
is mostly dark; the starfield is generated at full resolution rather than upscaled
from the 1024px site art, which would be visibly soft at 4K.

⚠ Developer-page headers get cropped differently across devices, so the logo and
wordmark stay inside the central band and well clear of the edges.

Run:  py tools/devpage_assets.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "img")
OUT = os.path.join(ROOT, "playstore")
os.makedirs(OUT, exist_ok=True)

BG = (7, 11, 17)          # the site's --bg
CYAN = (62, 230, 255)


def starfield(w, h, seed=7, density=0.00030):
    """Stars generated at OUTPUT resolution so they stay pin-sharp at 4K."""
    r = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), dtype=float)
    # deep-space gradient: a touch of blue at the top, near-black at the bottom
    g = np.linspace(1.0, 0.35, h)[:, None, None]
    a += np.array([[[10.0, 15.0, 26.0]]]) * g
    n = int(w * h * density)
    xs = r.integers(0, w, n)
    ys = r.integers(0, h, n)
    mag = r.random(n) ** 3.2                      # mostly faint, a few bright
    for i in range(n):
        v = 40 + mag[i] * 215
        tint = 1.0 + 0.25 * (r.random() - 0.5)
        a[ys[i], xs[i]] += [v * 0.92, v * 0.97, v * tint]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    glow = img.filter(ImageFilter.GaussianBlur(w / 420.0))
    img = Image.blend(img, glow, 0.45)
    return Image.blend(img, img.filter(ImageFilter.GaussianBlur(1.1)), 0.30)


def nebula(w, h, seed=11, strength=0.30):
    """A soft cyan wash so the field is not a flat black rectangle."""
    r = np.random.default_rng(seed)
    small = Image.fromarray((r.random((10, 18)) * 255).astype(np.uint8))
    m = np.asarray(small.resize((w, h), Image.BICUBIC)).astype(float) / 255.0
    m = np.clip(m - 0.52, 0, 1) ** 1.6
    a = np.zeros((h, w, 3))
    for c in range(3):
        a[..., c] = m * CYAN[c] * strength
    return a


def paste_fit(base, overlay_path, target_w, cx, cy):
    ov = Image.open(os.path.join(IMG, overlay_path)).convert("RGBA")
    scale = target_w / ov.width
    ov = ov.resize((int(ov.width * scale), int(ov.height * scale)), Image.LANCZOS)
    base.paste(ov, (int(cx - ov.width / 2), int(cy - ov.height / 2)), ov)
    return base


def save_under(img, path, limit=1_000_000):
    """Step quality down until it fits Play's 1 MB ceiling."""
    for q in (92, 88, 84, 80, 76, 72, 68, 64):
        img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(path) <= limit:
            return q, os.path.getsize(path)
    return q, os.path.getsize(path)


# ── developer icon, 512 x 512 ───────────────────────────────────────────────
S = 512
icon = Image.fromarray(
    np.clip(np.asarray(starfield(S, S, seed=3, density=0.00018)).astype(float)
            + nebula(S, S, seed=5, strength=0.22), 0, 255).astype(np.uint8))
# a soft cyan pool behind the whale so it reads at small sizes
pool = Image.new("RGB", (S, S), (0, 0, 0))
pa = np.zeros((S, S, 3))
yy, xx = np.mgrid[0:S, 0:S]
d = np.exp(-(((xx - S / 2) / (S * 0.42)) ** 2 + ((yy - S / 2) / (S * 0.34)) ** 2) * 1.4)
for c in range(3):
    pa[..., c] = d * CYAN[c] * 0.16
icon = Image.fromarray(np.clip(np.asarray(icon).astype(float) + pa, 0, 255).astype(np.uint8))
# ⚠ CIRCLE-SAFE. Play frequently masks developer icons to a circle, so anything
# outside the inscribed circle is clipped — at 90% width the whale lost its nose
# and the tip of its tail. 0.74 keeps the whole silhouette inside the mask.
icon = paste_fit(icon, "logo_whale.png", int(S * 0.74), S / 2, S / 2 - 2)
q, sz = save_under(icon.convert("RGB"), os.path.join(OUT, "developer_icon_512.jpg"))
print("developer_icon_512.jpg   512x512    q=%d  %6.0f KB" % (q, sz / 1024))

# ── header, 4096 x 2304 ─────────────────────────────────────────────────────
W, H = 4096, 2304
hdr = Image.fromarray(
    np.clip(np.asarray(starfield(W, H, seed=17, density=0.00026)).astype(float)
            + nebula(W, H, seed=23, strength=0.34), 0, 255).astype(np.uint8))
# central content, kept well inside the crop-safe band
hdr = paste_fit(hdr, "logo_whale.png", int(W * 0.42), W / 2, H * 0.42)
hdr = paste_fit(hdr, "logo_word.png", int(W * 0.36), W / 2, H * 0.76)
q, sz = save_under(hdr.convert("RGB"), os.path.join(OUT, "developer_header_4096.jpg"))
print("developer_header_4096.jpg 4096x2304 q=%d  %6.0f KB" % (q, sz / 1024))
print("\n-> %s" % OUT)
