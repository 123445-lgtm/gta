# -*- coding: utf-8 -*-
"""Recorta cada cuadrícula 2x2 generada por IA en 4 imágenes (una por escena)."""
import json, os, sys
import numpy as np
from PIL import Image

g = json.load(open("build/el/grids.json"))["grids"]
os.makedirs("build/img", exist_ok=True)


def gutter(frac, center, span):
    """Busca la franja casi negra (separador) cerca del centro.
    frac = fracción de píxeles muy oscuros por columna/fila."""
    lo, hi = int(center - span), int(center + span)
    seg = frac[lo:hi]
    dark = np.where(seg > 0.85)[0]
    if len(dark) == 0:
        c = int(center)
        return c, c
    # tramo contiguo más cercano al centro
    runs, start = [], dark[0]
    for p, q in zip(dark, dark[1:]):
        if q != p + 1:
            runs.append((start, p)); start = q
    runs.append((start, dark[-1]))
    r = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 + lo - center))
    return lo + r[0], lo + r[1]


for k, idxs in enumerate(g):
    p = f"build/el/grids/g{k:02d}.png"
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGB")
    a = np.asarray(im.convert("L"), dtype=np.float32)
    H, W = a.shape
    d = (a < 28)
    x0, x1 = gutter(d.mean(axis=0), W / 2, W * 0.06)
    y0, y1 = gutter(d.mean(axis=1), H / 2, H * 0.06)
    m = 6  # margen extra para eliminar bordes del separador
    boxes = [(m, m, x0 - m, y0 - m), (x1 + m, m, W - m, y0 - m),
             (m, y1 + m, x0 - m, H - m), (x1 + m, y1 + m, W - m, H - m)]
    for i, b in zip(idxs, boxes):
        im.crop(b).save(f"build/img/{i:03d}.jpg", quality=93)
    print(k, "gutters x", x0, x1, "y", y0, y1)
