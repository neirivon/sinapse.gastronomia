#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ARQUIVO: /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/poster_keep_title_cut_subtitle.py
#
# Como executar:
#   python3 /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/poster_keep_title_cut_subtitle.py
#
# O que faz:
#   - Mantém o ÍCONE + “SINAPSE 2.0” e remove apenas o subtítulo do sinapse.png
#   - Salva o recorte como sinapse_title.png
#   - Gera pôster 1080×1080: IFTM (topo) + [ícone+SINAPSE 2.0] (meio) + GASTRONOMIA (base)

import os
import numpy as np
from PIL import Image, ImageFilter

# === Entradas (absolutos) ===
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"     # com título + subtítulo
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# === Saídas (absolutos) ===
SINAPSE_TITLE = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse_title.png"
OUTPUT        = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

# === Parâmetros do corte (ajuste fino se necessário) ===
SMOOTH_WIN   = 7      # largura da média móvel no perfil de linhas (ímpar)
DENSE_RATIO  = 0.35   # fração do máximo para considerar “denso” (0.30–0.45)
BOTTOM_PAD   = 10     # px extras abaixo do título para não cortar “descendentes”
SEARCH_FROM  = 0.20   # comece a procurar faixa densa depois de 20% da altura
SEARCH_TO    = 0.80   # e antes de 80% da altura (evita pegar o subtítulo no final)
FALLBACK_TOP_RATIO = 0.62  # fallback se não encontrar (mantém ~62% de cima)

# === Parâmetros do pôster ===
CANVAS = 1080
BG = (0,0,0,255)
GAP = 24
SIDE_PAD = 80
TOP_PAD  = 80
BOT_PAD  = 80

# Destaques do IFTM (opcional)
IFTM_STROKE_PX   = 2
IFTM_WIDTH_BOOST = 1.08
IFTM_UNSHARP     = True

def load_rgba(p): 
    return Image.open(p).convert("RGBA")

def trim_alpha(im, thr=0):
    a = im.split()[-1]
    bbox = a.point(lambda t: 255 if t > thr else 0).getbbox()
    return im.crop(bbox) if bbox else im

def fit_width(im, w):
    ow, oh = im.size
    nh = max(1, round(oh*(w/ow)))
    return im.resize((int(w), nh), Image.Resampling.LANCZOS)

def add_white_stroke(im, stroke_px=2, alpha=220):
    if stroke_px<=0: return im
    a = im.split()[-1]
    outline = a.filter(ImageFilter.MaxFilter(stroke_px*2+1)).filter(ImageFilter.GaussianBlur(0.6))
    stroke = Image.new("RGBA", im.size, (255,255,255,0))
    stroke.putalpha(outline.point(lambda v: min(alpha, v)))
    return Image.alpha_composite(stroke, im)

def unsharp(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=140, threshold=2))

def moving_avg(v, k):
    if k <= 1: return v
    pad = k//2
    vpad = np.pad(v, (pad, pad), mode='edge')
    ker = np.ones(k, dtype=np.float32) / k
    return np.convolve(vpad, ker, mode='valid')

def cut_subtitle_keep_title(mid_png: Image.Image) -> Image.Image:
    im = trim_alpha(mid_png)
    arr = np.array(im)              # H x W x 4
    alpha = arr[..., 3].astype(np.uint8)
    H, W = alpha.shape

    # perfil de opacidade por linha
    row_counts = (alpha > 10).sum(axis=1).astype(np.float32)
    # suaviza
    smooth = moving_avg(row_counts, SMOOTH_WIN)

    # busca maior faixa “densa” no miolo da imagem (onde está o título)
    y0 = int(H * SEARCH_FROM); y1 = int(H * SEARCH_TO)
    seg = smooth[y0:y1]
    if seg.size == 0:
        cut_y = int(H * FALLBACK_TOP_RATIO)
    else:
        thr = max(3.0, seg.max() * DENSE_RATIO)
        dense = (seg >= thr).astype(np.uint8)

        # pega o maior bloco contíguo de linhas densas
        best_len, best_start = 0, None
        i = 0
        while i < len(dense):
            if dense[i]:
                j = i
                while j < len(dense) and dense[j]:
                    j += 1
                run_len = j - i
                if run_len > best_len:
                    best_len, best_start = run_len, i
                i = j
            else:
                i += 1

        if best_start is None:
            cut_y = int(H * FALLBACK_TOP_RATIO)
        else:
            title_top    = y0 + best_start
            title_bottom = y0 + best_start + best_len - 1
            cut_y = min(H-1, title_bottom + BOTTOM_PAD)

    im2 = im.crop((0, 0, W, cut_y))
    return trim_alpha(im2)

def main():
    # Carrega
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = load_rgba(IMG_MID)
    bot = trim_alpha(load_rgba(IMG_BOT))

    # Corta apenas o subtítulo (mantém ícone + “SINAPSE 2.0”)
    mid_title = cut_subtitle_keep_title(mid)
    os.makedirs(os.path.dirname(SINAPSE_TITLE), exist_ok=True)
    mid_title.save(SINAPSE_TITLE)

    # Monta pôster 1080×1080
    content_w = CANVAS - 2*SIDE_PAD

    top = fit_width(top, min(int(content_w*IFTM_WIDTH_BOOST), content_w))
    if IFTM_STROKE_PX>0: top = add_white_stroke(top, IFTM_STROKE_PX)
    if IFTM_UNSHARP:     top = unsharp(top)

    mid_title = fit_width(mid_title, content_w)
    bot = fit_width(bot, content_w)

    ims = [top, mid_title, bot]
    total_h = sum(i.height for i in ims) + GAP*2
    avail_h = CANVAS - TOP_PAD - BOT_PAD
    if total_h > avail_h:
        s = avail_h / total_h
        ims = [im.resize((int(im.width*s), int(im.height*s)), Image.Resampling.LANCZOS) for im in ims]

    canvas = Image.new("RGBA", (CANVAS, CANVAS), BG)
    y = (CANVAS - (sum(i.height for i in ims) + GAP*2)) // 2
    for idx, im in enumerate(ims):
        x = (CANVAS - im.width) // 2
        canvas.paste(im, (x, y), im)
        y += im.height + (GAP if idx < 2 else 0)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    canvas.save(OUTPUT, "PNG")
    print(f"✅ Título salvo (sem subtítulo): {SINAPSE_TITLE}")
    print(f"✅ Pôster pronto: {OUTPUT}")

if __name__ == "__main__":
    main()

