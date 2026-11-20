# -*- coding: utf-8 -*-
"""Música de fondo synthwave original, sintetizada con numpy (libre de derechos)."""
import sys, wave
import numpy as np

SR = 44100
BPM = 96
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(7)


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


def saw(f, t):
    return 2 * ((f * t) % 1) - 1


def lowpass(x, a):
    y = np.empty_like(x)
    acc = 0.0
    # filtro de un polo vectorizado por bloques (suficiente para pads)
    from scipy.signal import lfilter  # noqa
    return lfilter([a], [1, a - 1], x)


# Progresión: Am - F - C - G (2 compases cada uno)
CHORDS = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
BASS = [45, 41, 48, 43]


def render(seconds):
    n = int(seconds * SR) + SR
    out = np.zeros((n, 2))
    bars = int(seconds / BAR) + 2
    t_bar = np.arange(int(BAR * SR)) / SR
    for b in range(bars):
        start = int(b * BAR * SR)
        ci = (b // 2) % 4
        section = (b // 16) % 4  # 0 intro suave, 1 completo, 2 sin batería, 3 completo
        if b < 4 or start >= n:
            section = 0
        if start >= n:
            break
        seg = slice(start, min(n, start + len(t_bar)))
        L = seg.stop - seg.start
        t = t_bar[:L]
        # pad
        pad = np.zeros(L)
        for m in CHORDS[ci]:
            for det in (-0.08, 0.08):
                pad += saw(note(m + 12 * 0) * (1 + det / 100 * 10), t)
        pad = lowpass(pad, 0.04) * 0.10
        env = np.minimum(1, t / 0.3) * np.minimum(1, (BAR - t) / 0.3 + 0.3)
        pad *= env
        out[seg, 0] += pad
        out[seg, 1] += np.roll(pad, 300)
        if section in (1, 2, 3):
            # bajo en corcheas
            for k in range(8):
                s0 = int(k * BEAT / 2 * SR)
                ln = int(BEAT / 2 * SR * 0.9)
                if s0 >= L:
                    break
                tt = np.arange(min(ln, L - s0)) / SR
                f = note(BASS[ci] - 12 + (12 if k % 4 == 3 else 0))
                v = lowpass(saw(f, tt), 0.15) * np.exp(-tt * 6) * 0.22
                out[start + s0:start + s0 + len(tt)] += v[:, None]
            # arpegio en semicorcheas
            arp = CHORDS[ci] + [CHORDS[ci][0] + 12]
            for k in range(16):
                s0 = int(k * BEAT / 4 * SR)
                if s0 >= L:
                    break
                tt = np.arange(min(int(BEAT / 4 * SR), L - s0)) / SR
                f = note(arp[k % 4] + 12)
                v = np.sign(np.sin(2 * np.pi * f * tt)) * np.exp(-tt * 18) * 0.035
                pan = 0.5 + 0.4 * np.sin(k / 3)
                out[start + s0:start + s0 + len(tt), 0] += v * (1 - pan)
                out[start + s0:start + s0 + len(tt), 1] += v * pan
        if section in (1, 3):
            for k in range(4):
                s0 = int(k * BEAT * SR)
                if s0 >= L:
                    break
                tt = np.arange(min(int(0.4 * SR), L - s0)) / SR
                kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.45
                out[start + s0:start + s0 + len(tt)] += kick[:, None]
                if k % 2 == 1:
                    sn = rng.standard_normal(len(tt)) * np.exp(-tt * 14) * 0.16
                    sn = lowpass(sn, 0.5)
                    out[start + s0:start + s0 + len(tt)] += sn[:, None]
                for h in (0.5,):
                    s1 = s0 + int(h * BEAT * SR)
                    th = np.arange(min(int(0.05 * SR), max(0, L - s1))) / SR
                    if len(th):
                        hh = rng.standard_normal(len(th)) * np.exp(-th * 80) * 0.05
                        hh = hh - lowpass(hh, 0.3)
                        out[start + s1:start + s1 + len(th)] += hh[:, None]
    out = out[:int(seconds * SR)]
    # fundido de entrada y salida
    fi, fo = int(2 * SR), int(5 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]
    out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    out /= np.max(np.abs(out)) + 1e-9
    return (out * 0.8 * 32767).astype(np.int16)


if __name__ == "__main__":
    secs = float(sys.argv[1])
    a = render(secs)
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
