# -*- coding: utf-8 -*-
"""Imágenes procedurales originales (estilo neón / Vice City) para cada escena.

Cada escena produce dos capas: fondo (más grande que el cuadro, para movimiento)
y primer plano RGBA con texto y gráficos.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1920, 1080
BW, BH = 2208, 1242  # fondo 1.15x para paneo/zoom

F = "/usr/share/fonts/opentype/inter/"
def font(size, w="ExtraBold"):
    try:
        return ImageFont.truetype(F + f"InterDisplay-{w}.otf", size)
    except OSError:
        return ImageFont.truetype(F + f"Inter-{w}.otf", size)

PINK, ORANGE, PURPLE, TEAL, YELLOW = (255, 62, 154), (255, 140, 66), (122, 44, 191), (0, 214, 214), (255, 214, 102)
COLORS = {"pink": PINK, "orange": ORANGE, "purple": (178, 102, 255), "teal": TEAL}


# ─────────────────────────── utilidades ───────────────────────────
def grad(w, h, stops):
    """Degradado vertical. stops = [(pos, (r,g,b)), ...]"""
    im = Image.new("RGB", (1, h))
    px = im.load()
    for y in range(h):
        p = y / (h - 1)
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            if p0 <= p <= p1:
                k = (p - p0) / max(1e-6, p1 - p0)
                px[0, y] = tuple(int(a + (b - a) * k) for a, b in zip(c0, c1))
                break
    return im.resize((w, h))


def glow(layer, r=18, k=2):
    g = layer.filter(ImageFilter.GaussianBlur(r))
    out = layer.copy()
    for _ in range(k):
        out = Image.alpha_composite(g, out)
    return out


def palm(d, x, base, h, rnd, col=(15, 5, 30)):
    lean = rnd.uniform(-0.25, 0.25)
    pts = []
    for i in range(21):
        t = i / 20
        pts.append((x + lean * h * t * t + math.sin(t * 3) * 6, base - h * t))
    for i in range(20):
        w = 16 * (1 - pts[i][1] * 0 - i / 30)
        d.line([pts[i], pts[i + 1]], fill=col, width=max(6, int(w)))
    tx, ty = pts[-1]
    for a in range(9):
        ang = -math.pi + a * math.pi / 8 + rnd.uniform(-.15, .15)
        L = h * rnd.uniform(.32, .45)
        prev = (tx, ty)
        for s in range(1, 13):
            t = s / 12
            px = tx + math.cos(ang) * L * t
            py = ty + math.sin(ang) * L * t * 0.6 + (L * 0.5) * t * t
            d.line([prev, (px, py)], fill=col, width=max(2, int(14 * (1 - t))))
            for side in (-1, 1):
                d.line([(px, py), (px + side * 10 * (1 - t) + math.cos(ang) * 8, py + 22 * (1 - t * .5))], fill=col, width=3)
            prev = (px, py)
    d.ellipse([tx - 14, ty - 10, tx + 14, ty + 14], fill=col)


def sun(img, cx, cy, r, c_top=YELLOW, c_bot=PINK, stripes=True):
    s = grad(2 * r, 2 * r, [(0, c_top), (1, c_bot)]).convert("RGBA")
    m = Image.new("L", (2 * r, 2 * r), 0)
    md = ImageDraw.Draw(m)
    md.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    if stripes:
        for i in range(8):
            y = int(r * 1.05 + i * i * r * 0.016 + i * r * 0.07)
            md.rectangle([0, y, 2 * r, y + 4 + i * 2], fill=0)
    s.putalpha(m)
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx - r * 1.5, cy - r * 1.5, cx + r * 1.5, cy + r * 1.5], fill=c_bot + (90,))
    halo = halo.filter(ImageFilter.GaussianBlur(r * 0.5))
    img.alpha_composite(halo)
    img.alpha_composite(s, (cx - r, cy - r))


def buildings(d, rnd, base, x0, x1, hmin, hmax, col, win=None, wdens=0.35):
    x = x0
    while x < x1:
        w = rnd.randint(50, 140)
        h = rnd.randint(hmin, hmax)
        d.rectangle([x, base - h, x + w, base], fill=col)
        if rnd.random() < .3:
            d.polygon([(x, base - h), (x + w / 2, base - h - rnd.randint(20, 70)), (x + w, base - h)], fill=col)
        if rnd.random() < .25:
            d.line([(x + w / 2, base - h), (x + w / 2, base - h - rnd.randint(30, 90))], fill=col, width=4)
        if win:
            for wy in range(base - h + 14, base - 10, 22):
                for wx in range(x + 8, x + w - 10, 18):
                    if rnd.random() < wdens:
                        d.rectangle([wx, wy, wx + 8, wy + 10], fill=rnd.choice(win))
        x += w + rnd.randint(-10, 18)


def stars(d, rnd, w, h, n=300):
    for _ in range(n):
        x, y = rnd.randint(0, w), rnd.randint(0, h)
        b = rnd.randint(120, 255)
        d.point((x, y), fill=(b, b, b, 255))


def vignette(img, s=0.65):
    w, h = img.size
    m = Image.new("L", (w // 8, h // 8), 0)
    md = ImageDraw.Draw(m)
    md.ellipse([-w // 16, -h // 16, w // 8 + w // 16, h // 8 + h // 16], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(w // 40)).resize((w, h))
    dark = Image.new("RGBA", (w, h), (5, 0, 15, int(255 * s)))
    dark.putalpha(ImageChops.invert(m).point(lambda v: int(v * s)))
    img.alpha_composite(dark)


def grain(img, rnd, amt=10):
    n = Image.effect_noise((img.width // 2, img.height // 2), amt).resize(img.size).convert("RGBA")
    n.putalpha(18)
    img.alpha_composite(n)


# ─────────────────────────── fondos ───────────────────────────
def bg_sunset(rnd):
    w, h = BW, BH
    hz = int(h * 0.64)
    img = grad(w, h, [(0, (25, 6, 60)), (.35, (110, 20, 120)), (.6, (255, 80, 120)), (.64, (255, 150, 90)),
                      (.65, (40, 10, 70)), (1, (10, 2, 30))]).convert("RGBA")
    d = ImageDraw.Draw(img)
    stars(d, rnd, w, int(h * .3), 150)
    sun(img, w // 2 + rnd.randint(-300, 300), hz - 40, 260)
    # mar
    sea = grad(w, h - hz, [(0, (70, 20, 100)), (1, (10, 2, 30))]).convert("RGBA")
    img.alpha_composite(sea, (0, hz))
    d = ImageDraw.Draw(img)
    for i in range(70):
        y = hz + int((i / 70) ** 1.6 * (h - hz))
        x = w // 2 + rnd.randint(-380, 380)
        L = rnd.randint(30, 200)
        d.line([(x - L, y), (x + L, y)], fill=(255, 120 + rnd.randint(0, 100), 140, 140), width=2 + i // 25)
    for x in (rnd.randint(40, 300), rnd.randint(w - 420, w - 120)):
        palm(d, x, h + 20, rnd.randint(650, 900), rnd)
    if rnd.random() < .6:
        palm(d, rnd.randint(320, 520), h + 20, rnd.randint(420, 560), rnd)
    return img


def bg_skyline(rnd):
    w, h = BW, BH
    base = int(h * 0.7)
    img = grad(w, h, [(0, (20, 5, 50)), (.5, (140, 30, 120)), (.7, (255, 120, 100)), (1, (30, 5, 50))]).convert("RGBA")
    sun(img, rnd.randint(500, w - 500), base - 120, 200)
    d = ImageDraw.Draw(img)
    buildings(d, rnd, base, -20, w, 150, 380, (70, 25, 100))
    buildings(d, rnd, base, -40, w, 120, 560, (25, 8, 45), win=[(255, 200, 120), (255, 120, 200), (120, 230, 255)], wdens=.25)
    water = img.crop((0, base - (h - base), w, base)).transpose(Image.FLIP_TOP_BOTTOM)
    water = water.filter(ImageFilter.GaussianBlur(3))
    water.putalpha(150)
    d.rectangle([0, base, w, h], fill=(15, 4, 30, 255))
    img.alpha_composite(water, (0, base))
    d = ImageDraw.Draw(img)
    for i in range(60):
        y = base + rnd.randint(0, h - base)
        x = rnd.randint(0, w)
        d.line([(x, y), (x + rnd.randint(40, 160), y)], fill=(255, 150, 200, 70), width=2)
    palm(d, rnd.randint(30, 200), h + 30, 780, rnd, (8, 2, 18))
    palm(d, rnd.randint(w - 300, w - 80), h + 30, 700, rnd, (8, 2, 18))
    return img


def bg_night(rnd):
    w, h = BW, BH
    base = int(h * 0.74)
    img = grad(w, h, [(0, (4, 2, 18)), (.6, (35, 10, 70)), (.74, (80, 20, 110)), (1, (5, 2, 15))]).convert("RGBA")
    d = ImageDraw.Draw(img)
    stars(d, rnd, w, base, 400)
    ImageDraw.Draw(img).ellipse([w * .78, 90, w * .78 + 110, 200], fill=(240, 230, 255, 255))
    neon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nd = ImageDraw.Draw(neon)
    x = -20
    while x < w:
        bw, bh = rnd.randint(60, 150), rnd.randint(140, 600)
        d.rectangle([x, base - bh, x + bw, base], fill=(10, 4, 25))
        c = rnd.choice([PINK, TEAL, (178, 102, 255), ORANGE])
        nd.rectangle([x, base - bh, x + bw, base], outline=c + (255,), width=3)
        for wy in range(base - bh + 16, base - 12, 26):
            for wx in range(x + 10, x + bw - 12, 20):
                if rnd.random() < .18:
                    d.rectangle([wx, wy, wx + 8, wy + 12], fill=(255, 220, 150))
        x += bw + rnd.randint(4, 30)
    img.alpha_composite(glow(neon, 14, 2))
    d = ImageDraw.Draw(img)
    d.rectangle([0, base, w, h], fill=(8, 3, 18))
    refl = neon.crop((0, base - (h - base), w, base)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(refl, (0, base))
    return img


def bg_beach(rnd):
    w, h = BW, BH
    hz = int(h * .55)
    img = grad(w, h, [(0, (40, 120, 220)), (.45, (120, 200, 240)), (.55, (255, 210, 180)), (1, (255, 210, 180))]).convert("RGBA")
    sun(img, rnd.randint(300, w - 300), 220, 110, (255, 255, 220), (255, 230, 160), stripes=False)
    d = ImageDraw.Draw(img)
    for _ in range(8):
        cx, cy = rnd.randint(0, w), rnd.randint(60, hz - 200)
        for k in range(6):
            d.ellipse([cx + k * 40 - 80, cy - 30 + rnd.randint(-15, 15), cx + k * 40 + 40, cy + 30], fill=(255, 255, 255, 120))
    sea = grad(w, int(h * .2), [(0, (0, 150, 190)), (1, (60, 220, 210))]).convert("RGBA")
    img.alpha_composite(sea, (0, hz))
    d = ImageDraw.Draw(img)
    for i in range(40):
        y = hz + rnd.randint(0, int(h * .2))
        x = rnd.randint(0, w)
        d.line([(x, y), (x + rnd.randint(30, 120), y)], fill=(255, 255, 255, 110), width=2)
    sand_y = hz + int(h * .2)
    d.polygon([(0, sand_y), (w, sand_y - 30), (w, h), (0, h)], fill=(250, 220, 170))
    d.line([(0, sand_y), (w, sand_y - 30)], fill=(255, 255, 255), width=6)
    # sombrillas
    for _ in range(5):
        x, y = rnd.randint(300, w - 300), rnd.randint(sand_y + 60, h - 60)
        c = rnd.choice([PINK, TEAL, ORANGE, YELLOW])
        d.line([(x, y), (x, y - 120)], fill=(80, 60, 50), width=5)
        d.pieslice([x - 90, y - 170, x + 90, y - 70], 180, 360, fill=c)
    # hoteles art déco al fondo
    for i in range(6):
        x = rnd.randint(0, w)
        bw, bh = rnd.randint(120, 200), rnd.randint(90, 200)
        c = rnd.choice([(255, 200, 220), (200, 240, 235), (255, 235, 200)])
        d.rectangle([x, hz - bh, x + bw, hz], fill=c)
        for wy in range(hz - bh + 15, hz - 10, 24):
            d.line([(x + 10, wy), (x + bw - 10, wy)], fill=(80, 170, 190), width=6)
    for x in (rnd.randint(20, 220), rnd.randint(w - 360, w - 120)):
        palm(d, x, h + 20, rnd.randint(700, 950), rnd, (30, 60, 40))
    return img


def bg_highway(rnd):
    w, h = BW, BH
    hz = int(h * .5)
    img = grad(w, h, [(0, (30, 10, 70)), (.4, (220, 70, 120)), (.5, (255, 170, 90)), (.51, (40, 20, 80)), (1, (10, 5, 30))]).convert("RGBA")
    sun(img, w // 2, hz - 30, 180)
    d = ImageDraw.Draw(img)
    # puente/autopista en perspectiva
    vx = w // 2
    d.polygon([(vx - 8, hz), (vx + 8, hz), (w * .9, h), (w * .1, h)], fill=(25, 15, 40))
    for i in range(1, 14):
        t = (i / 14) ** 2
        y = hz + t * (h - hz)
        y2 = hz + ((i + .45) / 14) ** 2 * (h - hz)
        d.polygon([(vx - 2 - 3 * t, y), (vx + 2 + 3 * t, y), (vx + 2 + 3 * t + 6, y2), (vx - 2 - 3 * t - 6, y2)], fill=YELLOW)
    for side in (-1, 1):
        d.line([(vx + side * 8, hz), (vx + side * (w * .4), h)], fill=PINK, width=6)
        for i in range(1, 20):
            t = (i / 20) ** 2
            x = vx + side * (8 + t * (w * .4 - 8))
            y = hz + t * (h - hz)
            d.line([(x, y), (x, y - 10 - 160 * t)], fill=(60, 30, 80), width=max(2, int(10 * t)))
    # luces traseras
    for _ in range(6):
        t = rnd.uniform(.15, .8) ** 2
        x = vx + rnd.choice([-1, 1]) * t * w * .18
        y = hz + t * (h - hz)
        s = 4 + 30 * t
        d.ellipse([x - s, y - s / 2, x - s / 3, y + s / 2], fill=(255, 40, 60))
        d.ellipse([x + s / 3, y - s / 2, x + s, y + s / 2], fill=(255, 40, 60))
    return img


def bg_grid(rnd):
    w, h = BW, BH
    hz = int(h * .55)
    img = grad(w, h, [(0, (10, 0, 30)), (.55, (80, 10, 90)), (.551, (15, 0, 30)), (1, (5, 0, 15))]).convert("RGBA")
    d = ImageDraw.Draw(img)
    stars(d, rnd, w, hz - 100, 200)
    sun(img, w // 2, hz - 10, 240)
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for i in range(-30, 31):
        gd.line([(w // 2 + i * 12, hz), (w // 2 + i * 180, h)], fill=PINK + (255,), width=3)
    for i in range(1, 22):
        y = hz + (i / 21) ** 2.2 * (h - hz)
        gd.line([(0, y), (w, y)], fill=PINK + (255,), width=2 + i // 7)
    img.alpha_composite(glow(g, 10, 1))
    # montañas
    d = ImageDraw.Draw(img)
    pts = [(0, hz)]
    for x in range(0, w + 80, 80):
        if abs(x - w // 2) > 300:
            pts.append((x, hz - rnd.randint(30, 180)))
        else:
            pts.append((x, hz))
    pts.append((w, hz))
    d.polygon(pts, fill=(30, 5, 50))
    d.line(pts[1:-1], fill=TEAL, width=3)
    return img


# Mapa estilizado (inventado) de "Leonida": península con regiones
REGIONS = {
    "Port Gellhorn": (0.12, 0.14), "Mount Kalaga": (0.45, 0.12), "Ambrosia": (0.60, 0.30),
    "Grassrivers": (0.63, 0.60), "Vice City": (0.78, 0.66), "Leonida Keys": (0.60, 0.93),
}


def bg_map(rnd):
    w, h = BW, BH
    img = grad(w, h, [(0, (5, 20, 45)), (1, (2, 8, 25))]).convert("RGBA")
    d = ImageDraw.Draw(img)
    for x in range(0, w, 60):
        d.line([(x, 0), (x, h)], fill=(20, 50, 90, 255), width=1)
    for y in range(0, h, 60):
        d.line([(0, y), (w, y)], fill=(20, 50, 90, 255), width=1)
    return img


def leonida_poly(ox, oy, s):
    pts = [(0, .06), (.62, .06), (.66, .10), (.70, .22), (.76, .38), (.82, .55), (.84, .70), (.80, .80),
           (.74, .84), (.68, .80), (.60, .70), (.55, .58), (.50, .45), (.47, .32), (.40, .24), (.30, .22),
           (.18, .25), (.06, .22), (0, .18)]
    return [(ox + x * s * 1.25, oy + y * s) for x, y in pts]


BGS = {"sunset": bg_sunset, "skyline": bg_skyline, "night": bg_night, "beach": bg_beach,
       "highway": bg_highway, "grid": bg_grid, "map": bg_map}


def background(kind, seed, ai_path=None):
    if ai_path:
        from PIL import ImageEnhance
        im = Image.open(ai_path).convert("RGB")
        k = max(BW / im.width, BH / im.height)
        im = im.resize((int(im.width * k + .5), int(im.height * k + .5)), Image.LANCZOS)
        x, y = (im.width - BW) // 2, (im.height - BH) // 2
        im = im.crop((x, y, x + BW, y + BH))
        im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.1)).enhance(1.05)
        img = im.convert("RGBA")
        tint = Image.new("RGBA", img.size, (40, 0, 60, 40))
        img.alpha_composite(tint)
        vignette(img, .5)
        return img
    rnd = random.Random(seed)
    img = BGS[kind](rnd)
    vignette(img, .55)
    return img


# ─────────────────────────── primer plano ───────────────────────────
def text_glow(fg, xy, txt, fnt, fill=(255, 255, 255), gcol=PINK, anchor="mm", r=16, stroke=0):
    gl = Image.new("RGBA", fg.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).text(xy, txt, font=fnt, fill=gcol + (255,), anchor=anchor, stroke_width=stroke + 4, stroke_fill=gcol + (255,))
    gl = gl.filter(ImageFilter.GaussianBlur(r))
    fg.alpha_composite(gl)
    fg.alpha_composite(gl)
    ImageDraw.Draw(fg).text(xy, txt, font=fnt, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(20, 0, 40))


def fit(txt, size, maxw, w="ExtraBold"):
    while size > 20:
        f = font(size, w)
        if f.getbbox(txt)[2] <= maxw:
            return f
        size -= 4
    return font(size, w)


def panel(fg, box, alpha=150, outline=PINK):
    p = Image.new("RGBA", fg.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(p)
    pd.rounded_rectangle(box, 28, fill=(12, 2, 30, alpha))
    fg.alpha_composite(p)
    o = Image.new("RGBA", fg.size, (0, 0, 0, 0))
    ImageDraw.Draw(o).rounded_rectangle(box, 28, outline=outline + (255,), width=4)
    fg.alpha_composite(glow(o, 10, 1))


def caption_bar(fg, txt):
    f = font(46, "Bold")
    tw = f.getbbox(txt)[2]
    x0, y0 = 90, H - 190
    panel(fg, [x0, y0, x0 + tw + 90, y0 + 100], 170, PINK)
    d = ImageDraw.Draw(fg)
    d.rectangle([x0 + 26, y0 + 28, x0 + 34, y0 + 72], fill=YELLOW)
    d.text((x0 + 56, y0 + 50), txt, font=f, fill="white", anchor="lm")


def silhouette(fg, cx, cy, s, col):
    l = Image.new("RGBA", fg.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    d.ellipse([cx - 95 * s, cy - 330 * s, cx + 95 * s, cy - 100 * s], fill=(10, 2, 25, 255), outline=col + (255,), width=6)
    d.rounded_rectangle([cx - 40 * s, cy - 120 * s, cx + 40 * s, cy - 60 * s], 10, fill=(10, 2, 25, 255))
    d.pieslice([cx - 260 * s, cy - 90 * s, cx + 260 * s, cy + 420 * s], 180, 360, fill=(10, 2, 25, 255), outline=col + (255,), width=6)
    fg.alpha_composite(glow(l, 22, 2))
    d = ImageDraw.Draw(fg)
    d.text((cx, cy - 215 * s), "?", font=font(int(150 * s)), fill=col + (230,), anchor="mm")


def lower_third(fg, title, sub, col=PINK):
    f = fit(title, 96, 1100)
    tw = max(f.getbbox(title)[2], font(40, "Bold").getbbox(sub.upper())[2]) if sub else f.getbbox(title)[2]
    panel(fg, [80, H - 330, 80 + tw + 120, H - 90], 175, col)
    text_glow(fg, (140, H - 240), title, f, anchor="lm", gcol=col, r=14)
    if sub:
        d = ImageDraw.Draw(fg)
        fs = font(40, "Bold")
        sw = fs.getbbox(sub.upper())[2]
        d.rounded_rectangle([140, H - 175, 140 + sw + 44, H - 115], 14, fill=col)
        d.text((162, H - 145), sub.upper(), font=fs, fill=(15, 0, 30), anchor="lm")


def foreground(v, chapter=None, ai=False):
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fg)
    t = v["t"]
    if t == "title":
        text_glow(fg, (W // 2, H // 2 - 60), v["title"], fit(v["title"], 300, W - 200), r=24)
        text_glow(fg, (W // 2, H // 2 + 130), v["sub"], fit(v["sub"], 70, W - 300, "Bold"), gcol=TEAL, r=12)
    elif t == "chapter":
        panel(fg, [W // 2 - 760, H // 2 - 230, W // 2 + 760, H // 2 + 230], 160)
        text_glow(fg, (W // 2, H // 2 - 90), "CAPÍTULO " + v["n"], font(70, "Bold"), fill=YELLOW, gcol=ORANGE, r=10)
        text_glow(fg, (W // 2, H // 2 + 60), v["title"], fit(v["title"], 120, 1400), r=18)
    elif t == "stat":
        panel(fg, [W // 2 - 720, 200, W // 2 + 720, 860], 165)
        text_glow(fg, (W // 2, 430), v["big"], fit(v["big"], 280, 1300), fill=YELLOW, gcol=PINK, r=26)
        text_glow(fg, (W // 2, 640), v["label"].upper(), fit(v["label"].upper(), 80, 1300, "Bold"), gcol=TEAL, r=10)
        d = ImageDraw.Draw(fg)
        d.text((W // 2, 760), v["sub"], font=fit(v["sub"], 44, 1300, "Medium"), fill=(220, 210, 240), anchor="mm")
    elif t == "bullets":
        n = len(v["items"])
        top = H // 2 - (n * 92 + 150) // 2
        panel(fg, [260, top - 30, W - 260, top + 150 + n * 92 + 10], 175)
        text_glow(fg, (W // 2, top + 55), v["title"], fit(v["title"], 76, 1200), gcol=PINK, r=12)
        d = ImageDraw.Draw(fg)
        for i, it in enumerate(v["items"]):
            y = top + 160 + i * 92
            c = TEAL if not it.startswith("–") else ORANGE
            d.rounded_rectangle([340, y - 14, 368, y + 14], 6, fill=c)
            d.text((400, y), it, font=fit(it, 52, 1200, "SemiBold"), fill="white", anchor="lm")
    elif t == "quote":
        panel(fg, [200, 250, W - 200, 830], 165, TEAL)
        d = ImageDraw.Draw(fg)
        d.text((290, 250), "“", font=font(300), fill=PINK, anchor="lt")
        words, lines, cur = v["text"].split(), [], ""
        f = font(78, "Bold")
        for wd in words:
            if f.getbbox(cur + " " + wd)[2] > 1300:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        y0 = 540 - (len(lines) - 1) * 50
        for i, ln in enumerate(lines):
            text_glow(fg, (W // 2, y0 + i * 100), ln, f, gcol=PURPLE, r=10)
        ImageDraw.Draw(fg).text((W // 2, 760), "— " + v["author"], font=font(44, "Medium"), fill=YELLOW, anchor="mm")
    elif t == "timeline":
        ev = v["events"]
        panel(fg, [120, 170, W - 120, 900], 170)
        text_glow(fg, (W // 2, 260), v["title"], fit(v["title"], 76, 1500), r=12)
        y = 560
        line = Image.new("RGBA", fg.size, (0, 0, 0, 0))
        ImageDraw.Draw(line).line([(220, y), (W - 220, y)], fill=TEAL + (255,), width=8)
        fg.alpha_composite(glow(line, 10, 1))
        d = ImageDraw.Draw(fg)
        n = len(ev)
        for i, (date, lab) in enumerate(ev):
            x = 220 + i * (W - 440) / (n - 1)
            last = i == n - 1
            r = 26 if last else 18
            d.ellipse([x - r, y - r, x + r, y + r], fill=YELLOW if last else PINK, outline="white", width=4)
            up = i % 2 == 0
            d.text((x, y + (-70 if up else 70)), date, font=font(40, "ExtraBold"), fill=YELLOW, anchor="mm")
            fl = font(32, "SemiBold")
            maxw = (W - 440) / (n - 1) * 1.7
            lines, cur = [], ""
            for wd in lab.split():
                if cur and fl.getbbox(cur + " " + wd)[2] > maxw:
                    lines.append(cur); cur = wd
                else:
                    cur = (cur + " " + wd).strip()
            lines.append(cur)
            for k, ln in enumerate(lines):
                fy = (y - 125 - (len(lines) - 1 - k) * 40) if up else (y + 125 + k * 40)
                d.text((x, fy), ln, font=fl, fill="white", anchor="mm")
    elif t == "map" and ai and v.get("hl"):
        ox, oy, s = 1290, 150, 430
        panel(fg, [1240, 110, 1840, 610], 175, TEAL)
        land = Image.new("RGBA", fg.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(land)
        poly = leonida_poly(ox, oy, s)
        ld.polygon(poly, fill=(30, 70, 60, 255), outline=TEAL + (255,))
        for i in range(9):
            cx = ox + (.74 - i * .022) * s * 1.25
            cy = oy + (.87 + i * .009) * s
            ld.ellipse([cx - 11, cy - 5, cx + 11, cy + 5], fill=(30, 70, 60, 255))
        fg.alpha_composite(land)
        d = ImageDraw.Draw(fg)
        for name, (rx, ry) in REGIONS.items():
            x, y = ox + rx * s * 1.25, oy + ry * s
            on = v.get("hl") == name
            r = 13 if on else 6
            d.ellipse([x - r, y - r, x + r, y + r], fill=YELLOW if on else (200, 200, 220), outline=PINK if on else None, width=4)
        d.text((1540, 585), "Mapa ilustrativo", font=font(22, "Medium"), fill=(170, 180, 210), anchor="mm")
        lower_third(fg, v["title"], "Región de Leonida", TEAL)
    elif t == "map":
        ox, oy, s = 330, 120, 860
        land = Image.new("RGBA", fg.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(land)
        poly = leonida_poly(ox, oy, s)
        ld.polygon(poly, fill=(30, 70, 60, 255))
        # cayos
        for i in range(9):
            cx = ox + (.74 - i * .022) * s * 1.25
            cy = oy + (.87 + i * .009) * s
            ld.ellipse([cx - 22, cy - 9, cx + 22, cy + 9], fill=(30, 70, 60, 255))
        ol = Image.new("RGBA", fg.size, (0, 0, 0, 0))
        ImageDraw.Draw(ol).line(poly + [poly[0]], fill=TEAL + (255,), width=5)
        fg.alpha_composite(land)
        fg.alpha_composite(glow(ol, 12, 1))
        d = ImageDraw.Draw(fg)
        for name, (rx, ry) in REGIONS.items():
            x, y = ox + rx * s * 1.25, oy + ry * s
            on = v.get("hl") == name
            if on:
                halo = Image.new("RGBA", fg.size, (0, 0, 0, 0))
                ImageDraw.Draw(halo).ellipse([x - 120, y - 120, x + 120, y + 120], fill=PINK + (150,))
                fg.alpha_composite(halo.filter(ImageFilter.GaussianBlur(40)))
                d = ImageDraw.Draw(fg)
            r = 16 if on else 10
            d.ellipse([x - r, y - r, x + r, y + r], fill=YELLOW if on else (200, 200, 220))
            d.text((x + 26, y), name, font=font(44 if on else 32, "Bold" if on else "Medium"),
                   fill=YELLOW if on else (220, 220, 235), anchor="lm", stroke_width=3, stroke_fill=(5, 10, 25))
        text_glow(fg, (W - 120, H - 260), v["title"], fit(v["title"], 90, 700), anchor="rt", r=14)
        d = ImageDraw.Draw(fg)
        d.text((W - 120, H - 140), "Mapa ilustrativo", font=font(30, "Medium"), fill=(160, 170, 200), anchor="rt")
    elif t == "character" and ai:
        lower_third(fg, v["name"], v["role"], COLORS[v["color"]])
        d = ImageDraw.Draw(fg)
        d.text((W - 60, H - 40), "Imagen ilustrativa generada por IA", font=font(24, "Medium"), fill=(220, 220, 235), anchor="rs")
    elif t == "character":
        col = COLORS[v["color"]]
        panel(fg, [140, 140, 1780, 940], 150, col)
        silhouette(fg, 560, 720, 1.25, col)
        text_glow(fg, (1000, 470), v["name"], fit(v["name"], 120, 820), anchor="lm", gcol=col, r=16)
        d = ImageDraw.Draw(fg)
        d.rounded_rectangle([1000, 560, 1000 + font(46, "Bold").getbbox(v["role"].upper())[2] + 50, 640], 16, fill=col)
        d.text((1025, 600), v["role"].upper(), font=font(46, "Bold"), fill=(15, 0, 30), anchor="lm")
    elif t == "scene":
        caption_bar(fg, v["cap"])
    # marca de capítulo arriba a la izquierda
    if chapter and t not in ("title", "chapter"):
        d = ImageDraw.Draw(fg)
        f = font(30, "Bold")
        txt = chapter
        tw = f.getbbox(txt)[2]
        d.rounded_rectangle([60, 50, 60 + tw + 50, 104], 14, fill=(10, 2, 25, 180), outline=PINK, width=2)
        d.text((85, 77), txt, font=f, fill="white", anchor="lm")
    return fg


if __name__ == "__main__":
    import os, sys
    from guion import ESCENAS
    os.makedirs("build/preview", exist_ok=True)
    idx = [int(a) for a in sys.argv[1:]] or range(len(ESCENAS))
    for i in idx:
        v = ESCENAS[i]["visual"]
        bg = background(v["bg"], i)
        x, y = (BW - W) // 2, (BH - H) // 2
        im = bg.crop((x, y, x + W, y + H))
        im.alpha_composite(foreground(v, "GTA VI"))
        im.convert("RGB").save(f"build/preview/{i:03d}.jpg", quality=88)
        print(i)
