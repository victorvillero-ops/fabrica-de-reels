"""Revisa un guion de voz (frases.txt, una frase por línea) ANTES de generar la voz con VoiceStudio.

Uso:  python revisar_guion_voz.py frases.txt

Reglas (de investigacion-voz/informe-voicestudio.md; con Clon MK1 en STENDEC, las frases de 1–3
palabras fallaron en el 80 % de las tomas, frente al 15–24 % del resto):
  1. CORTA      — nada de frases sueltas de 1–3 palabras. Únela a la vecina («Un motor. Un motor
                  Rolls-Royce, como…» en una sola línea) o genérala dentro de una frase y recórtala con
                  los tiempos por palabra.
  2. DELETREO   — letras deletreadas separadas por puntos suspensivos: «ese... te... e... ene...».
                  Con comas, la «e» suelta se funde con la sílaba vecina y desaparece.
  3. SUELTA     — una palabra extranjera o inventada (Stendec, nombres en inglés) nunca sola en su
                  línea: siempre dentro de una frase en español. Sin tildes inventadas («Sténdec»
                  empeoró el acento en las pruebas).
  4. LARGA      — más de 30 palabras: divídela; OmniVoice reparte peor el ritmo en frases muy largas.
Sale con código 1 si hay avisos, para que Eco no genere sin revisarlos.
"""
import re, sys
from pathlib import Path

LETRAS = ["a", "be", "ce", "de", "e", "efe", "ge", "hache", "i", "jota", "ka", "ele", "eme", "ene", "o", "pe",
          "cu", "erre", "ese", "te", "u", "uve", "equis", "ye", "zeta"]
L = "|".join(LETRAS)
DELETREO_COMAS = re.compile(rf"\b({L})\s*,\s*({L})\s*,\s*({L})\b", re.I)
PALABRA = re.compile(r"[\wáéíóúüñÁÉÍÓÚÜÑ'-]+")
# Palabras que suenan a extranjeras/inventadas: mayúscula inicial y grupos raros en español.
# (k, w, sh, th, ck, ee, oo, o una consonante final que el español casi nunca usa: c, t, b, p, g, f, m, k)
RARA = re.compile(r"(?:^|\s)([A-Z][a-z]*(?:k|w|sh|th|ck|ee|oo)[a-z]*|[A-Z][a-z]*[cbtpgfmk])\b")


def revisar(lineas):
    avisos = []
    for n, t in enumerate(lineas, 1):
        palabras = PALABRA.findall(t)
        if len(palabras) <= 3:
            avisos.append((n, "CORTA", t, "únela a la frase vecina o genérala dentro de una frase"))
        if DELETREO_COMAS.search(t):
            avisos.append((n, "DELETREO", t, "separa las letras con puntos suspensivos: «ese... te... e...»"))
        if len(palabras) <= 2 and RARA.search(" " + t):
            avisos.append((n, "SUELTA", t, "pon la palabra extranjera o inventada dentro de una frase"))
        if len(palabras) > 30:
            avisos.append((n, "LARGA", t, "divide la frase (más de 30 palabras)"))
    return avisos


def main():
    lineas = [l.strip() for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()]
    avisos = revisar(lineas)
    tipos = {}
    for n, tipo, t, consejo in avisos:
        tipos[tipo] = tipos.get(tipo, 0) + 1
        print(f"frase {n:>3}  {tipo:<8} «{t}» -> {consejo}")
    print(f"\n{len(lineas)} frases, {len(avisos)} avisos " + (str(tipos) if tipos else "(ninguno)"))
    sys.exit(1 if avisos else 0)


if __name__ == "__main__":
    main()
