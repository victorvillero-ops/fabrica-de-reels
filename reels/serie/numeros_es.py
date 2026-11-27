"""Spanish number words, for comparing a transcript written in digits with a script written in words."""
U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce",
     "quince", "dieciseis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidos", "veintitres", "veinticuatro",
     "veinticinco", "veintiseis", "veintisiete", "veintiocho", "veintinueve"]
D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
C = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos", 7: "setecientos",
     8: "ochocientos", 9: "novecientos"}


def palabras(n: int) -> str:
    if n < 30: return U[n]
    if n < 100: return D[n // 10] + ("" if n % 10 == 0 else " y " + U[n % 10])
    if n == 100: return "cien"
    if n < 1000: return C[n // 100] + ("" if n % 100 == 0 else " " + palabras(n % 100))
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        return ("mil" if m == 1 else palabras(m) + " mil") + ("" if r == 0 else " " + palabras(r))
    m, r = divmod(n, 1_000_000)
    return ("un millon" if m == 1 else palabras(m) + " millones") + ("" if r == 0 else " " + palabras(r))


def expandir(texto: str) -> str:
    """Replace every number written in digits (3.790 / 2013 / 32,5) with its Spanish words."""
    import re
    def rep(m):
        s = m.group(0)
        if "," in s:
            a, b = s.split(",", 1)
            return palabras(int(a.replace(".", ""))) + " coma " + palabras(int(b))
        return palabras(int(s.replace(".", "")))
    return re.sub(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", rep, texto)
