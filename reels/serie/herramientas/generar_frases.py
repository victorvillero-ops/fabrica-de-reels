"""Shared voice generator (template). Generates each line with VoiceStudio and verifies every take.

Usage (run with VoiceStudio's Python, it has faster_whisper):
  python generar_frases.py frases.txt "<voice>" frases <transcribe.js>
A take passes when ALL of these hold:
  - text score >= 0.97 (Parakeet transcription vs the script),
  - en-probability <= 0.001 (Whisper LID); lines with < 1.2 s of speech are exempt here because LID is
    unreliable on them: revisar_voz.py measures them together with their neighbours afterwards,
  - speaking rate within ±20 % of VEL (syllables/s, default 5.1 = Clon MK1) on lines of 4+ words,
  - no long pause (>= 0.6 s) inside the line beyond the pause marks the text has (commas, colons...).
Checks 3-4 come from calidad_voz.py (see investigacion-voz/informe-voicestudio.md for why).
Base seeds first (SEEDS), then EXTRA seeds if no take passed. Writes <outdir>/fNNN.wav and appends one
JSON per line to <outdir>/informe.jsonl (every take tried, with all scores). Resumes past existing fNNN.wav.
Regenerate lines: ONLY=12,40 REHACER=1 -> deletes those fNNN.wav and skips the seeds already tried for
them (same seed = same audio), so new seeds are used. Blank lines in frases.txt are ignored for numbering.
Before generating, check the script with revisar_guion_voz.py.
"""
import difflib, json, os, re, subprocess, sys, unicodedata
sys.path.insert(0, 'D:/El Claudio/MODEL 2/reels/serie')
sys.path.insert(0, 'D:/El Claudio/MODEL 2/reels/serie/herramientas')
from numeros_es import expandir
import calidad_voz
from pathlib import Path
from faster_whisper import WhisperModel

MODEL = r"D:\Skills y Modelos Locales\VoiceStudio\Modelos (OmniVoice Local)\hf_cache\models--deepdml--faster-whisper-large-v3-turbo-ct2\snapshots\4df90f75321148c3a29a9e2351b7ddf8f5b115a8"
SEEDS = [int(x) for x in os.environ.get("SEEDS", "21,14,3,8,29").split(",")]
EXTRA = [int(x) for x in os.environ.get("EXTRA", "35,47,56,64,77").split(",")]
EN_MAX, OK = 0.001, 0.97
VEL = float(os.environ.get("VEL", calidad_voz.VEL_REF))
EXTRA2 = [91, 103, 117, 131, 149, 163, 177, 191]   # used only when regenerating and the others were tried

# Spanish letter names, used only on lines that spell letters out ("ese, te, e, ene, ...").
LETRAS = {"a": "a", "be": "b", "ce": "c", "de": "d", "e": "e", "efe": "f", "ge": "g", "hache": "h", "i": "i",
          "jota": "j", "ka": "k", "ele": "l", "eme": "m", "ene": "n", "o": "o", "pe": "p", "cu": "q", "erre": "r",
          "ese": "s", "te": "t", "u": "u", "uve": "v", "equis": "x", "zeta": "z"}
# Letters separated by commas or (recommended, see revisar_guion_voz.py) by "..." / "…": "ese... te... e..."
SPELL = re.compile(r"\b(" + "|".join(LETRAS) + r")\s*(?:,|\.\.\.|…)\s*(" + "|".join(LETRAS) + r")\b", re.I)

def norm(s: str, spelled: bool = False) -> list[str]:
    s = expandir(s)
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\bstar\s+dust\b", "stardust", s)
    s = re.sub(r"\b(e?s)?ten\s*(dec|deck|dek|dex)k?\b", "stendec", s)   # Stendec / Stendek / Estén deck
    w = s.split()
    if spelled:
        w = [LETRAS.get(x, x) for x in w]
        out = []
        for x in w:  # collapse runs of single letters into one token: s t e n d e c -> stendec
            if len(x) == 1 and out and out[-1][0] == "#":
                out[-1] += x
            elif len(x) == 1:
                out.append("#" + x)
            else:
                out.append(x)
        w = [x.lstrip("#") for x in out]
    return w

def score(text: str, h: str) -> float:
    sp = bool(SPELL.search(text))
    a, b = norm(text, sp), norm(h, sp)
    # Proper names (capitalised mid-sentence: Checklin, Harmer, Lancastrian...): ASR spells them its own way
    # ("Shecklin"). A heard word close to a name (char ratio >= 0.8) counts as that name.
    names = {w for w in norm(" ".join(re.findall(r"(?<=[\w,;:] )[A-ZÁÉÍÓÚ][\w-]+", text)))}
    if names:
        b = [next((n for n in names if difflib.SequenceMatcher(None, n, x).ratio() >= 0.8), x) for x in b]
    r = difflib.SequenceMatcher(None, a, b).ratio()
    if not sp and r < OK:
        # Word-boundary merges ("la azafata" heard as "la zafata", "de el" as "del"): identical once spaces
        # are removed and doubled letters collapsed. Only an exact match counts, so no missing word slips by.
        sq = lambda ws: re.sub(r"(.)\1+", r"\1", "".join(ws))
        if sq(a) == sq(b):
            r = 1.0
    if sp:
        # The spelled letters must all be there, in order (a missing T is a real error); if they are,
        # also compare with spaces removed so "SCTI AR" and "sctiar" count as the same.
        letters = "".join(LETRAS[x.lower()] for x in re.findall(r"\b(?:" + "|".join(LETRAS) + r")\b(?=\s*[,.])", text, re.I))
        joined = "".join(b)
        if letters and letters in joined:
            r = max(r, difflib.SequenceMatcher(None, "".join(a), joined).ratio())
        else:
            r = min(r, 0.89)
    return r

def heard(wav: Path, tjs: str) -> str:
    raw = wav.with_suffix(".f32")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", str(raw)], check=True)
    out = subprocess.run(["node", tjs, str(raw)], capture_output=True, text=True, encoding="utf-8", cwd=str(wav.parent)).stdout
    raw.unlink(missing_ok=True)
    m = re.search(r"TEXTO: (.*)", out)
    return m.group(1).strip() if m else ""

wm = WhisperModel(MODEL, device="cpu", compute_type="int8")
def en_prob(wav: Path) -> float:
    _, info = wm.transcribe(str(wav), beam_size=1, without_timestamps=True)
    return float(dict(info.all_language_probs or []).get("en", 0.0))

def speak(voice, seed, text, wav):
    for _ in range(3):
        r = subprocess.run(["voicestudio", "speak", "--voice", voice, "--language", "es", "--seed", str(seed),
                            "-o", str(wav), "--overwrite", text], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if wav.exists() and wav.stat().st_size > 1000:
            return True
        print(f"   speak falló (s{seed}): {r.stderr.strip()[:200]}", flush=True)
    return False

def acc_ok(t):
    return t["en"] <= EN_MAX or t.get("corta", False)

def pick(takes):
    passed = [t for t in takes if t["pass"]]
    if passed:
        return max(passed, key=lambda t: (t["score"], -t["en"]))
    # No take passed everything: prefer accent, then text, then the quality checks.
    ok_acc = [t for t in takes if acc_ok(t)]
    if ok_acc:
        return max(ok_acc, key=lambda t: (t["score"] >= OK, t.get("calidad_ok", True), t["score"], -t["en"]))
    good = [t for t in takes if t["score"] >= 0.90]
    return min(good, key=lambda t: t["en"]) if good else max(takes, key=lambda t: t["score"])

def tried_seeds(outdir, i):
    rep = outdir / "informe.jsonl"
    seeds = set()
    if rep.exists():
        for l in rep.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                if r.get("i") == i:
                    seeds |= {t["seed"] for t in r.get("takes", [])}
    return seeds

def main():
    lines = [l.strip() for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()]
    voice, outdir, tjs = sys.argv[2], Path(sys.argv[3]).resolve(), sys.argv[4]
    outdir.mkdir(parents=True, exist_ok=True)
    only = {int(x) for x in os.environ["ONLY"].split(",")} if os.environ.get("ONLY") else None
    for i, text in enumerate(lines):
        if only is not None and i not in only:
            continue
        final = outdir / f"f{i:03d}.wav"
        if final.exists() and only is not None and os.environ.get("REHACER") == "1":
            final.unlink()
        if final.exists():
            continue
        skip = tried_seeds(outdir, i)
        order = [s for s in SEEDS + EXTRA if s not in skip]
        if skip:
            order += [s for s in EXTRA2 if s not in skip]
        extras = set(EXTRA) | set(EXTRA2)
        takes = []
        for seed in order:
            if seed == 42:
                continue
            if seed in extras and any(t["pass"] for t in takes):
                break
            wav = outdir / f"f{i:03d}-s{seed}.wav"
            if not speak(voice, seed, text, wav):
                continue
            h = heard(wav, tjs)
            sc, en = round(score(text, h), 3), round(en_prob(wav), 5)
            q = calidad_voz.evaluar(text, wav, VEL)
            t = {"seed": seed, "heard": h, "score": sc, "en": en, "wav": wav.name, **q}
            t["pass"] = sc >= OK and acc_ok(t) and q["calidad_ok"]
            takes.append(t)
            why = [] if t["pass"] else [k for k, bad in (("texto", sc < OK), ("acento", not acc_ok(t)),
                                                        ("velocidad", not q["vel_ok"]), ("pausas", not q["pausas_ok"])) if bad]
            print(f"   {i:03d} s{seed:<3} {sc:.3f} en={en:.5f} {q['sil_s']} síl/s"
                  f"{' corta' if q['corta'] else ''}{'  falla: ' + ','.join(why) if why else ''}", flush=True)
            if t["pass"]:
                break
        if not takes:
            print(f"{i:03d} SIN TOMAS", flush=True); continue
        best = pick(takes)
        (outdir / best["wav"]).replace(final)
        for extra in outdir.glob(f"f{i:03d}-s*.wav"):
            extra.unlink()
        rec = {"i": i, "n": i + 1, "text": text, "heard": best["heard"], "score": best["score"], "en": best["en"],
               "seed": best["seed"], "pass": best["pass"], "spelled": bool(SPELL.search(text)),
               "sil_s": best.get("sil_s"), "corta": best.get("corta"), "pausas_largas": best.get("pausas_largas"),
               "takes": takes}
        with open(outdir / "informe.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        flag = "" if best["pass"] else "  <-- REVISAR"
        print(f"{i:03d} {best['score']:.3f} en={best['en']:.5f} s{best['seed']:<3} {best['heard']}{flag}", flush=True)

main()
