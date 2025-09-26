#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove halo/matte branco do SINAPSE e monta poster 1080x1080.
Requisitos: Pillow, numpy
    pip install pillow numpy
"""

from PIL import Image, ImageFilter
import numpy as np
import os

# === ENTRADAS ===
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"          # com halo branco
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# === SAÍDAS ===
MID_CLEAN = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse_clean.png"
OUTPUT    = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

# === PARAMETROS DO POSTER ===
CANVAS = 1080
BG = (0, 0, 0, 255)
GAP = 24
SIDE_PAD = 80
TOP_PAD  = 80
BOT_PAD  = 80

# Ajustes no IFTM para nitidez
IFTM_WIDTH_BOOST = 1.10
IFTM_STROKE_PX   = 2
IFTM_UNSHARP     = True

def load_rgba(p): return Image.open(p).convert("RGBA")

def trim_alpha(im, thr=0):
    a = im.split()[-1]
    bbox = a.point(lambda t: 255 if t > thr else 0).getbbox()
    return im.crop(bbox) if bbox else im

def fit_width(im, w):
    ow, oh = im.size
    nh = max(1, round(oh * (w/ow)))
    return im.resize((int(w), nh), Image.Resampling.LANCZOS)

def add_white_stroke(im, stroke_px=2, alpha=220):
    if stroke_px <= 0: return im
    a = im.split()[-1]
    outline = a.filter(ImageFilter.MaxFilter(stroke_px*2+1)).filter(ImageFilter.GaussianBlur(0.6))
    stroke = Image.new("RGBA", im.size, (255,255,255,0))
    stroke.putalpha(outline.point(lambda v: min(alpha, v)))
    return Image.alpha_composite(stroke, im)

def unsharp(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=2))

def remove_white_matte(im_rgba, bg=(255,255,255), alpha_shrink_px=1, alpha_cutoff=4):
    """
    Remove 'matte' branco de imagens com semi-transparências.
    Fórmula de dematte: C' = (C - (1-a)*bg) / a, para a>0.
    Também contrai 1px do canal alfa para eliminar franjas residuais.
    """
    im = im_rgba.convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    rgb = arr[..., :3]
    a   = arr[..., 3:4] / 255.0

    bg = np.array(bg, dtype=np.float32)[None, None, :]

    # Evita divisão por zero
    mask = a > 1e-6
    rgb_corr = np.zeros_like(rgb)
    rgb_corr[mask[...,0]] = np.clip((rgb[mask[...,0]] - (1.0 - a[mask[...,0]]) * bg) / a[mask[...,0]], 0, 255)

    # Onde a==0, mantém 0
    arr[..., :3] = rgb_corr
    # Reconstroi imagem
    im2 = Image.fromarray(arr.clip(0,255).astype(np.uint8), 'RGBA')

    # Contrai levemente o alfa para comer franja
    if alpha_shrink_px > 0:
        a = im2.split()[-1]
        a = a.filter(ImageFilter.MinFilter(alpha_shrink_px*2+1))
        # limpa ruídos quase transparentes
        a = a.point(lambda v: 0 if v < alpha_cutoff else v)
        im2.putalpha(a)

    return im2

def main():
    # 1) Corrige o SINAPSE (remove halo branco)
    mid_raw = load_rgba(IMG_MID)
    mid_clean = remove_white_matte(mid_raw, bg=(255,255,255), alpha_shrink_px=1)
    mid_clean = trim_alpha(mid_clean)
    os.makedirs(os.path.dirname(MID_CLEAN), exist_ok=True)
    mid_clean.save(MID_CLEAN)

    # 2) Monta poster com as três
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = mid_clean
    bot = trim_alpha(load_rgba(IMG_BOT))

    content_w = CANVAS - 2*SIDE_PAD
    top = fit_width(top, min(int(content_w*IFTM_WIDTH_BOOST), content_w))
    mid = fit_width(mid, content_w)
    bot = fit_width(bot, content_w)

    # Destaque do IFTM
    if IFTM_STROKE_PX > 0:
        top = add_white_stroke(top, IFTM_STROKE_PX)
    if IFTM_UNSHARP:
        top = unsharp(top)

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
    print(f"✅ Poster pronto (sem halo): {OUTPUT}")

if __name__ == "__main__":
    main()

