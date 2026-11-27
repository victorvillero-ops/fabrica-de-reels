"""Score how natively Spanish each audio sounds: Whisper's language-ID probability for es vs en."""
import sys, glob
from faster_whisper import WhisperModel

MODEL = r"D:\Skills y Modelos Locales\VoiceStudio\Modelos (OmniVoice Local)\hf_cache\models--deepdml--faster-whisper-large-v3-turbo-ct2\snapshots\4df90f75321148c3a29a9e2351b7ddf8f5b115a8"
model = WhisperModel(MODEL, device="cpu", compute_type="int8")

files = [f for a in sys.argv[1:] for f in sorted(glob.glob(a))]
for f in files:
    _, info = model.transcribe(f, beam_size=1, without_timestamps=True)
    probs = dict(info.all_language_probs or [])
    es, en = probs.get("es", 0.0), probs.get("en", 0.0)
    print(f"{es:.4f}\t{en:.4f}\t{f}", flush=True)
