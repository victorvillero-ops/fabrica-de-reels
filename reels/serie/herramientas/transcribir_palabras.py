"""Transcribe an audio/video file with word-level timestamps; writes <out>.json and prints segments."""
import sys, json
from faster_whisper import WhisperModel

MODEL = r"D:\Skills y Modelos Locales\VoiceStudio\Modelos (OmniVoice Local)\hf_cache\models--deepdml--faster-whisper-large-v3-turbo-ct2\snapshots\4df90f75321148c3a29a9e2351b7ddf8f5b115a8"
src, out = sys.argv[1], sys.argv[2]
model = WhisperModel(MODEL, device="cpu", compute_type="int8")
segments, info = model.transcribe(src, language="es", word_timestamps=True, beam_size=5, vad_filter=False)
data = {"language": info.language, "duration": info.duration, "segments": []}
for s in segments:
    data["segments"].append({
        "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
        "words": [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for w in (s.words or [])],
    })
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}", flush=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
