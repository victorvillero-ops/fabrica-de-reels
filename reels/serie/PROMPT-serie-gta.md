# Prompt — nuevo reel de la serie GTA 6

> Copia todo lo que hay debajo de la línea en una sesión nueva (abierta en `D:\El Claudio\MODEL 2`) y rellena el tema al final.

---

Vamos a hacer un **nuevo reel de la serie GTA 6** (reels 03, 04 y 05 ya están hechos y aprobados). Respóndeme en español. Lee primero `CLAUDE.md` y, como referencia viva, `reels/serie/serie.py`, `reels/serie/ayudas.js`, `reels/serie/mundo_base.js` y `reels/reel-05/video/fuente/construir.py` (el más reciente; el 04 usa `SLAB_JS` para losas con años). Copia la estructura del reel anterior, no la inventes de cero.

## Formato y estilo (fijo en toda la serie)

- Vertical 1080×1920, ~40–50 s, voz en español neutro, voz **Historiador** de VoiceStudio (la misma de los reels 03–05).
- Mundo 3D en three.js: **Leonida al atardecer** (cielo morado→rosa→naranja, sol con franjas, mar oscuro con reflejo, paseo, skyline con ventanas encendidas, palmeras). Lo da `mundo_base.js`; cada reel añade su propio "set" encima (en el 05, una isla que sube del mar con regiones y props; en el 04, una línea de tiempo con losas sobre el paseo).
- Paleta: rosa `#FF3D8B`, oro `#FFC94A`, morado `#2A0B4A`/`#1B0B3A`, rojo de sello `#FF3B3B`. Tipos: Montserrat 900 y Inter 800.
- Gráficos (clases de `serie.py`):
  - `.tag` = etiqueta anclada a un punto 3D con `pin()`, título en oro + `<small>` en placa morada (p. ej. "VICE CITY" / "= Miami").
  - `.big` = texto grande centrado; dentro, `.grad` (oro), `.plate` (placa rosa) o `.stamp` (sello rojo girado, para "NO EXISTE", "RETRASADO"…).
- Subtítulos: MAYÚSCULAS blancas, 76 px, banda fija y 300–490 px, grupos de ≤3 palabras que entran con pop palabra a palabra; palabras clave en oro (`HL`).
- Sonido: música `musica.wav` al 0.12 (la misma de los reels 03–05) + SFX en momentos exactos de palabra: `barrido-1/2/largo` en cada cambio de escena, `pop-1/2` en cada dato o etiqueta, `sello` en sellos, `impacto` en el clímax, `subida-1` al arranque, más foley temático (`agua`, `lancha`…). Reutiliza los WAV de `reels/reel-0X/video/assets/audio/`; si falta uno, `earshot make --sound <nombre> -o archivo.wav`.
- CTA final: pregunta en pantalla grande (`bg-cta`), última línea sin subtítulo (`None` en `CAPS`).

## Estructura del guion

1. **Gancho** (línea 0): afirmación chocante o paradoja que se entiende sin sonido en 2 s ("Leonida no existe. Pero casi todo en ella es real.").
2. **Escalada de datos**: un dato nuevo o más sorprendente cada 3–5 s; un giro de tensión hacia los 8–10 s ("Pero lo más loco no es eso").
3. **Remate** + **CTA binaria o de elección** para comentarios ("¿Cuál visitarías primero?").
4. 12–15 líneas, una frase hablada por línea. Cada dato con fuente; lo que sea estimación se dice como estimación ("se estima"). Guarda guion + fuentes en `reels/reel-NN/guion.md`.

Encadena el equipo como siempre: **hermes** (guion/gancho) → **atenea** (verificar cada cifra con fuentes) → **eco** (voz) → **hefesto** (vídeo) → **argos** (revisión), o hazlo tú siguiendo estos pasos.

## Pipeline paso a paso

Carpeta nueva `reels/reel-NN/` copiando `voz/generar_frases.py` y `voz/unir_frases.py` del reel anterior y `video/` (hyperframes.json, meta.json con el id nuevo, `assets/audio/` con música y SFX, `fuente/construir.py` como plantilla).

1. **Guion** → `voz/frases.txt`, una línea por frase. Escribe los números en letra cuando importe cómo se pronuncian ("dos mil dos", "ciento cinco").
2. **Voz línea a línea** (desde `voz/`):
   ```bash
   PYTHONIOENCODING=utf-8 python generar_frases.py frases.txt Historiador frases "D:/El Claudio/MODEL 2/reels/serie/herramientas/transcribe.js"
   ```
   Prueba las semillas `SEEDS` (por defecto 3,8,14,21,29; **nunca la 42**, da acento inglés), transcribe cada toma con Parakeet y se queda la mejor (para en ≥0.97). Revisa `frases/informe.json`: toda línea debe estar ≈1.0; si una baja, bórrala (`fNN.wav`) y regenera con otras semillas (`SEEDS=33,41,57 …`).
3. **Unir**: ajusta en `unir_frases.py` `SCENE_STARTS` (líneas que abren escena → pausa 0.42 s; resto 0.22 s) y la cola (`total = t + 1.2`). `python unir_frases.py` → `voz-final.wav` + `tiempos.json`.
4. **Acento y palabras** con el Python de VoiceStudio (`"$APPDATA/VoiceStudio/runtime/project/.venv/Scripts/python.exe"`):
   - `../../serie/herramientas/acento.py "frases/f*.wav"` → la probabilidad de inglés de cada línea debe quedar ≲0.001. Si alguna sale alta, regenérala con otra semilla.
   - `../../serie/herramientas/transcribir_palabras.py voz-final.wav palabras.json` (tiempos por palabra).
5. **Copiar al vídeo**: `voz-final.wav` → `video/assets/audio/voz.wav`; `tiempos.json` y `palabras.json` → `video/fuente/`.
6. **construir.py** (no edites nunca `index.html` ni `compositions/*.html`: se generan):
   - `R = Reel(Path(__file__).parent)`; diccionario `K` con los tiempos clave: `R.ls(i)` (inicio de línea), `R.wt(i, "palabra", ["alias", "2002"], nth=…)` (momento exacto en que se dice una palabra; los alias cubren cómo la escribió Whisper, cifras incluidas). Si falla, el error lista las palabras oídas en esa línea: añade el alias.
   - `body`: los `.tag` y `.big` en HTML. Los `.big` se colocan con `top` entre ~860 y ~1040 px.
   - `sets_js`: geometría propia del reel (usa `seeded()` para aleatorio determinista, `canvasTex`, `bGeo`, `winTex`, `palm()`).
   - `keys_js`: lista `keys = [[t, [pos], [lookAt]], …]` de la cámara; dos claves por escena (llegada y leve deriva) para que nunca esté quieta; `camAt` interpola con smoothstep.
   - `render_js`: todo función pura de `t` (HyperFrames salta a cualquier frame): `pin("id", x, y, z, win(t, a, b))`, `riseIn`, `grow`, opacidades con `win()`. Nada de `Date.now()`, `Math.random()` ni estado acumulado.
   - `overlay_js`: tweens GSAP de los `.big` sobre `tl` en los tiempos de `K` (sello: `scale 1.8→1`, `power4.out`, 0.18 s; placa: `y 20→0`, 0.25 s; CTA: `back.out`).
   - `R.sfx(t, "archivo.wav", vol)` para cada sonido; `CAPS` (texto de subtítulo por línea, puede diferir de la locución, p. ej. cifras "2002", "105") y `HL` (palabras en oro, en minúscula y con su puntuación pegada, como aparecen en `CAPS`).
   - Cierra con `R.write(R.mundo(body, sets_js, keys_js, render_js, overlay_js, K), R.subs(CAPS, HL))`.
   - Si una mejora sirve para toda la serie, va en `reels/serie/` (afecta a todos los reels al reconstruir).
7. **Comprobar y renderizar** (desde `reels/reel-NN/video`):
   ```bash
   HF="/d/El Claudio/MODEL 2/.claude/skills/hyperframes/scripts/plugin-cli.mjs"
   PYTHONIOENCODING=utf-8 python fuente/construir.py
   node "$HF" check                      # debe terminar en "Check passed"
   node "$HF" snapshot --at 3,9,15,21,27,33,39
   node "$HF" render -q delivery -o "../reel-NN-gta6-<tema>.mp4"
   ```
   Telemetría de HyperFrames apagada; no envíes feedback ni informes de uso.
8. **Capturas del MP4 final** (no solo del snapshot): extrae fotogramas en cada escena con ffmpeg y míralos. Corrige y vuelve a renderizar si algo:
   - pisa la banda de subtítulos (y 300–490) o queda debajo de ~1248 px (UI de Instagram/TikTok);
   - se corta en los bordes (márgenes x 200–880 para etiquetas; `pin()` ya las limita a x 200–880, y 690–1230);
   - se solapa con otra etiqueta o `.big` al mismo tiempo, o una etiqueta apunta a un objeto fuera de cuadro.
9. **Audio medido** (no lo puedo oír, dilo así): `ffmpeg -nostats -i reel.mp4 -af ebur128=peak=true -f null -` → integrado ≈ −14/−15 LUFS, pico < −1 dBTP.
10. **Copia para el móvil** (< 30 MB) y envíamela:
    ```bash
    ffmpeg -y -i reel-NN-gta6-<tema>.mp4 -c:v libx264 -crf 25 -maxrate 4.5M -bufsize 9M -preset slow -c:a aac -b:a 160k -movflags +faststart reel-NN-gta6-<tema>-movil.mp4
    ```
11. Pasa el reel a **argos** para una revisión independiente (solapes, sincronía subtítulo/voz, duración, loudness, datos) antes de darlo por terminado.

## Gotchas de Windows

`PYTHONIOENCODING=utf-8` al imprimir español; `python` (no `python3`); rutas con espacios siempre entre comillas; en heredocs de Python usa barras `/`.

## Tema del nuevo reel

**Reel NN — [tema]:** [idea, ángulo o datos que quiero contar]
