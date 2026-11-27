# Fábrica de reels con Claude Code

Sistema para producir **reels verticales en español (1080×1920)** con un equipo de agentes de Claude Code, voces de IA locales verificadas y vídeo generado por código (HyperFrames + three.js + GSAP). Incluye la **serie GTA 6** (reels 03–08) como ejemplo completo y reutilizable.

> Repositorio privado para compartir el método con amigos. No incluye vídeos, audios ni voces clonadas: solo código, guiones y guías. Para rehacer un reel necesitas generar tu propia voz (ver más abajo).

## Qué hay aquí

| Ruta | Qué es |
|---|---|
| `CLAUDE.md` | Instrucciones que Claude Code lee al abrir la carpeta: pipeline completo, comandos y reglas de calidad. **Empieza por aquí.** |
| `.claude/agents/` | El equipo de agentes (mitología griega): `hermes` (estrategia y guiones), `atenea` (investigación y verificación), `eco` (voz y audio), `hefesto` (vídeo), `argos` (revisión de calidad), `dedalo` (web), `mnemosine` (conocimiento/documentos), `prometeo` (herramientas). |
| `reels/serie/` | Builder compartido de la serie GTA: `serie.py` (clase `Reel`: tiempos por palabra, subtítulos, SFX, mundo 3D), `mundo_base.js` (Leonida al atardecer), `ayudas.js` (cámara, etiquetas 3D), `herramientas/` (transcripción, acento, similitud de voz, tiempos por palabra) y `PROMPT-serie-gta.md` (prompt listo para pegar en una sesión nueva y hacer otro reel). |
| `reels/reel-0X/` | Cada reel: `guion.md` (guion, fuentes, análisis), `voz/frases.txt` + scripts de voz, `video/fuente/construir.py` (genera el HTML del vídeo) y `tiempos.json`/`palabras.json`. |
| `perfil/perfil.html` | La foto de perfil de la cuenta, dibujada en SVG. |
| `skills-lock.json` | Lista exacta de las skills de terceros que usa el sistema (repositorio y commit de cada una). |

## Cómo se hace un reel (resumen)

Cadena del equipo: **hermes → atenea → eco → hefesto → argos**.

1. **Idea y guion** (hermes): formato lista "7 cosas", gancho directo, contador 1/7, cierre en bucle. Una frase por línea en `voz/frases.txt`, números en letra.
2. **Verificación** (atenea): cada dato con fuente y nivel de confianza; nada de rumores como hechos.
3. **Voz línea a línea** (eco): `generar_frases.py` prueba varias semillas, transcribe cada toma y se queda la que coincide con el texto; luego `acento.py` (probabilidad de inglés ≲ 0,001), `unir_frases.py` (pausas y `tiempos.json`) y `transcribir_palabras.py` (`palabras.json`).
4. **Vídeo** (hefesto): `construir.py` usa `reels/serie/` y genera `index.html` + `compositions/`. Nunca se editan a mano los HTML generados.
5. **Revisar, renderizar, capturar** (hefesto + argos): `check`, `snapshot`, render, capturas del MP4 final, loudness −14/−15 LUFS, copia móvil < 30 MB.

Los detalles y comandos exactos están en `CLAUDE.md` y en `reels/serie/PROMPT-serie-gta.md`.

## Instalación (Windows 11)

1. **Claude Code** (CLI o app de escritorio) y abrir esta carpeta.
2. **Node.js 20+**, **Python 3.12/3.13** (en Windows usa `python`, no `python3`), **ffmpeg** en el PATH, **git**.
3. **Skills**: instala las de `skills-lock.json` en `.claude/skills/` con la CLI `skills` (desactiva telemetría):
   ```bash
   DO_NOT_TRACK=1 DISABLE_TELEMETRY=1 npx skills add <repositorio> 
   ```
   Repositorios usados: `heygen-com/hyperframes` (hyperframes, hyperframes-cli, hyperframes-registry, media-use…), `greensock/gsap-skills`, `Leonxlnx/earshot` (earshot, real-sound), `Leonxlnx/taste-skill`, `LottieFiles/motion-design-skill`, `Ootto-AI/claude-content-skills` (reel-analyzer, reel-scripter, viral-hook-writer…), `vyralcontent/content-skills`, `coreyhaines31/marketingskills`, `delphi-ai/animate-skill`, `remotion-dev/skills`, `obsidianmd/obsidian-skills`, `NicholasSpisak/second-brain`. Aparte (no están en el lock): `impeccable`, `onetake`, `collage-broll-explainers`. Revisa la licencia y el código de cada skill antes de instalarla.
4. **Voz**: el sistema usa **VoiceStudio** (TTS local, CLI `voicestudio`) y su Python con `faster-whisper` y SpeechBrain para acento/similitud; y el modelo **Parakeet** de **OpenWhispr** para comprobar cada toma. Crea tu propia voz (diseñada o clonada **solo de una voz tuya o con permiso**) y pasa siempre `--seed` (la semilla 42 da acento inglés).
5. **Telemetría**: mantenla apagada en HyperFrames y en `npx skills`.

### Rutas que tendrás que adaptar a tu PC

El código se escribió para una máquina concreta y tiene algunas rutas fijas:

| Archivo | Ruta a cambiar |
|---|---|
| `reels/serie/herramientas/transcribe.js` | `D:/openwhispr-dev/...` (OpenWhispr y su `sherpa-onnx`) |
| `reels/serie/herramientas/acento.py`, `transcribir_palabras.py`, `similitud.py` | modelo `faster-whisper` dentro de la carpeta de VoiceStudio |
| `reels/reel-0X/voz/generar_frases.py` | ruta a `reels/serie` |
| `CLAUDE.md`, `.claude/agents/*.md`, `PROMPT-serie-gta.md` | `D:\El Claudio\MODEL 2` y `D:\Skills y Modelos Locales\...` |

Lo más fácil: abre la carpeta en Claude Code y pídele *"adapta las rutas de este repo a mi PC"*.

## Rehacer un reel de ejemplo

```bash
cd reels/reel-06/video
# genera tu voz para voz/frases.txt (paso 3) y copia voz-final.wav a assets/audio/voz.wav,
# tiempos.json y palabras.json a fuente/; añade musica.wav y los SFX a assets/audio/
PYTHONIOENCODING=utf-8 python fuente/construir.py
node "<ruta>/.claude/skills/hyperframes/scripts/plugin-cli.mjs" check
node "<ruta>/.claude/skills/hyperframes/scripts/plugin-cli.mjs" render -q delivery -o ../reel-06.mp4
```

Los SFX se pueden recrear con `earshot make --sound <nombre> -o archivo.wav`.

## Avisos

- Los datos de los guiones de GTA 6 son de noviembre de 2026 y llevan sus fuentes en cada `guion.md`; los easter eggs los encontraron jugadores, no los confirmó Rockstar.
- `reels/reel-06/guion.md` analiza un reel ajeno como referencia de formato; no se incluye ese vídeo.
- No uses voces clonadas de otras personas sin su permiso.
