"""Generate each line with VoiceStudio, verify it with Parakeet, retry other seeds, keep the best.

Usage: python generar_frases.py frases.txt <voice> <outdir> <transcribe.js>
Writes <outdir>/fNN.wav and <outdir>/informe.json (text, heard, score, seed per line).
"""
import difflib, json, re, subprocess, sys, unicodedata
sys.path.insert(0, 'D:/El Claudio/MODEL 2/reels/serie')
from numeros_es import expandir
from pathlib import Path

NUM = {"1": "uno", "2": "dos", "4": "cuatro", "7": "siete", "80": "ochenta", "120": "ciento veinte",
       "500": "quinientos", "1500": "mil quinientos", "1.500": "mil quinientos", "85": "ochenta y cinco"}

def norm(s: str) -> list[str]:
    s = expandir(s)
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9. ]", " ", s)
    words = []
    for w in s.split():
        w = w.strip(".")
        words.extend(NUM.get(w, w).split())
    return [w for w in words if w]

def heard(wav: Path, tjs: str) -> str:
    raw = wav.with_suffix(".f32")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", str(raw)], check=True)
    out = ""
    for _ in range(3):  # Parakeet occasionally hangs: time out and retry
        try:
            out = subprocess.run(["node", tjs, str(raw)], capture_output=True, text=True, encoding="utf-8",
                                 cwd=str(wav.parent), timeout=150).stdout
        except subprocess.TimeoutExpired:
            print("  transcripción colgada, reintento", flush=True); continue
        if "TEXTO:" in out: break
    raw.unlink(missing_ok=True)
    m = re.search(r"TEXTO: (.*)", out)
    return m.group(1).strip() if m else ""

SEEDS = tuple(int(x) for x in __import__("os").environ.get("SEEDS", "3,8,14,21,29").split(","))

def main():
    lines = [l.strip() for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()]
    voice, outdir, tjs = sys.argv[2], Path(sys.argv[3]).resolve(), sys.argv[4]
    outdir.mkdir(parents=True, exist_ok=True)
    report = []
    for i, text in enumerate(lines):
        if (outdir / f"f{i:02d}.wav").exists():
            print(f"{i:02d} ya generada", flush=True); continue
        best = None
        for seed in SEEDS:
            wav = outdir / f"f{i:02d}-s{seed}.wav"
            subprocess.run(["voicestudio", "speak", "--voice", voice, "--language", "es", "--seed", str(seed),
                            "-o", str(wav), "--overwrite", text], capture_output=True)
            h = heard(wav, tjs)
            score = difflib.SequenceMatcher(None, norm(text), norm(h)).ratio()
            if best is None or score > best["score"]:
                best = {"i": i, "text": text, "heard": h, "score": round(score, 3), "seed": seed, "wav": wav.name}
            if score >= 0.97:
                break
        final = outdir / f"f{i:02d}.wav"
        (outdir / best["wav"]).replace(final)
        for extra in outdir.glob(f"f{i:02d}-s*.wav"):
            extra.unlink()
        best["wav"] = final.name
        report.append(best)
        print(f"{i:02d} {best['score']:.2f} s{best['seed']:<3} {best['heard']}", flush=True)
    (outdir / "log.txt").unlink(missing_ok=True)
    (outdir / "informe.json" if report else outdir / "_vacío.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

main()
