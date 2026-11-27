"""Comprobaciones de calidad de una toma de voz, además del texto y el acento.

Nacen del análisis de VoiceStudio/OmniVoice (investigacion-voz/informe-voicestudio.md):
- OmniVoice decide la duración de cada frase con una regla de caracteres, así que algunas frases
  salen aceleradas o arrastradas  -> velocidad().
- A veces rellena el lienzo con una pausa larga a mitad de frase donde no hay coma -> pausas().
- La probabilidad de inglés de Whisper no es fiable en clips de menos de ~1,2 s -> es_corta()
  (el acento de esas frases se mide junto a sus vecinas en revisar_voz.py).

Sin dependencias raras: numpy + wave (el Python de VoiceStudio las tiene).
"""
import re
import wave
from pathlib import Path

import numpy as np

VOCALES = re.compile(r"[aeiouáéíóúü]+", re.I)
PAUSA_TEXTO = re.compile(r"[,;:…—–]|\.{3}|\.(?=\s+\S)|[?!](?=\s+\S)")

VEL_REF = 5.1      # sílabas por segundo: mediana medida con Clon MK1 en STENDEC (278 frases)
VEL_TOL = 0.20     # ±20 % alrededor de la referencia
MIN_PALABRAS_VEL = 4   # en frases más cortas la velocidad no se puede juzgar bien
HUECO_MIN = 0.6    # segundos de silencio interno que cuentan como pausa larga
CORTA_S = 1.2      # por debajo de esta duración de habla, el acento se mide con contexto


def silabas(texto: str) -> int:
    return max(1, len(VOCALES.findall(texto.lower())))


def _leer(wav):
    with wave.open(str(wav)) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    dt = {2: np.int16, 4: np.int32}[sw]
    x = np.frombuffer(raw, dtype=dt).astype(np.float64) / float(np.iinfo(dt).max)
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    return x, sr


def medir(wav) -> dict:
    """Duración de habla (de la primera a la última parte con voz) y pausas internas largas."""
    x, sr = _leer(wav)
    hop = max(1, int(sr * 0.01))
    fr = x[: len(x) // hop * hop].reshape(-1, hop)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    voz = db > (db.max() - 35)
    idx = np.where(voz)[0]
    if not len(idx):
        return {"habla": 0.0, "huecos": []}
    huecos, run, ini = [], 0, 0
    tramo = voz[idx[0]: idx[-1] + 1]
    for k, v in enumerate(tramo):
        if not v:
            if run == 0:
                ini = k
            run += 1
        else:
            if run * 0.01 >= HUECO_MIN:
                huecos.append(round(float(idx[0] + ini) * 0.01, 2))
            run = 0
    return {"habla": round(float(idx[-1] - idx[0] + 1) * 0.01, 2), "huecos": huecos}


def velocidad(texto: str, m: dict, ref: float = VEL_REF, tol: float = VEL_TOL) -> dict:
    """Sílabas por segundo y si está dentro de ±tol de la referencia (solo frases de 4+ palabras)."""
    if not m["habla"]:
        return {"sil_s": None, "vel_ok": False}
    v = silabas(texto) / m["habla"]
    juzgable = len(texto.split()) >= MIN_PALABRAS_VEL
    ok = (not juzgable) or (ref * (1 - tol) <= v <= ref * (1 + tol))
    return {"sil_s": round(v, 2), "vel_ok": bool(ok), "vel_juzgable": juzgable}


def pausas(texto: str, m: dict) -> dict:
    """Una pausa larga solo es aceptable si el texto tiene ahí un signo de pausa.
    Se compara el número de pausas largas con el de signos de pausa internos."""
    permitidas = len(PAUSA_TEXTO.findall(texto.strip().rstrip(".?!…")))
    n = len(m["huecos"])
    return {"pausas_largas": n, "pausas_texto": permitidas, "pausas_ok": n <= permitidas}


def es_corta(m: dict) -> bool:
    return bool(m["habla"] < CORTA_S)


def evaluar(texto: str, wav, ref: float = VEL_REF) -> dict:
    """Todas las comprobaciones de este módulo para una toma."""
    m = medir(wav)
    r = {"habla": m["habla"], "corta": es_corta(m)}
    r.update(velocidad(texto, m, ref))
    r.update(pausas(texto, m))
    r["calidad_ok"] = r["vel_ok"] and r["pausas_ok"]
    return r


if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 3:
        print("uso: python calidad_voz.py toma.wav \"texto de la frase\"")
        sys.exit(1)
    print(json.dumps(evaluar(sys.argv[2], Path(sys.argv[1])), ensure_ascii=False, indent=1))
