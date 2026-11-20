# -*- coding: utf-8 -*-
"""Corta la locución de ElevenLabs (un MP3 por capítulo, con pausas de 2,5 s entre escenas)
en un WAV por escena y estima los tiempos de cada frase para los subtítulos."""
import json, os, re, subprocess
import numpy as np
from guion import ESCENAS

SR = 44100
SRC = "build/el"
OUT = "build/audio"
os.makedirs(OUT, exist_ok=True)
PAUSA_INI, PAUSA_FIN = 0.4, 0.6


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)


def silences(x, min_len, thr_db=-40):
    """Devuelve (inicio, fin) en muestras de los tramos silenciosos."""
    hop = int(SR * 0.01)
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-9) / 32768
    db = 20 * np.log10(rms + 1e-9)
    quiet = db < thr_db
    out, start = [], None
    for i, q in enumerate(quiet):
        if q and start is None:
            start = i
        elif not q and start is not None:
            if (i - start) * 0.01 >= min_len:
                out.append((start * hop, i * hop))
            start = None
    if start is not None and (n - start) * 0.01 >= min_len:
        out.append((start * hop, n * hop))
    return out


def frases(t):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+", t) if f.strip()]


def trim(x):
    s = silences(x, 0.05, -45)
    a, b = 0, len(x)
    if s and s[0][0] == 0:
        a = s[0][1]
    if s and s[-1][1] >= len(x) - int(SR * 0.02):
        b = s[-1][0]
    return x[max(0, a - int(SR * .03)):min(len(x), b + int(SR * .08))]


blocks = json.load(open(f"{SRC}/blocks.json"))
meta = []
for k, b in enumerate(blocks):
    x = load(f"{SRC}/b{k:02d}.mp3")
    gaps = [((g[0] + g[1]) // 2) for g in silences(x, 1.6) if g[0] > 0 and g[1] < len(x)]
    # posiciones esperadas de cada corte según la longitud del texto
    lens = [len(ESCENAS[i]["texto"]) for i in b]
    speech = len(x) - len(gaps) * 2.5 * SR
    est, acc = [], 0
    for j in range(len(b) - 1):
        acc += lens[j]
        est.append(acc / sum(lens) * speech + j * 2.5 * SR)
    cuts_mid = []
    small = [((a + c) // 2, c - a) for a, c in silences(x, 0.12)]
    for j, e in enumerate(est):
        cand = [g for g in gaps if abs(g - e) < 12 * SR and g not in cuts_mid]
        if cand:
            cuts_mid.append(min(cand, key=lambda g: abs(g - e)))
        else:
            near = [s for s in small if abs(s[0] - e) < 4 * SR and s[0] not in cuts_mid]
            pick = min(near, key=lambda s: abs(s[0] - e) - s[1])[0] if near else int(e)
            print(f"bloque {k}: corte {j} estimado ({pick / SR:.1f}s)")
            cuts_mid.append(pick)
    if len(gaps) > len(b) - 1:
        print(f"bloque {k}: {len(gaps)} pausas largas para {len(b) - 1} cortes")
    cuts = [0] + sorted(cuts_mid) + [len(x)]
    for j, i in enumerate(b):
        seg = trim(x[cuts[j]:cuts[j + 1]])
        dur_voz = len(seg) / SR
        # tiempos de frase: reparto por caracteres, ajustado al silencio más cercano
        fr = frases(ESCENAS[i]["texto"])
        tot = sum(len(f) for f in fr)
        sil = [((a + c) / 2) / SR for a, c in silences(seg, 0.15, -38)]
        bounds, acc = [0.0], 0
        for f in fr[:-1]:
            acc += len(f)
            est = acc / tot * dur_voz
            near = min(sil, key=lambda s: abs(s - est)) if sil else est
            bounds.append(near if abs(near - est) < 2.0 and near > bounds[-1] + 0.4 else est)
        bounds.append(dur_voz)
        subs = [(PAUSA_INI + bounds[m], PAUSA_INI + bounds[m + 1], f) for m, f in enumerate(fr)]
        audio = np.concatenate([np.zeros(int(PAUSA_INI * SR)), seg, np.zeros(int(PAUSA_FIN * SR))])
        path = f"{OUT}/{i:03d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", path],
                       input=audio.astype(np.int16).tobytes(), check=True)
        meta.append({"i": i, "wav": path, "dur": len(audio) / SR, "subs": subs})

meta.sort(key=lambda m: m["i"])
json.dump(meta, open("build/audio_meta.json", "w"), ensure_ascii=False, indent=1)
print(f"TOTAL {sum(m['dur'] for m in meta) / 60:.2f} min, {len(meta)} escenas")
