"""Revisión final de una voz generada línea a línea (después de generar_frases.py, antes de unir_frases.py).

Uso (con el Python de VoiceStudio):
  python revisar_voz.py <carpeta frases> <frases.txt> [salida.json]

Para cada fNNN.wav:
  - velocidad (sílabas/s) frente a la mediana de ESTA voz en ESTE guion (±20 %, frases de 4+ palabras);
  - pausas largas a mitad de frase sin signo de pausa en el texto;
  - acento de las frases cortas (< 1,2 s de habla) medido JUNTO a la frase anterior y la siguiente,
    porque Whisper no distingue el idioma en clips tan cortos.
Imprime las frases a rehacer y la orden ONLY=... REHACER=1 para generar_frases.py, y una lista corta
de frases que conviene ESCUCHAR (las de menor margen). Mide; no escucha.
"""
import json, sys, tempfile, wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import calidad_voz as cv

MODEL = r"D:\Skills y Modelos Locales\VoiceStudio\Modelos (OmniVoice Local)\hf_cache\models--deepdml--faster-whisper-large-v3-turbo-ct2\snapshots\4df90f75321148c3a29a9e2351b7ddf8f5b115a8"
EN_MAX = 0.001


def leer(p):
    with wave.open(str(p)) as w:
        return w.getparams(), w.readframes(w.getnframes())


def concatenar(paths, dst, hueco_s=0.25):
    params, _ = leer(paths[0])
    sil = b"\x00" * int(params.framerate * hueco_s) * params.sampwidth * params.nchannels
    with wave.open(str(dst), "wb") as w:
        w.setparams(params)
        for k, p in enumerate(paths):
            pp, data = leer(p)
            if (pp.framerate, pp.sampwidth, pp.nchannels) != (params.framerate, params.sampwidth, params.nchannels):
                raise ValueError(f"formato distinto en {p}")
            if k:
                w.writeframes(sil)
            w.writeframes(data)


def main():
    carpeta, guion = Path(sys.argv[1]), Path(sys.argv[2])
    salida = Path(sys.argv[3]) if len(sys.argv) > 3 else carpeta / "revision-voz.json"
    lineas = [l.strip() for l in guion.read_text(encoding="utf-8").splitlines() if l.strip()]

    filas = []
    for i, t in enumerate(lineas):
        p = carpeta / f"f{i:03d}.wav"
        if not p.exists():
            filas.append({"n": i + 1, "i": i, "texto": t, "falta": True}); continue
        m = cv.medir(p)
        filas.append({"n": i + 1, "i": i, "texto": t, "habla": m["habla"], "corta": cv.es_corta(m),
                      **cv.velocidad(t, m), **cv.pausas(t, m)})

    juzgables = [f for f in filas if f.get("vel_juzgable") and f.get("sil_s")]
    mediana = float(np.median([f["sil_s"] for f in juzgables])) if juzgables else cv.VEL_REF
    for f in filas:
        if f.get("vel_juzgable") and f.get("sil_s"):
            f["vel_rel"] = round(float(f["sil_s"] / mediana - 1), 3)
            f["vel_ok"] = bool(abs(f["vel_rel"]) <= cv.VEL_TOL)

    from faster_whisper import WhisperModel
    wm = WhisperModel(MODEL, device="cpu", compute_type="int8")
    def en_prob(wav):
        _, info = wm.transcribe(str(wav), beam_size=1, without_timestamps=True)
        return float(dict(info.all_language_probs or []).get("en", 0.0))

    with tempfile.TemporaryDirectory() as td:
        for f in filas:
            if f.get("falta") or not f["corta"]:
                continue
            i = f["i"]
            vecinas = [carpeta / f"f{j:03d}.wav" for j in (i - 1, i, i + 1) if 0 <= j < len(lineas)]
            vecinas = [v for v in vecinas if v.exists()]
            ctx = Path(td) / f"ctx{i:03d}.wav"
            concatenar(vecinas, ctx)
            f["en_contexto"] = round(en_prob(ctx), 5)
            f["acento_ok"] = bool(f["en_contexto"] <= EN_MAX)

    rehacer, motivos = [], {}
    for f in filas:
        why = []
        if f.get("falta"): why.append("falta el audio")
        if f.get("vel_ok") is False: why.append(f"velocidad {f['vel_rel']:+.0%}")
        if f.get("pausas_ok") is False: why.append(f"{f['pausas_largas']} pausa(s) larga(s) sin coma")
        if f.get("acento_ok") is False: why.append(f"acento en contexto {f['en_contexto']}")
        if why:
            rehacer.append(f["i"]); motivos[f["n"]] = why

    # Para escuchar: las de menor margen aunque pasen (velocidad cerca del límite, cortas, deletreos).
    def margen(f):
        m = 1.0
        if f.get("vel_rel") is not None: m = min(m, cv.VEL_TOL - abs(f["vel_rel"]))
        if f.get("corta"): m = min(m, 0.05)
        return m
    escuchar = [f["n"] for f in sorted((f for f in filas if not f.get("falta") and f["i"] not in rehacer), key=margen)[:10]]

    rep = {"mediana_sil_s": round(mediana, 2), "rehacer": motivos,
           "orden": f"ONLY={','.join(map(str, rehacer))} REHACER=1" if rehacer else "",
           "escuchar": escuchar, "frases": filas}
    salida.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Mediana de velocidad: {mediana:.2f} síl/s")
    print(f"A rehacer: {len(motivos)}")
    for n, w in motivos.items():
        print(f"  frase {n}: {'; '.join(w)}")
    if rehacer:
        print(f"Orden: {rep['orden']} python generar_frases.py ...  (índices base 0)")
    print(f"Escuchar (menor margen): {escuchar}")
    print(f"Informe: {salida}")


if __name__ == "__main__":
    main()
