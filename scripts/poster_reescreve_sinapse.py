#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, numpy as np

# === ENTRADAS ===
IMG_TOP = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/IFTM_360.png"
IMG_MID = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"   # vamos usar só o ícone (lado esquerdo)
IMG_BOT = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/Gastronomia.png"

# === SAÍDAS ===
OUTPUT  = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/POSTER_TELEGRAM_1080.png"

# === CANVAS ===
CANVAS = 1080
BG = (0,0,0,255)
GAP = 24
SIDE_PAD = 80
TOP_PAD = 80
BOT_PAD = 80

# === TEXTO SINAPSE ===
TITLE = "SINAPSE 2.0"
SUBTITLE = "Sistema Integrado Neuropsicopedagógico\nAtivo, Personalizado, Sustentável e Educacional"
# Cores do gradiente (roxo → azul)
GRAD_START = (106, 17, 203)   # #6A11CB
GRAD_END   = (37, 117, 252)   # #2575FC
STROKE_PX = 1                 # contorno leve para o título
SUBTITLE_COLOR = (240,240,240,255)

# === FONTES (Ubuntu padrão) ===
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# === AJUSTE DO ÍCONE DO SINAPSE ===
# fração do width original considerada "ícone" (resto é texto)
ICON_FRACTION = 0.26  # ajuste fino se necessário (0.24–0.30)
ICON_TARGET_HEIGHT = 110  # altura alvo do conjunto ícone + título (será escalonado com o resto se faltar espaço)

# === AJUSTES IFTM ===
IFTM_WIDTH_BOOST = 1.10
IFTM_STROKE_PX   = 2
IFTM_UNSHARP     = True

def load_rgba(p): 
    return Image.open(p).convert("RGBA")

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

def text_mask(text, font):
    dummy = Image.new("L", (1,1), 0)
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0,0), text, font=font, spacing=4, align="left")
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    d.text((0,0), text, font=font, fill=255, spacing=4, align="left")
    return im

def gradient_image(size, start, end):
    w,h = size
    grad = np.linspace(0,1,w, dtype=np.float32)
    r = (1-grad)*start[0] + grad*end[0]
    g = (1-grad)*start[1] + grad*end[1]
    b = (1-grad)*start[2] + grad*end[2]
    rgb = np.stack([np.tile(r,(h,1)), np.tile(g,(h,1)), np.tile(b,(h,1))], axis=2).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")

def draw_title_with_gradient(text, font, stroke_px=1):
    mask = text_mask(text, font)  # L
    w,h = mask.size
    grad = gradient_image((w,h), GRAD_START, GRAD_END).convert("RGBA")
    # aplica micro contorno branco
    if stroke_px>0:
        # dilata e subtrai para gerar borda
        dil = mask.filter(ImageFilter.MaxFilter(stroke_px*2+1))
        edge = Image.new("L", (w,h), 0)
        edge = ImageChops.subtract(dil, mask)
        stroke = Image.new("RGBA", (w,h), (255,255,255,255))
        stroke.putalpha(edge)
        grad = Image.alpha_composite(stroke, grad)
    grad.putalpha(mask)
    return grad

# Import atrasado para ImageChops (após definição)
from PIL import ImageChops

def compose_mid_block(mid_png, max_width):
    """Recorta ícone à esquerda e renderiza o texto do zero ao lado."""
    icon_src = trim_alpha(mid_png)
    w,h = icon_src.size
    icon_w = int(w * ICON_FRACTION)
    icon = icon_src.crop((0,0,icon_w,h))
    # Redimensiona ícone para altura alvo
    icon = icon.resize((int(icon_w * (ICON_TARGET_HEIGHT/h)), ICON_TARGET_HEIGHT), Image.Resampling.LANCZOS)

    # Tamanho das fontes proporcional ao ícone
    title_font_size = int(ICON_TARGET_HEIGHT * 0.54)   # ajuste fino
    sub_font_size   = int(ICON_TARGET_HEIGHT * 0.18)

    font_title = ImageFont.truetype(FONT_BOLD, title_font_size)
    font_sub   = ImageFont.truetype(FONT_REG,  sub_font_size)

    title_img = draw_title_with_gradient(TITLE, font_title, stroke_px=STROKE_PX)
    sub_mask  = text_mask(SUBTITLE, font_sub)
    sub_rgba  = Image.new("RGBA", sub_mask.size, SUBTITLE_COLOR); sub_rgba.putalpha(sub_mask)

    # Layout horizontal: [ÍCONE][gap][TÍTULO] (sub abaixo do título)
    gap_h = int(ICON_TARGET_HEIGHT * 0.18)
    block_w = icon.width + gap_h + max(title_img.width, sub_rgba.width)
    block_h = max(icon.height, title_img.height + 6 + sub_rgba.height)

    block = Image.new("RGBA", (block_w, block_h), (0,0,0,0))
    x = 0
    # centraliza verticalmente ícone vs conjunto texto
    icon_y = (block_h - icon.height)//2
    block.paste(icon, (x, icon_y), icon)
    x += icon.width + gap_h
    text_y = (block_h - (title_img.height + 6 + sub_rgba.height))//2
    block.paste(title_img, (x, text_y), title_img)
    block.paste(sub_rgba, (x, text_y + title_img.height + 6), sub_rgba)

    # se exceder largura disponível, escala
    if block.width > max_width:
        scale = max_width / block.width
        block = block.resize((int(block.width*scale), int(block.height*scale)), Image.Resampling.LANCZOS)

    return block

def main():
    # Carrega e prepara topo/bot
    top = trim_alpha(load_rgba(IMG_TOP))
    mid = load_rgba(IMG_MID)
    bot = trim_alpha(load_rgba(IMG_BOT))

    content_w = CANVAS - 2*SIDE_PAD

    # Topo com destaque
    top = fit_width(top, min(int(content_w * IFTM_WIDTH_BOOST), content_w))
    if IFTM_STROKE_PX>0: top = add_white_stroke(top, IFTM_STROKE_PX)
    if IFTM_UNSHARP:     top = unsharp(top)

    # Meio: reconstruído
    mid_block = compose_mid_block(mid, content_w)

    # Base
    bot = fit_width(bot, content_w)

    # Checa altura total e escala se necessário
    ims = [top, mid_block, bot]
    total_h = sum(i.size[1] for i in ims) + GAP*2
    avail_h = CANVAS - TOP_PAD - BOT_PAD
    if total_h > avail_h:
        scale = avail_h / total_h
        ims = [i.resize((max(1,int(i.size[0]*scale)), max(1,int(i.size[1]*scale))), Image.Resampling.LANCZOS) for i in ims]

    # Monta canvas
    canvas = Image.new("RGBA", (CANVAS, CANVAS), BG)
    y = (CANVAS - (sum(i.size[1] for i in ims) + GAP*2))//2
    for idx, im in enumerate(ims):
        x = (CANVAS - im.size[0])//2
        canvas.paste(im, (x, y), im)
        y += im.size[1] + (GAP if idx < 2 else 0)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    canvas.save(OUTPUT, "PNG")
    print(f"✅ Poster reconstruído sem halo: {OUTPUT}")

if __name__ == "__main__":
    main()

