#!/usr/bin/env python3
"""
images.py — shared helper for article featured images.

Strategy (best-effort, never fatal):
  1. Try to generate a related image with the Gemini image model.
  2. If that fails for ANY reason (SDK/model/rate limit/offline), fall back to
     a clean branded placeholder rendered locally with Pillow.
Either way we always end up with a >=1200px-wide JPEG and alt text, so the
build never breaks and every article has a valid featured image + og:image.
"""
import io, os, re, base64, pathlib, hashlib

ROOT     = pathlib.Path(__file__).parent
IMG_DIR  = ROOT / "static" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 1200, 675           # 16:9, safely over the 1200px minimum

# muted brand palette per category (bg1, bg2) for placeholders
CAT_COLORS = {
    "home-security": ((31, 95, 214), (17, 40, 92)),
    "vpn-privacy":   ((22, 130, 120), (12, 52, 66)),
    "streaming":     ((150, 60, 170), (48, 24, 78)),
    "telecom":       ((196, 110, 30), (74, 40, 18)),
    "_default":      ((31, 95, 214), (26, 31, 43)),
}


def image_prompt(title, category_name):
    return (
        f'Editorial news header illustration for an article titled "{title}". '
        f'Topic: {category_name}. Clean, modern, professional technology-news '
        f'style; conceptual and symbolic. Absolutely no text, no words, no logos, '
        f'no watermarks, no real brand marks. Wide 16:9 composition, muted blue '
        f'and slate colour palette, soft studio lighting.'
    )


def alt_text(title, category_name):
    return f"{category_name} illustration for: {title}"[:120]


# ---------------------------------------------------------------- post-process
def _save_jpeg(img_bytes, out_path):
    from PIL import Image
    im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = im.size
    # cover-crop to 16:9 then resize to 1200x675
    tr = TARGET_W / TARGET_H
    if w / h > tr:                       # too wide -> crop sides
        nw = int(h * tr); x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    else:                                # too tall -> crop top/bottom
        nh = int(w / tr); y = (h - nh) // 2
        im = im.crop((0, y, w, y + nh))
    im = im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=82, optimize=True, progressive=True)
    return True


# ---------------------------------------------------------------- gemini path
def _extract_image_bytes(resp):
    """Pull raw image bytes out of a google-genai response (several shapes)."""
    # interactions API shape
    oi = getattr(resp, "output_image", None)
    if oi is not None:
        data = getattr(oi, "data", None)
        if data:
            return base64.b64decode(data) if isinstance(data, str) else data
    # generate_content shape: candidates[].content.parts[].inline_data.data
    for cand in getattr(resp, "candidates", []) or []:
        content = getattr(cand, "content", None)
        for part in getattr(content, "parts", []) or []:
            inline = getattr(part, "inline_data", None) or getattr(part, "inlineData", None)
            data = getattr(inline, "data", None) if inline else None
            if data:
                return base64.b64decode(data) if isinstance(data, str) else data
    return None


def gen_gemini_image(client, model, prompt, out_path):
    """Return True if a real Gemini image was generated and saved."""
    if client is None:
        return False
    # Strategy A: newer Interactions API
    try:
        inter = client.interactions.create(model=model, input=prompt)
        b = _extract_image_bytes(inter)
        if b and _save_jpeg(b, out_path):
            return True
    except Exception as e:
        print(f"    [img] interactions path failed: {e}")
    # Strategy B: generate_content with image modality
    try:
        from google.genai import types
        cfg = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
        resp = client.models.generate_content(model=model, contents=prompt, config=cfg)
        b = _extract_image_bytes(resp)
        if b and _save_jpeg(b, out_path):
            return True
    except Exception as e:
        print(f"    [img] generate_content path failed: {e}")
    # Strategy C: bare generate_content (older SDKs)
    try:
        resp = client.models.generate_content(model=model, contents=prompt)
        b = _extract_image_bytes(resp)
        if b and _save_jpeg(b, out_path):
            return True
    except Exception as e:
        print(f"    [img] bare generate_content failed: {e}")
    return False


# ---------------------------------------------------------------- placeholder
def _font(size):
    from PIL import ImageFont
    for name in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Arialbd.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def placeholder_image(title, category_slug, category_name, out_path):
    from PIL import Image, ImageDraw
    c1, c2 = CAT_COLORS.get(category_slug, CAT_COLORS["_default"])
    im = Image.new("RGB", (TARGET_W, TARGET_H), c1)
    draw = ImageDraw.Draw(im)
    # vertical gradient
    for y in range(TARGET_H):
        t = y / TARGET_H
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (TARGET_W, y)], fill=(r, g, b))
    # category label
    lab = _font(30)
    draw.text((70, 70), category_name.upper(), font=lab, fill=(255, 255, 255))
    draw.line([(70, 118), (250, 118)], fill=(255, 255, 255), width=3)
    # wrapped title
    tf = _font(58)
    words, lines, cur = title.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=tf) > TARGET_W - 140 and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    lines.append(cur)
    lines = lines[:4]
    y = TARGET_H - 90 - len(lines) * 66
    for ln in lines:
        draw.text((70, y), ln, font=tf, fill=(255, 255, 255)); y += 66
    # brand mark
    bf = _font(26)
    draw.text((70, TARGET_H - 52), "TechShield News", font=bf, fill=(210, 220, 235))
    im.save(out_path, "JPEG", quality=85, optimize=True, progressive=True)
    return True


# ---------------------------------------------------------------- public entry
def ensure_image(post, cfg, client=None, force=False):
    """
    Make sure `post` has a featured image. Returns (rel_url, alt, kind).
    kind is 'ai' or 'placeholder'. Idempotent unless force=True.
    """
    slug = post["slug"]
    fname = f"{slug}.jpg"
    out = IMG_DIR / fname
    rel = f"/static/images/{fname}"
    cat_slug = post.get("category", "_default")
    cat_name = post.get("category_name", "Technology")
    alt = alt_text(post["title"], cat_name)

    existing_kind = post.get("image_kind")
    if out.exists() and not force and existing_kind == "ai":
        return rel, post.get("image_alt", alt), "ai"

    model = cfg["generation"].get("image_model", "gemini-3.1-flash-image")
    prompt = image_prompt(post["title"], cat_name)
    if gen_gemini_image(client, model, prompt, out):
        print(f"    [img] AI image -> {fname}")
        return rel, alt, "ai"

    # fallback
    try:
        placeholder_image(post["title"], cat_slug, cat_name, out)
        print(f"    [img] placeholder -> {fname}")
        return rel, alt, "placeholder"
    except Exception as e:
        print(f"    [img] placeholder failed ({e}); no image")
        return "", alt, "none"
