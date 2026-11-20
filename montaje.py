# -*- coding: utf-8 -*-
"""Montaje: anima cada escena (paneo/zoom del fondo + entrada del texto),
la codifica con ffmpeg, une todo, mezcla voz + música y genera subtítulos SRT."""
import json, math, os, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
from guion import ESCENAS
from visuals import background, foreground, W, H, BW, BH

FPS = 30
OUT = "build/seg"
os.makedirs(OUT, exist_ok=True)
meta = json.load(open("build/audio_meta.json"))

# nombre del capítulo actual para la etiqueta superior
chap, CHAP = "INTRO", []
for e in ESCENAS:
    v = e["visual"]
    if v["t"] == "chapter":
        chap = f"{v['n']} · {v['title']}"
    CHAP.append(chap)


def ease(x):
    return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))


def render_scene(i):
    path = f"{OUT}/{i:03d}.mp4"
    if os.path.exists(path):
        return path
    v = ESCENAS[i]["visual"]
    dur = meta[i]["dur"]
    nf = int(round(dur * FPS))
    bg = background(v["bg"], i).convert("RGB")
    fg = foreground(v, CHAP[i])
    fg_a = fg.getchannel("A")
    fg_rgb = fg.convert("RGB")
    mode = i % 4  # 0 zoom in, 1 zoom out, 2 paneo der, 3 paneo izq
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                          "-tune", "stillimage", "-crf", "23", "-pix_fmt", "yuv420p", "-threads", "1", path + ".tmp.mp4"],
                         stdin=subprocess.PIPE)
    for f in range(nf):
        k = f / max(1, nf - 1)
        if mode == 0:
            z = 1.0 + 0.12 * k; cx, cy = .5, .5
        elif mode == 1:
            z = 1.12 - 0.12 * k; cx, cy = .5, .5
        elif mode == 2:
            z = 1.06; cx, cy = .5 - .06 + .12 * k, .5
        else:
            z = 1.06; cx, cy = .5 + .06 - .12 * k, .5
        # ventana del fondo a mostrar (tamaño W*s x H*s, centrada en cx,cy)
        s = (BW / W) / z
        ww, hh = W * s, H * s
        x0 = cx * BW - ww / 2
        y0 = cy * BH - hh / 2
        x0 = min(max(0, x0), BW - ww); y0 = min(max(0, y0), BH - hh)
        frame = bg.transform((W, H), Image.AFFINE, (s, 0, x0, 0, s, y0), resample=Image.BILINEAR)
        t = f / FPS
        a = ease((t - 0.15) / 0.6)
        if a > 0:
            dy = int((1 - a) * 40)
            mask = fg_a if a >= 1 else fg_a.point(lambda q, a=a: int(q * a))
            if dy == 0:
                frame.paste(fg_rgb, (0, 0), mask)
            else:
                frame.paste(fg_rgb.crop((0, 0, W, H - dy)), (0, dy), mask.crop((0, 0, W, H - dy)))
        # fundidos a negro entre escenas
        fade = min(1, t / 0.25, (dur - t) / 0.25)
        if fade < 1:
            frame = Image.blend(Image.new("RGB", (W, H)), frame, max(0, fade))
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    p.wait()
    os.rename(path + ".tmp.mp4", path)
    return path


def srt_time(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    n = len(ESCENAS)
    idx = list(range(n))
    with ProcessPoolExecutor(int(os.environ.get("JOBS", "4"))) as ex:
        for pth in ex.map(render_scene, idx):
            print(pth, file=sys.stderr, flush=True)

    # concat vídeo
    with open("build/concat.txt", "w") as f:
        for i in idx:
            f.write(f"file 'seg/{i:03d}.mp4'\n")
    # concat voz
    with open("build/voz.txt", "w") as f:
        for m in meta:
            f.write(f"file 'audio/{m['i']:03d}.wav'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "build/voz.txt",
                    "-ar", "44100", "-ac", "2", "build/voz.wav"], check=True)
    total = sum(m["dur"] for m in meta)
    subprocess.run([sys.executable, "musica.py", str(total), "build/musica.wav"], check=True)

    # subtítulos
    t0, k, lines = 0.0, 1, []
    for m in meta:
        for a, b, txt in m["subs"]:
            lines.append(f"{k}\n{srt_time(t0 + a)} --> {srt_time(t0 + b)}\n{txt}\n")
            k += 1
        t0 += m["dur"]
    os.makedirs("salida", exist_ok=True)
    open("salida/GTA6_subtitulos_es.srt", "w").write("\n".join(lines))

    # mezcla final: música con ducking bajo la voz, normalizado a -14 LUFS (YouTube)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "build/concat.txt",
        "-i", "build/voz.wav", "-i", "build/musica.wav",
        "-filter_complex",
        "[1:a]highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,asplit=2[v][sc];"
        "[2:a]volume=0.32[m];"
        "[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
        "[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "salida/GTA6_video_completo.mp4"], check=True)
    print("OK", total / 60, "min")


if __name__ == "__main__":
    main()
