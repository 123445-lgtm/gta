# GTA 6 — vídeo de YouTube (≈20 min)

Vídeo completo generado de forma automática: guion, locución, imágenes, música y montaje.

## Entregables (`salida/`)
- `GTA6_video_completo.mp4` — vídeo final 1080p30, audio a -14 LUFS (no se versiona en git por tamaño).
- `GTA6_subtitulos_es.srt` — subtítulos en español sincronizados (súbelos a YouTube como CC).
- `miniatura.jpg` — miniatura 1280×720.
- `youtube_titulo_descripcion.txt` — títulos propuestos, descripción con capítulos y etiquetas.
- `guion.md` — guion completo con marcas de tiempo y descripción visual de cada escena.

## Cómo regenerarlo
```bash
pip install piper-tts numpy scipy pillow
# voz: es_ES-davefx-medium (Piper) en /opt/voices/...
python3 voz.py        # locución por frases + tiempos
python3 montaje.py    # imágenes animadas, música, mezcla y SRT
```

- `guion.py` — texto y tipo de visual de cada escena (edítalo y vuelve a ejecutar).
- `visuals.py` — gráficos procedurales originales (estética neón/Vice City, sin material con copyright).
- `musica.py` — música synthwave original sintetizada.
- `montaje.py` — animación (paneo/zoom, entrada de textos, fundidos), mezcla con *ducking* y exportación.
