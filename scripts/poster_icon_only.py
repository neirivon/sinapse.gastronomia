#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ARQUIVO: /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/poster_keep_title_cut_subtitle.py
#
# Como executar:
#   python3 /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/poster_keep_title_cut_subtitle.py
#
# O que faz:
#   - Carrega sinapse.png (ícone + "SINAPSE 2.0" + subtítulo)
#   - Corta APENAS o subtítulo (mantém ícone + "SINAPSE 2.0")
#   - Salva sinapse_title.png (limpo, sem subtítulo)
#   - Gera pôster 1080×1080: IFTM (topo) + [ícone+SINAPSE 2.0] (meio) + GASTRONOMIA (base)

import os
import numpy as np
from PIL import Image, ImageFilter

# === Entradas (caminhos absolutos) ===
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"       # com título e subtítulo
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# === Saídas (caminhos absolutos) ===
SINAPSE_TITLE = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse_title.png"
OUTPUT        = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

# === Parâmetros do pôster ===
CANVAS = 1080
BG = (0,0,0,255)
GAP = 24
SIDE_PAD = 80
TOP_PAD  = 80
BOT_PAD  = 80

# Caso o detector automático não encontre o “vão” entre título e subtítulo,
# corta mantendo o TOP_RATIO da altura (ex.: 0.60 mantém ~60% de cima).
FALLBACK_TOP_RATIO = 0.62  # ajuste fino se necessário

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

def cut_subtitle_keep_title(mid_png: Image.Image) -> Image.Image:
    """
    Detecta o 'vão' horizontal (linhas com quase nenhum pixel opaco)
    entre o título ('SINAPSE 2.0') e o subtítulo, e corta abaixo dele.
    Se não encontrar, usa FALLBACK_TOP_RATIO.
    """
    im = trim_alpha(mid_png)
    arr = np.array(im)                      # H x W x 4
    alpha = arr[..., 3]                     # H x W
    H, W = alpha.shape

    # Conta quantos pixels 'opacos' há por linha (alpha > 10)
    row_counts = (alpha > 10).sum(axis=1)

    # Procura um vale de 'quase nada' de opaco (vão) na metade de baixo
    start = int(H * 0.35)      # começa a procurar 35% da altura
    end   = int(H * 0.85)      # até ~85%
    threshold = max(3, int(W * 0.01))  # linha com poucos pixels opacos
    gap_idx = None
    run = 0
    min_run = 2                 # pelo menos 2 linhas "vazias" seguidas para considerar vão

    for y in range(start, end):
        if row_counts[y] <= threshold:
            run += 1
            if run >= min_run:
                gap_idx = y - run//2       # pega o meio do vão
                break
        else:
            run = 0

    if gap_idx is None:
        # fallback por proporção
        cut_y = int(H * FALLBACK_TOP_RATIO)
    else:
        # sobe um pouquinho para garantir que não corte o título
        cut_y = max(1, gap_idx - 2)

    # Faz o corte e reapara transparências
    im2 = im.crop((0, 0, W, cut_y))
    im2 = trim_alpha(im2)
    return im2

def main():
    # 1) Carrega
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = load_rgba(IMG_MID)
    bot = trim_alpha(load_rgba(IMG_BOT))

    # 2) Corta somente o subtítulo (mantém ícone + 'SINAPSE 2.0')
    mid_title = cut_subtitle_keep_title(mid)
    os.makedirs(os.path.dirname(SINAPSE_TITLE), exist_ok=True)
    mid_title.save(SINAPSE_TITLE)

    # 3) Dimensiona e monta pôster 1080×1080
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

