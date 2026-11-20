# -*- coding: utf-8 -*-
"""Genera la locución (Piper TTS, offline) por frases y guarda tiempos."""
import json, os, re, sys, wave
import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig
from guion import ESCENAS

VOZ = os.environ.get("VOZ", "/opt/voices/vits-piper-es_ES-davefx-medium/es_ES-davefx-medium.onnx")
LS = float(os.environ.get("LENGTH_SCALE", "1.1"))
OUT = "build/audio"
os.makedirs(OUT, exist_ok=True)

voice = PiperVoice.load(VOZ)
SR = voice.config.sample_rate
cfg = SynthesisConfig(length_scale=LS, noise_scale=0.6, noise_w_scale=0.8)

PAUSA_FRASE = 0.28
PAUSA_INI, PAUSA_FIN = 0.5, 0.7


def frases(t):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+", t) if f.strip()]


def synth(t):
    chunks = [c.audio_int16_array for c in voice.synthesize(t, syn_config=cfg)]
    return np.concatenate(chunks) if chunks else np.zeros(0, np.int16)


meta = []
for i, e in enumerate(ESCENAS):
    parts, subs, t = [np.zeros(int(PAUSA_INI * SR), np.int16)], [], PAUSA_INI
    for f in frases(e["texto"]):
        a = synth(f)
        d = len(a) / SR
        subs.append((t, t + d, f))
        parts += [a, np.zeros(int(PAUSA_FRASE * SR), np.int16)]
        t += d + PAUSA_FRASE
    parts.append(np.zeros(int(PAUSA_FIN * SR), np.int16))
    audio = np.concatenate(parts)
    path = f"{OUT}/{i:03d}.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())
    meta.append({"i": i, "wav": path, "dur": len(audio) / SR, "subs": subs})
    print(i, round(len(audio) / SR, 1), file=sys.stderr)

json.dump(meta, open("build/audio_meta.json", "w"), ensure_ascii=False, indent=1)
tot = sum(m["dur"] for m in meta)
print(f"TOTAL {tot/60:.2f} min")
