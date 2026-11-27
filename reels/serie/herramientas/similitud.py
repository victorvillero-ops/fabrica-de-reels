"""Speaker similarity (SpeechBrain ECAPA, cosine) of each test take against held-out stretches of the original reel.

Usage: python similitud.py <clon-dir>   (reads reel-original.wav, pruebas/*.wav; prints a table and writes similitud.json)
"""
import json, sys, subprocess, tempfile
from pathlib import Path
import torch, torchaudio
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy

D = Path(sys.argv[1])
model = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                       savedir=str(Path.home() / ".cache" / "ecapa-voxceleb"),
                                       run_opts={"device": "cpu"}, local_strategy=LocalStrategy.COPY)

def load(p: Path) -> torch.Tensor:
    tmp = Path(tempfile.gettempdir()) / "sim16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-ac", "1", "-ar", "16000", str(tmp)], check=True)
    import wave, numpy as np
    with wave.open(str(tmp)) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return torch.from_numpy(a).unsqueeze(0)

def emb(w: torch.Tensor) -> torch.Tensor:
    with torch.no_grad():
        e = model.encode_batch(w).squeeze()
    return e / e.norm()

orig, sr = load(D / "reel-original.wav"), 16000
# held-out stretches (not used as clone references): 40-56 s, 73-90 s, 91-114 s
held = [(40.0, 56.0), (73.0, 90.0), (91.0, 114.0)]
H = [emb(orig[:, int(a * sr):int(b * sr)]) for a, b in held]
target = torch.stack(H).mean(0); target = target / target.norm()
ceiling = [float(H[i] @ H[j]) for i in range(3) for j in range(i + 1, 3)]
print(f"techo (original contra original, tramos distintos): {min(ceiling):.3f}-{max(ceiling):.3f}")

rows = {}
for p in sorted((D / "pruebas").glob("*.wav")):
    rows[p.stem] = round(float(emb(load(p)) @ target), 4)
base = Path(r"D:\Skills y Modelos Locales\Voces\muestras")
for p in sorted(base.glob("*.wav")):
    rows["(otra voz) " + p.stem] = round(float(emb(load(p)) @ target), 4)
for k, v in rows.items():
    print(f"{v:.3f}  {k}")
json.dump({"ceiling": ceiling, "scores": rows}, open(D / "similitud.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
