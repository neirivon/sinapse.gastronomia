#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os

# ====== ENTRADAS ======
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"  # usaremos só o ÍCONE à esquerda
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# ====== SAÍDA ======
OUTPUT  = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

# ====== CANVAS ======
CANVAS = 1080
BG = (0,0,0,255)
GAP = 24
SIDE_PAD = 80
TOP_PAD  = 80
BOT_PAD  = 80

# ====== TEXTO DO SINAPSE ======
TITLE = "SINAPSE 2.0"  # cuidado para não colar caractere Δ; aqui é A normal
SUBTITLE = ("Sistema Integrado Neuropsicopedagógico\n"
            "Ativo, Personalizado, Sustentável e Educacional")

# Gradiente título (roxo→azul)
GRAD_START = (106, 17, 203)   # #6A11CB
GRAD_END   = (37, 117, 252)   # #2575FC
SUBTITLE_COLOR = (235,235,235,255)

# ====== FONTES ======
# Se tiver Poppins/Montserrat no seu sistema, aponte aqui:
PREFERRED_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PREFERRED_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ====== PARÂMETROS ======
ICON_FRACTION = 0.26           # qual fração do PNG original é o ÍCONE (0.24~0.30)
ICON_TARGET_H = 120            # altura do bloco do meio base (será reescalado se faltar espaço)
SS = 4                         # supersampling 4× para texto ultra nítido
IFTM_WIDTH_BOOST = 1.08
IFTM_STROKE_PX   = 2
IFTM_UNSHARP     = True

def load_rgba(p): return Image.open(p).convert("RGBA")

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

def text_rgba_supersampled(text, font_path, size_px, fill="gradient", stroke_px=0):
    """Renderiza texto em 4× e reduz => bordas perfeitas."""
    size_hi = size_px * SS
    font = ImageFont.truetype(font_path, size_hi)
    # mede
    dummy = Image.new("L", (1,1), 0)
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0,0), text, font=font, align="left", spacing=4)
    w,h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    mask = Image.new("L", (w, h), 0)
    dm = ImageDraw.Draw(mask)
    dm.text((0,0), text, font=font, fill=255, align="left", spacing=4)
    # prepara cor/gradiente
    if fill=="gradient":
        grad = gradient_image((w,h), GRAD_START, GRAD_END).convert("RGBA")
        if stroke_px>0:
            dil = mask.filter(ImageFilter.MaxFilter(stroke_px*2*SS+1))
            edge = ImageChops.subtract(dil, mask)
            stroke = Image.new("RGBA", (w,h), (255,255,255,255))
            stroke.putalpha(edge)
            grad = Image.alpha_composite(stroke, grad)
        grad.putalpha(mask)
        img_hi = grad
    else:
        img_hi = Image.new("RGBA", (w,h), fill); img_hi.putalpha(mask)
    # reduz para tamanho final com LANCZOS
    out = img_hi.resize((max(1,w//SS), max(1,h//SS)), Image.Resampling.LANCZOS)
    return out

def paragraph_rgba_supersampled(text, font_path, size_px, color=(255,255,255,255), spacing=4):
    size_hi = size_px * SS
    font = ImageFont.truetype(font_path, size_hi)
    dummy = Image.new("L", (1,1), 0)
    d = ImageDraw.Draw(dummy)
    bbox = d.multiline_textbbox((0,0), text, font=font, spacing=spacing*SS, align="left")
    w,h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    mask = Image.new("L", (w,h), 0)
    dm = ImageDraw.Draw(mask)
    dm.multiline_text((0,0), text, font=font, fill=255, spacing=spacing*SS, align="left")
    img_hi = Image.new("RGBA", (w,h), color); img_hi.putalpha(mask)
    out = img_hi.resize((max(1,w//SS), max(1,h//SS)), Image.Resampling.LANCZOS)
    return out

def gradient_image(size, start, end):
    w,h = size
    t = np.linspace(0,1,w, dtype=np.float32)
    r = (1-t)*start[0] + t*end[0]
    g = (1-t)*start[1] + t*end[1]
    b = (1-t)*start[2] + t*end[2]
    rgb = np.stack([np.tile(r,(h,1)), np.tile(g,(h,1)), np.tile(b,(h,1))], axis=2).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")

from PIL import ImageChops

def build_mid_block(icon_src, max_width):
    """Recorta ícone e desenha 'SINAPSE 2.0' + subtítulo 100% novo (sem halo)"""
    icon_src = trim_alpha(icon_src)
    w,h = icon_src.size
    icon_w = int(w * ICON_FRACTION)
    icon = icon_src.crop((0,0,icon_w,h))
    # padroniza altura alvo
    scale = ICON_TARGET_H / icon.height
    icon = icon.resize((max(1,int(icon.width*scale)), ICON_TARGET_H), Image.Resampling.LANCZOS)

    # tamanhos proporcionais
    title_size = int(ICON_TARGET_H * 0.58)
    sub_size   = int(ICON_TARGET_H * 0.20)

    title_rgba = text_rgba_supersampled(TITLE, PREFERRED_BOLD, title_size, fill="gradient", stroke_px=1)
    sub_rgba   = paragraph_rgba_supersampled(SUBTITLE, PREFERRED_REG, sub_size, color=SUBTITLE_COLOR, spacing=4)

    gap = int(ICON_TARGET_H * 0.18)
    text_w = max(title_rgba.width, sub_rgba.width)
    block_w = icon.width + gap + text_w
    block_h = max(icon.height, title_rgba.height + 6 + sub_rgba.height)

    block = Image.new("RGBA", (block_w, block_h), (0,0,0,0))
    # posiciona
    x = 0
    y_icon = (block_h - icon.height)//2
    block.paste(icon, (x, y_icon), icon)
    x += icon.width + gap
    y_text = (block_h - (title_rgba.height + 6 + sub_rgba.height))//2
    block.paste(title_rgba, (x, y_text), title_rgba)
    block.paste(sub_rgba, (x, y_text + title_rgba.height + 6), sub_rgba)

    # garante largura máxima
    if block.width > max_width:
        s = max_width / block.width
        block = block.resize((int(block.width*s), int(block.height*s)), Image.Resampling.LANCZOS)

    return block

def main():
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = load_rgba(IMG_MID)
    bot = trim_alpha(load_rgba(IMG_BOT))

    content_w = CANVAS - 2*SIDE_PAD

    # topo com leve destaque
    top = fit_width(top, min(int(content_w*IFTM_WIDTH_BOOST), content_w))
    if IFTM_STROKE_PX>0: top = add_white_stroke(top, IFTM_STROKE_PX)
    if IFTM_UNSHARP:     top = unsharp(top)

    # meio reconstruído
    mid_block = build_mid_block(mid, content_w)

    # base
    bot = fit_width(bot, content_w)

    ims = [top, mid_block, bot]
    total_h = sum(i.size[1] for i in ims) + GAP*2
    avail_h = CANVAS - TOP_PAD - BOT_PAD
    if total_h > avail_h:
        s = avail_h/total_h
        ims = [i.resize((int(i.width*s), int(i.height*s)), Image.Resampling.LANCZOS) for i in ims]

    canvas = Image.new("RGBA", (CANVAS, CANVAS), BG)
    y = (CANVAS - (sum(i.height for i in ims) + GAP*2))//2
    for idx, im in enumerate(ims):
        x = (CANVAS - im.width)//2
        canvas.paste(im, (x, y), im)
        y += im.height + (GAP if idx<2 else 0)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    canvas.save(OUTPUT, "PNG")
    print(f"✅ Poster 1080 gerado sem halo e com texto nítido: {OUTPUT}")

if __name__ == "__main__":
    main()

