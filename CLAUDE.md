# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this workspace is

Not a single app: a Windows 11 workspace for producing **Spanish-language vertical reels** (1080×1920) with AI voices and code-rendered video. The user writes in Spanish; reply in Spanish. It is not a git repository.

| Path | What it is |
|---|---|
| `reels/reel-NN/` | one reel each: `voz/` (voice), `video/` (HyperFrames project), final `.mp4` files next to them |
| `reels/serie/` | shared code for the GTA 6 series (reels 03–05) and `herramientas/` (voice verification helpers) |
| `reels/reel-02/remotion/`, `reels/muestra-motion-canvas/mc/` | one-off comparisons in Remotion and Motion Canvas; HyperFrames is the default |
| `lemo-opuscar/` | separate cloned project with its own `CLAUDE.md` — read that when working inside it |
| `.claude/skills/` | project skills (HyperFrames, earshot, viral/reel skills, impeccable, taste, Obsidian…). Several are symlinks into `.agents/skills/`, installed with `npx skills add` (see `skills-lock.json`) |
| `ATLAS/` | empty on purpose (a shelved project) |
| `package.json` | only `matter-js`; no scripts |

External tools live outside the repo: VoiceStudio (CLI `voicestudio`), the voice repository `D:\Skills y Modelos Locales\Voces\` (read its `LEEME - Repositorio de voces.md`), OpenWhispr at `D:\openwhispr-dev` (its Parakeet model is used for transcription checks), yt-dlp, Obsidian, ComfyUI, ffmpeg.

## Agent team (`.claude/agents/`)

The user named the team after Greek mythology and refers to agents by these names:

| Agent | Role |
|---|---|
| `hermes` | content strategy: ideas, trends, hooks, reel scripts, captions, calendars |
| `atenea` | research and fact-checking (read-only, sourced briefs) |
| `eco` | voice and audio: VoiceStudio voiceovers and clones with verification, SFX, music |
| `hefesto` | video production: HyperFrames, GTA series builder, Lemo-Opuscar, onetake, Motion Canvas, Manim |
| `argos` | independent quality review of videos, voice, pages, facts |
| `dedalo` | web and UI design/build (hands finishing to the `impeccable-*` agents) |
| `mnemosine` | knowledge (Obsidian, second brain) and office documents |
| `prometeo` | finding, reviewing and installing skills/tools (installs only with approval) |

Typical reel chain: hermes → atenea → eco → hefesto → argos.

## Reel pipeline (how a reel is made)

1. **Script** → `reels/reel-NN/voz/frases.txt`, one spoken line per row (numbers may be digits; checks expand them to Spanish words). It must pass `reels/serie/herramientas/revisar_guion_voz.py`:
   - no lone lines of 1–3 words;
   - spelled letters separated by "...";
   - foreign words inside a sentence;
   - nothing over 30 words.
   The reasons are in `investigacion-voz/informe-voicestudio.md`.
2. **Voice, line by line** — `reels/serie/herramientas/generar_frases.py frases.txt <voice> frases <transcribe.js>` (the shared generator; older reels keep their own copies):
   - calls `voicestudio speak` with several seeds (`SEEDS`/`EXTRA` env);
   - checks each take for text (Parakeet ≥0.97), accent (≤0.001), speaking rate (±20 %) and stray pauses (`calidad_voz.py`);
   - resumes past existing `frases/fNNN.wav`; `ONLY=… REHACER=1` regenerates lines with untried seeds.
   Then run `revisar_voz.py frases frases.txt`. It measures the accent of short lines with their neighbours, prints what to regenerate and lists the lines to listen to.
3. **Join** — `voz/unir_frases.py` trims silences, places lines with gaps (longer at the line indices in `SCENE_STARTS`), writes `voz-final.wav` and `tiempos.json` (line windows). Edit `SCENE_STARTS` and the tail (`total = t + X`) per reel.
4. **Accent + word timings** — run with VoiceStudio's Python (`$APPDATA/VoiceStudio/runtime/project/.venv/Scripts/python.exe`): `herramientas/acento.py <wavs>` (en-probability must stay ≲0.001) and `herramientas/transcribir_palabras.py voz-final.wav palabras.json`.
5. **Copy into the video project**: `voz-final.wav` → `video/assets/audio/voz.wav`; `tiempos.json` and `palabras.json` → `video/fuente/`.
6. **Build** — `video/fuente/construir.py` generates `index.html`, `compositions/mundo.html` and `compositions/subtitulos.html`. Never hand-edit those generated files; change `construir.py` (or `reels/serie/`) and rebuild.
7. **Check, snapshot, render, verify** (below), then make a phone copy under 30 MB.

### The GTA series builder (`reels/serie/`)

- `serie.py` → `Reel(fuente)` loads `tiempos.json`/`palabras.json`. `R.ls(i)`/`R.le(i)` = line start/end; `R.wt(i, token, alias, nth)` = time a word is spoken in line *i* (aliases cover how Whisper spelled it, e.g. `"3"` for "tres"); `R.sfx(t, file, vol)` queues a sound; `R.mundo(...)` wraps the three.js world; `R.subs(CAPS, HL)` makes uppercase captions (a `None` caption is skipped); `R.write()` writes all three files and assigns audio lanes.
- `mundo_base.js` (renderer, camera, sunset sky, sea, skyline, palms) and `ayudas.js` (`camAt` camera keys, `pin()` labels projected from 3D, `win()` fade windows, `grow()`) are inlined into every reel's `mundo.html`. Editing them changes every reel on its next rebuild.
- Animation is driven by one GSAP proxy tween that calls `render(clock.t)`; everything must be a pure function of time (HyperFrames seeks frames).
- `pin()` clamps labels to x 200–880, y 690–1230 so they never sit in the caption band (y 300–480) or under platform UI (below ~1248).

## Commands

Run HyperFrames through the skill's CLI, from the reel's `video/` folder:

```bash
HF="/d/El Claudio/MODEL 2/.claude/skills/hyperframes/scripts/plugin-cli.mjs"
cd reels/reel-05/video
PYTHONIOENCODING=utf-8 python fuente/construir.py        # rebuild generated HTML
node "$HF" check                                          # must end "Check passed" (0 errors)
node "$HF" snapshot --at 9,19,29,39                       # contact sheet in .hyperframes/artifacts/snapshots/<id>/
node "$HF" render -q delivery -o "../reel-05-nombre.mp4"  # ~1.5–2 min for 45 s
```

Phone copy and loudness:

```bash
ffmpeg -y -i in.mp4 -c:v libx264 -crf 25 -maxrate 4.5M -bufsize 9M -preset slow -c:a aac -b:a 160k -movflags +faststart in-movil.mp4
ffmpeg -nostats -i in.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"   # reels sit around -14/-15 LUFS
```

SFX come from `earshot make --sound <name> -o file.wav` (reuse the WAVs already in earlier reels' `video/assets/audio/` when they fit).

## Expectations the user has stated

- **Verify voices properly**: transcription match *and* accent score per line; the user rejects "Spanglish" voices by ear. VoiceStudio's default seed (42) gives an English accent — always pass `--seed`.
- **After every render, take captures** of the final MP4 and fix any label/graphic overlapping captions or edges, then re-render.
- Send deliverables to the user's phone (copy < 30 MB). Audio is measured, not heard — say so.
- Cloned voices (e.g. "Clon MK1"): only from a voice the user owns or has permission for; keep the real recording as reference (locking replaces it with a generated take and lowers similarity); verify with `herramientas/similitud.py` (SpeechBrain ECAPA vs held-out stretches of the source).
- Telemetry: keep HyperFrames telemetry off and never send feedback/usage reports from tools; run `npx skills` with `DO_NOT_TRACK=1 DISABLE_TELEMETRY=1`.
- Before installing a skill or tool, review its code/licence for paid APIs, network calls and telemetry, and tell the user what it needs.

## Windows gotchas

- Console encoding is cp1252: set `PYTHONIOENCODING=utf-8` when Python prints Spanish/Chinese text, and open files with `encoding="utf-8"`.
- `python3` is the Microsoft Store stub here; use `python` (3.13 default, 3.12 via `py -3.12`).
- Paths contain spaces (`D:\El Claudio\MODEL 2`, `D:\Skills y Modelos Locales`): always quote them. In heredocs passed to Python, use forward slashes to avoid stray `\r`/escape issues.
- Some tools install to `D:\Skills y Modelos Locales\` by user preference (yt-dlp, Obsidian, MiKTeX, manimgl venv, ClaudeAnimationBase, motion-canvas); prefer that location for new programs.
