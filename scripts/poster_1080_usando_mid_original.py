#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ARQUIVO: /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/poster_1080_usando_mid_original.py
#
# Como executar:
#   python3 /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/poster_1080_usando_mid_original.py
#
# O que faz:
#   - Carrega as 3 imagens originais (sem alterar o conteúdo):
#       topo: IFTM_360.png
#       meio: sinapse.png (o seu arquivo já editado no GIMP)
#       base: Gastronomia.png
#   - Remove apenas as BORDAS TRANSPARENTES de cada uma (trim)
#   - Redimensiona para caber com proporção preservada
#   - Empilha numa arte 1080×1080 com fundo preto (ideal p/ Telegram)
#   - Salva em: /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png

from PIL import Image, ImageFilter
import os

# === Entradas (caminhos absolutos) ===
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"       # <- SEU ARQUIVO EDITADO
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# === Saída ===
OUTPUT  = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

# === Layout (ajuste fino) ===
CANVAS = 1080                   # 1080 × 1080
BG = (0, 0, 0, 255)             # fundo preto opaco
SIDE_PAD = 80                   # margem lateral
TOP_PAD  = 80                   # margem superior
BOT_PAD  = 80                   # margem inferior
GAP = 24                        # espaço fixo entre as três logos

# Destaque opcional no IFTM (deixa mais nítido no preto)
IFTM_STROKE_PX   = 2            # 0 para desativar contorno branco
IFTM_WIDTH_BOOST = 1.08         # 1.00 = sem boost; >1 deixa o topo levemente maior
IFTM_UNSHARP     = True         # nitidez extra no IFTM

def load_rgba(p): 
    return Image.open(p).convert("RGBA")

def trim_alpha(im, thr=0):
    """Corta bordas 100% transparentes sem mexer no conteúdo."""
    a = im.split()[-1]
    bbox = a.point(lambda t: 255 if t > thr else 0).getbbox()
    return im.crop(bbox) if bbox else im

def fit_width(im, w):
    """Redimensiona pela largura, mantendo proporção."""
    ow, oh = im.size
    if ow == w: 
        return im
    nh = max(1, round(oh * (w/ow)))
    return im.resize((w, nh), Image.Resampling.LANCZOS)

def add_white_stroke(im, stroke_px=2, alpha=220):
    """Halo branco sutil p/ destacar no fundo preto."""
    if stroke_px <= 0: 
        return im
    a = im.split()[-1]
    outline = a.filter(ImageFilter.MaxFilter(stroke_px*2+1)).filter(ImageFilter.GaussianBlur(0.6))
    stroke = Image.new("RGBA", im.size, (255,255,255,0))
    stroke.putalpha(outline.point(lambda v: min(alpha, v)))
    return Image.alpha_composite(stroke, im)

def unsharp(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=140, threshold=2))

def main():
    # Carrega e remove bordas transparentes
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = trim_alpha(load_rgba(IMG_MID))   # usa seu sinapse.png como está
    bot = trim_alpha(load_rgba(IMG_BOT))

    # Largura útil (sem margens)
    content_w = CANVAS - 2*SIDE_PAD

    # Topo com leve destaque
    top = fit_width(top, min(int(content_w*IFTM_WIDTH_BOOST), content_w))
    if IFTM_STROKE_PX > 0:
        top = add_white_stroke(top, IFTM_STROKE_PX)
    if IFTM_UNSHARP:
        top = unsharp(top)

    # Meio e base ocupam a largura útil (ajuste automático se não couber em altura)
    mid = fit_width(mid, content_w)
    bot = fit_width(bot, content_w)

    # Se a soma das alturas + gaps não couber, escala tudo proporcionalmente
    blocks = [top, mid, bot]
    total_h = sum(b.size[1] for b in blocks) + GAP*2
    avail_h = CANVAS - TOP_PAD - BOT_PAD
    if total_h > avail_h:
        s = avail_h / total_h
        blocks = [b.resize((max(1,int(b.size[0]*s)), max(1,int(b.size[1]*s))), Image.Resampling.LANCZOS) for b in blocks]

    # Monta canvas 1080 × 1080
    canvas = Image.new("RGBA", (CANVAS, CANVAS), BG)
    y = (CANVAS - (sum(b.size[1] for b in blocks) + GAP*2)) // 2
    for i, b in enumerate(blocks):
        x = (CANVAS - b.size[0]) // 2
        canvas.paste(b, (x, y), b)
        y += b.size[1] + (GAP if i < len(blocks)-1 else 0)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    canvas.save(OUTPUT, "PNG")
    print(f"✅ Pôster pronto: {OUTPUT}  ({CANVAS}x{CANVAS})")

if __name__ == "__main__":
    main()

