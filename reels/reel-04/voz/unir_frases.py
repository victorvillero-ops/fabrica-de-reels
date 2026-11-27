"""Join the verified line takes into one voiceover with pauses; write tiempos.json (line windows).

Pauses: 0.30 s between lines, 0.55 s where a new scene starts (lines listed in SCENE_STARTS).
"""
import json, subprocess, wave
from pathlib import Path

HERE = Path(__file__).parent
LINES = [l.strip() for l in (HERE / "frases.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
SCENE_STARTS = {1, 3, 5, 7, 9, 11}
LEAD = 0.12  # silence before the first word

def dur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout
    return float(out)

def main():
    parts, t, rows = [], LEAD, []
    tmp = HERE / "_union"; tmp.mkdir(exist_ok=True)
    # Every take normalised to the same format first: 24 kHz mono 16-bit, trimmed of edge silence.
    for i, text in enumerate(LINES):
        src = HERE / "frases" / f"f{i:02d}.wav"
        dst = tmp / f"c{i:02d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
                        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse",
                        "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(dst)], check=True)
        if i > 0:
            gap = 0.42 if i in SCENE_STARTS else 0.22
            t += gap
        d = dur(dst)
        rows.append({"i": i, "text": text, "start": round(t, 3), "end": round(t + d, 3)})
        parts.append((dst, rows[-1]["start"]))
        t += d
    total = t + 2.6
    # Mix every line at its start time onto silence (exact placement, no drift).
    inputs, filters = [], []
    for k, (p, start) in enumerate(parts):
        inputs += ["-i", str(p)]
        ms = int(round(start * 1000))
        filters.append(f"[{k}]adelay={ms}|{ms}[d{k}]")
    mix = "".join(f"[d{k}]" for k in range(len(parts)))
    filters.append(f"{mix}amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters),
                    "-map", "[out]", "-ar", "48000", "-ac", "1", str(HERE / "voz-final.wav")], check=True)
    (HERE / "tiempos.json").write_text(json.dumps({"total": round(total, 3), "lines": rows}, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    for p in tmp.glob("*.wav"): p.unlink()
    tmp.rmdir()
    print(f"total {total:.2f}s")
    for r in rows: print(f"{r['i']:02d} {r['start']:6.2f}-{r['end']:6.2f} {r['text']}")

main()
