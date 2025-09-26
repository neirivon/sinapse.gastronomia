#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ARQUIVO: /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/export_assets_bot.py
#
# Como executar:
#   python3 /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/export_assets_bot.py
#
# Entradas (existentes no projeto):
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png      (seu arquivo editado no GIMP, com subtítulo removido)
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png
#
# Saídas geradas:
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/derivatives/avatar_gastronomia_512.png     (PNG, fundo preto)
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/derivatives/avatar_sinapse_512.png         (PNG, fundo preto) [opcional]
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/derivatives/banner_1600x400.png            (PNG, fundo preto)
#   /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/derivatives/sticker_gastronomia_512.png    (PNG, transparente)
#
# Observações:
# - O sticker é gerado com o ÍCONE da Gastronomia (sem a palavra). O corte do ícone
#   usa uma fração configurável da largura do arquivo (ICON_FRACTION_GASTRO). Ajuste
#   se precisar (0.25–0.35 costuma funcionar bem).
# - O banner organiza: [IFTM]  |  [SINAPSE 2.0]  |  [GASTRONOMIA], com margens.
# - Avatar 512×512 usa safe-area circular (elemento centralizado e com respiro).

from PIL import Image, ImageFilter
import os

# ======= Entradas =======
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# ======= Saídas =======
OUT_DIR = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/derivatives"
AVATAR_GASTRO = f"{OUT_DIR}/avatar_gastronomia_512.png"
AVATAR_SINAPSE = f"{OUT_DIR}/avatar_sinapse_512.png"
BANNER_1600x400 = f"{OUT_DIR}/banner_1600x400.png"
STICKER_GASTRO = f"{OUT_DIR}/sticker_gastronomia_512.png"

# ======= Parâmetros =======
# Avatar
AVATAR_SIZE = 512
AVATAR_BG = (0, 0, 0, 255)      # Telegram “achata” fundo; preto funciona bem
SAFE_MARGIN = 64                # respiro interno (px) para não cortar no círculo

# Banner
BANNER_W, BANNER_H = 1600, 400
BANNER_BG = (0, 0, 0, 255)
BANNER_SIDE_PAD = 80
BANNER_VPAD = 40
BANNER_GAP = 60

# Sticker (transparente)
STICKER_SIZE = 512
ICON_FRACTION_GASTRO = 0.30     # fração da largura à esquerda que contém o ícone (ajuste fino: 0.25–0.35)

def load_rgba(p): 
    return Image.open(p).convert("RGBA")

def trim_alpha(im, thr=0):
    a = im.split()[-1]
    bbox = a.point(lambda t: 255 if t > thr else 0).getbbox()
    return im.crop(bbox) if bbox else im

def fit_within_box(im, max_w, max_h):
    w, h = im.size
    scale = min(max_w / w, max_h / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)

def center_paste(canvas, im):
    x = (canvas.size[0] - im.size[0]) // 2
    y = (canvas.size[1] - im.size[1]) // 2
    canvas.paste(im, (x, y), im)

def ensure_outdir():
    os.makedirs(OUT_DIR, exist_ok=True)

def make_avatar_from_source(src_rgba, out_path):
    # recorta bordas transparentes e centraliza no quadrado
    src = trim_alpha(src_rgba)
    canvas = Image.new("RGBA", (AVATAR_SIZE, AVATAR_SIZE), AVATAR_BG)
    # área útil (safe area)
    usable = AVATAR_SIZE - 2 * SAFE_MARGIN
    fitted = fit_within_box(src, usable, usable)
    center_paste(canvas, fitted)
    canvas.save(out_path)

def make_banner(ifrm, mid, bot):
    # recorta bordas transparentes
    a = trim_alpha(ifrm)
    b = trim_alpha(mid)
    c = trim_alpha(bot)

    # altura útil no banner
    usable_h = BANNER_H - 2 * BANNER_VPAD
    # larguras alvo proporcionais (leve destaque para o meio)
    a = fit_within_box(a, (BANNER_W - 2*BANNER_SIDE_PAD - 2*BANNER_GAP) * 0.25, usable_h)
    b = fit_within_box(b, (BANNER_W - 2*BANNER_SIDE_PAD - 2*BANNER_GAP) * 0.50, usable_h)
    c = fit_within_box(c, (BANNER_W - 2*BANNER_SIDE_PAD - 2*BANNER_GAP) * 0.25, usable_h)

    # calcula posições
    canvas = Image.new("RGBA", (BANNER_W, BANNER_H), BANNER_BG)
    x = BANNER_SIDE_PAD
    y_a = (BANNER_H - a.size[1]) // 2
    canvas.paste(a, (x, y_a), a)

    x += a.size[0] + BANNER_GAP
    y_b = (BANNER_H - b.size[1]) // 2
    canvas.paste(b, (x, y_b), b)

    x += b.size[0] + BANNER_GAP
    y_c = (BANNER_H - c.size[1]) // 2
    canvas.paste(c, (x, y_c), c)

    canvas.save(BANNER_1600x400)

def make_sticker_gastro(bot_rgba):
    # recorta bordas e depois corta só a faixa da esquerda (ícone)
    full = trim_alpha(bot_rgba)
    w, h = full.size
    icon_w = max(1, int(w * ICON_FRACTION_GASTRO))
    icon = full.crop((0, 0, icon_w, h))
    icon = trim_alpha(icon)  # tira sobra de transparência após o crop

    # Encaixa no 512×512 transparente
    canvas = Image.new("RGBA", (STICKER_SIZE, STICKER_SIZE), (0, 0, 0, 0))
    fitted = fit_within_box(icon, STICKER_SIZE - 32, STICKER_SIZE - 32)  # 16 px de folga nas bordas
    center_paste(canvas, fitted)
    canvas.save(STICKER_GASTRO)

def main():
    ensure_outdir()

    # Carrega fontes
    iftm = load_rgba(IMG_TOP)
    sinapse = load_rgba(IMG_MID)      # já editado por você no GIMP
    gastro = load_rgba(IMG_BOT)

    # 1) Avatares 512×512
    # 1a) Avatar preferido: Gastronomia (ícone + palavra, centralizado)
    make_avatar_from_source(gastro, AVATAR_GASTRO)
    # 1b) Avatar alternativo: Ícone SINAPSE
    #    -> aqui recortamos só a área do ícone à esquerda (25–30% da largura total)
    w_mid, h_mid = sinapse.size
    icon_w = int(w_mid * 0.28)
    sinapse_icon = trim_alpha(sinapse.crop((0, 0, icon_w, h_mid)))
    make_avatar_from_source(sinapse_icon, AVATAR_SINAPSE)

    # 2) Banner 1600×400
    make_banner(iftm, sinapse, gastro)

    # 3) Sticker 512×512 (ícone Gastronomia transparente)
    make_sticker_gastro(gastro)

    print("✅ Export concluído:")
    print(" -", AVATAR_GASTRO)
    print(" -", AVATAR_SINAPSE)
    print(" -", BANNER_1600x400)
    print(" -", STICKER_GASTRO)

if __name__ == "__main__":
    main()

