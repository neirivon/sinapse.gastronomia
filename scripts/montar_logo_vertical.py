#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter, ImageOps
import os

IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"
OUTPUT  = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

CANVAS = 1080
BG = (0, 0, 0, 255)
GAP = 24
SIDE_PAD = 80
TOP_PAD  = 80
BOT_PAD  = 80

# Destaques específicos do IFTM
IFTM_WIDTH_BOOST = 1.15         # deixa o IFTM ~15% mais largo que as outras
IFTM_STROKE_PX   = 2            # contorno branco (0 para desativar)
IFTM_SHARPEN     = True         # nitidez extra

def load_rgba(p): return Image.open(p).convert("RGBA")

def trim_alpha(im, thr=0):
    a = im.split()[-1]
    bbox = a.point(lambda t: 255 if t > thr else 0).getbbox()
    return im.crop(bbox) if bbox else im

def fit_width(im, w, resample=Image.Resampling.LANCZOS):
    ow, oh = im.size
    nh = max(1, round(oh * (w/ow)))
    return im.resize((int(w), nh), resample)

def add_white_stroke(im, stroke_px=2, alpha=220):
    if stroke_px <= 0: return im
    # Máscara (alpha)
    a = im.split()[-1]
    # Expande a máscara para criar “borda”
    outline = a.filter(ImageFilter.MaxFilter(stroke_px*2+1))
    blur = outline.filter(ImageFilter.GaussianBlur(0.7))
    stroke = Image.new("RGBA", im.size, (255,255,255,0))
    stroke.putalpha(blur.point(lambda v: min(alpha, v)))
    # Composita stroke por baixo do ícone
    out = Image.alpha_composite(stroke, im)
    return out

def unsharp_if_needed(im):
    # nitidez suave para ícones/flat
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))

def main():
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = trim_alpha(load_rgba(IMG_MID))
    bot = trim_alpha(load_rgba(IMG_BOT))

    content_w = CANVAS - 2*SIDE_PAD
    # largura base para mid/bot
    base_w = content_w
    # aplica boost no topo
    top_w = min(int(base_w * IFTM_WIDTH_BOOST), content_w)
    mid_w = base_w
    bot_w = base_w

    # primeiro, limite por altura disponível (vamos ajustar depois se passar)
    top = fit_width(top, top_w)
    mid = fit_width(mid, mid_w)
    bot = fit_width(bot, bot_w)

    # tratamentos do IFTM
    if IFTM_STROKE_PX > 0:
        top = add_white_stroke(top, IFTM_STROKE_PX)
    if IFTM_SHARPEN:
        top = unsharp_if_needed(top)

    ims = [top, mid, bot]

    total_h = sum(i.size[1] for i in ims) + GAP*2
    avail_h = CANVAS - TOP_PAD - BOT_PAD
    if total_h > avail_h:
        scale = avail_h / total_h
        ims = [i.resize((max(1,int(i.size[0]*scale)), max(1,int(i.size[1]*scale))),
                        Image.Resampling.LANCZOS) for i in ims]

    canvas = Image.new("RGBA", (CANVAS, CANVAS), BG)
    y = (CANVAS - (sum(i.size[1] for i in ims) + GAP*2))//2
    for idx, im in enumerate(ims):
        x = (CANVAS - im.size[0])//2
        canvas.paste(im, (x, y), im)
        y += im.size[1] + (GAP if idx < 2 else 0)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    canvas.save(OUTPUT, "PNG")
    print(f"✅ Poster pronto: {OUTPUT} ({CANVAS}x{CANVAS})")

if __name__ == "__main__":
    main()

