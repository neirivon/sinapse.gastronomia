#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ARQUIVO: /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/recortar_so_subtitulo.py
#
# Como executar:
#   python3 /home/neirivon/SINAPSE2.0/GASTRONOMIA/scripts/recortar_so_subtitulo.py
#
# O que faz:
#   - NÃO mexe na largura do arquivo: preserva todo o ícone e o texto “SINAPSE 2.0”
#   - Corta apenas o subtítulo (linhas pequenas de baixo)
#   - Salva /home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse_title.png

import os, numpy as np
from PIL import Image

SRC  = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse.png"
DST  = "/home/neirivon/SINAPSE2.0/GASTRONOMIA/assets/logo/sinapse_title.png"

# Ajustes do detector (pode afinar, se necessário)
SMOOTH_WIN   = 7        # média móvel no perfil de linhas (ímpar)
DENSE_RATIO  = 0.35     # fração do máximo para considerar “denso” (0.30–0.45)
BOTTOM_PAD   = 10       # px extras abaixo do título
SEARCH_FROM  = 0.20     # procurar faixa densa após 20% da altura
SEARCH_TO    = 0.80     # e antes de 80% (evita subtítulo)
FALLBACK_TOP_RATIO = 0.62  # se não achar, mantém ~62% da altura total

def moving_avg(v, k):
    if k <= 1: return v
    pad = k//2
    vpad = np.pad(v, (pad, pad), mode='edge')
    ker = np.ones(k, dtype=np.float32) / k
    return np.convolve(vpad, ker, mode='valid')

def main():
    im = Image.open(SRC).convert("RGBA")  # NÃO aparar alpha nas bordas: preserva largura!
    arr = np.array(im)                    # H x W x 4
    alpha = arr[..., 3]
    H, W = alpha.shape

    # Perfil de opacidade por linha e suavização
    row_counts = (alpha > 10).sum(axis=1).astype(np.float32)
    smooth = moving_avg(row_counts, SMOOTH_WIN)

    y0 = int(H * SEARCH_FROM); y1 = int(H * SEARCH_TO)
    seg = smooth[y0:y1]
    if seg.size == 0:
        cut_y = int(H * FALLBACK_TOP_RATIO)
    else:
        thr = max(3.0, seg.max() * DENSE_RATIO)
        dense = (seg >= thr).astype(np.uint8)

        # maior bloco contíguo de linhas densas (título)
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
            title_bottom = y0 + best_start + best_len - 1
            cut_y = min(H-1, title_bottom + BOTTOM_PAD)

    # CORTA APENAS NA VERTICAL: mantém x de 0 a W inteiro (sem mexer no ícone)
    recorte = im.crop((0, 0, W, cut_y))

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    recorte.save(DST)
    print(f"✅ Recorte salvo (apenas vertical): {DST}")
    print(f"   Tamanho original: {W}x{H}  →  recorte: {recorte.size[0]}x{recorte.size[1]}")

if __name__ == "__main__":
    main()

