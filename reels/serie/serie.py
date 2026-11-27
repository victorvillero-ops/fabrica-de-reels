"""Shared builder for the GTA 6 series (reel-03 look): Leonida-at-sunset three.js world, pinned labels,
uppercase gold captions, sound lanes. Each reel's construir.py supplies its keys, labels, sets, camera and sounds.
"""
import json, re, subprocess, unicodedata
from pathlib import Path

HERE = Path(__file__).parent
WORLD_JS = (HERE / "mundo_base.js").read_text(encoding="utf-8")
HELP_JS = (HERE / "ayudas.js").read_text(encoding="utf-8")
PINK, GOLD = "#FF3D8B", "#FFC94A"
OUTLINE = ("0 0 0 #2A0B4A, 4px 4px 0 #2A0B4A, -4px 4px 0 #2A0B4A, 4px -4px 0 #2A0B4A, -4px -4px 0 #2A0B4A, "
           "0 5px 0 #2A0B4A, 5px 0 0 #2A0B4A, -5px 0 0 #2A0B4A, 0 -5px 0 #2A0B4A, 0 14px 26px rgba(0,0,0,0.55)")

CSS = f"""
  #root {{ position:absolute; inset:0; overflow:hidden; background:#1B0B3A; }}
  #mu-gl {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
  .tag {{ position:absolute; left:0; top:0; transform: translate(-50%, -100%); white-space:nowrap; text-align:center; opacity:0;
         font-family:'Montserrat', sans-serif; font-weight:900; color:#fff; text-shadow: {OUTLINE}; }}
  .tag small {{ display:table; margin:8px auto 0; font-family:'Inter', sans-serif; font-weight:800; font-size:28px; letter-spacing:0.05em; text-transform:uppercase;
               background:#2A0B4A; color:#fff; padding:6px 14px; border-radius:10px; text-shadow:none; }}
  .big {{ position:absolute; left:0; width:1080px; text-align:center; font-family:'Montserrat', sans-serif; font-weight:900; opacity:0;
         letter-spacing:-0.02em; line-height:0.95; color:#fff; text-shadow: {OUTLINE}; }}
  .grad {{ color:{GOLD}; text-shadow: {OUTLINE}; }}
  .plate {{ display:inline-block; background:{PINK}; color:#fff; padding:10px 26px 6px; border-radius:14px; text-shadow:none; }}
  .stamp {{ display:inline-block; color:#FF3B3B; border:10px solid #FF3B3B; padding:8px 28px 0; border-radius:16px; text-shadow:none;
           background:rgba(30,6,40,0.35); }}
  .vig {{ position:absolute; inset:0; background: linear-gradient(180deg, rgba(10,0,30,0) 62%, rgba(18,4,40,0.72) 100%), radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 60%, rgba(10,0,30,0.5) 100%); }}
"""


class Reel:
    def __init__(self, fuente: Path):
        self.fuente, self.out = fuente, fuente.parent
        self.T = json.loads((fuente / "tiempos.json").read_text(encoding="utf-8"))
        W = json.loads((fuente / "palabras.json").read_text(encoding="utf-8"))
        self.lines, self.total = self.T["lines"], self.T["total"]
        self.words = [w for s in W["segments"] for w in s["words"]]
        self.sfx_list = []

    def ls(self, i): return self.lines[i]["start"]
    def le(self, i): return self.lines[i]["end"]

    @staticmethod
    def norm(s):
        s = unicodedata.normalize("NFD", s.lower())
        return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))

    def wt(self, i, token, alias=(), nth=0):
        keys = [self.norm(token)] + [self.norm(a) for a in alias]
        cands = [w for w in self.words if self.ls(i) - 0.6 <= w["s"] <= self.le(i) + 0.3]
        hits = [w for w in cands if any(self.norm(w["w"]).startswith(k) for k in keys)]
        if len(hits) <= nth:
            raise SystemExit(f"word '{token}' not in line {i}: {[w['w'] for w in cands]}")
        return round(hits[nth]["s"], 3)

    def sfx(self, t, name, vol=0.5):
        self.sfx_list.append((round(t, 3), name, vol))

    # ------------------------------------------------------------------ files
    def mundo(self, body, sets_js, keys_js, render_js, overlay_js, K):
        js = ("const K = " + json.dumps(K) + ";\nconst DUR = K.end;\n" + WORLD_JS + "\n" + sets_js + "\n" + keys_js + "\n" + HELP_JS +
              "\nfunction render(t) {\n  const [p, l] = camAt(t); cam.position.set(p[0], p[1], p[2]); cam.lookAt(l[0], l[1], l[2]); cam.updateMatrixWorld(true);\n"
              + render_js + "\n  sun.position.y = 150 - 40 * (t / DUR);\n  renderer.render(scene, cam);\n}\n"
              "const clock = { t: 0 };\ntl.to(clock, { t: DUR, duration: DUR, ease: \"none\", onUpdate: () => render(clock.t) }, 0);\nrender(0);\n" + overlay_js)
        return f"""<template>
<style>{CSS}</style>
<div id="root" data-composition-id="mundo" data-width="1080" data-height="1920" data-duration="{self.total}">
<canvas id="mu-gl" width="1080" height="1920"></canvas>
<div class="vig"></div>
{body}
</div>
<script>
(function () {{
  document.fonts.load('900 190px "Montserrat"').then(function () {{
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["mundo"] = tl;
  }});
}})();
</script>
</template>
"""

    def _token_times(self, toks, lw):
        """(start, end) for each caption token: matched to a heard word by text (in order), otherwise
        interpolated between its matched neighbours (covers digits vs words, "GTA 6" vs "GTA seis")."""
        n, m = len(toks), len(lw)
        hit, p = [None] * n, 0
        for j, tk in enumerate(toks):
            k = self.norm(tk)
            if not k: continue
            for q in range(p, min(m, p + 4)):
                h = self.norm(lw[q]["w"])
                if h and (h.startswith(k[:5]) or k.startswith(h[:5])):
                    hit[j] = q; p = q + 1; break
        out = []
        for j in range(n):
            if hit[j] is not None:
                w = lw[hit[j]]; out.append((w["s"], w["e"])); continue
            pj = next((x for x in range(j - 1, -1, -1) if hit[x] is not None), None)
            nj = next((x for x in range(j + 1, n) if hit[x] is not None), None)
            t0 = lw[hit[pj]]["e"] if pj is not None else lw[0]["s"]
            t1 = lw[hit[nj]]["s"] if nj is not None else lw[-1]["e"]
            lo, hi = (pj if pj is not None else -1), (nj if nj is not None else n)
            f = (j - lo) / (hi - lo)
            t = t0 + (t1 - t0) * f
            out.append((t, t + 0.25))
        return out

    def subs(self, caps, hl, skip_last=True, sync="letters"):
        """sync="letters" (reels 03–06, unchanged) spreads chunks over the line by letter count;
        sync="words" starts each chunk at its first word's time in palabras.json."""
        groups = []
        for i, text in enumerate(caps):
            if text is None: continue
            toks = text.split(); chunks, cur = [], []
            for tkn in toks:
                cur.append(tkn)
                if len(cur) >= 3 or (tkn[-1] in ",.?:" and len(cur) >= 2):
                    chunks.append(cur); cur = []
            if cur:
                if chunks and len(cur) == 1: chunks[-1] += cur
                else: chunks.append(cur)
            a, b = self.ls(i), self.le(i)
            if sync == "words":
                # words heard in THIS line only: the window stops where the neighbouring lines start/end
                lo = max(a - 0.3, self.le(i - 1) + 0.01) if i > 0 else a - 0.3
                hi = min(b + 0.2, self.ls(i + 1) - 0.01) if i + 1 < len(self.lines) else b + 0.2
                lw = [w for w in self.words if lo <= w["s"] <= hi]
                if lw:
                    tt = self._token_times(toks, lw)
                    j0 = 0
                    for ch in chunks:
                        j1 = j0 + len(ch)
                        ts = [max(a, x[0]) for x in tt[j0:j1]]; ts[0] = a if j0 == 0 else ts[0]
                        e = max(ts[-1] + 0.2, min(b, tt[j1 - 1][1]))
                        groups.append((round(ts[0], 3), round(e, 3), ch, [round(x, 3) for x in ts])); j0 = j1
                    continue
            tot = sum(len(t) + 1 for t in toks); pos = 0
            for ch in chunks:
                n = sum(len(t) + 1 for t in ch)
                groups.append((round(a + (b - a) * pos / tot, 3), round(a + (b - a) * (pos + n) / tot, 3), ch)); pos += n
        starts = [round(max(0.05, g[0] - 0.06), 3) for g in groups]
        html, js = [], []
        for k, g in enumerate(groups):
            s, e, ch = g[:3]; tts = g[3] if len(g) > 3 else None
            nxt = starts[k + 1] if k + 1 < len(groups) else self.total
            end = min(nxt, max(e + 0.35, s + 0.5))
            if k == len(groups) - 1: end = min(self.total, e + 0.35)
            start = 0.0 if k == 0 else starts[k]
            words = []
            for j, w in enumerate(ch):
                cls = "w hl" if w.lower().strip(",.:") in hl or w.lower() in hl else "w"
                words.append(f'<span class="{cls}" id="su-{k}-{j}">{w}</span>')
                if k > 0:
                    js.append(f'tl.fromTo("#su-{k}-{j}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "back.out(2.2)" }}, {tts[j] if tts else round(s + (e - s) * j / len(ch), 3)});')
            html.append(f'<div class="grp clip" id="su-{k}" data-start="{start}" data-duration="{round(end - start, 3)}" data-track-index="0"><p>{" ".join(words)}</p></div>')
        return f"""<template>
<style>
  #root {{ position:absolute; inset:0; pointer-events:none; }}
  .grp {{ position:absolute; left:0; top:300px; width:1080px; height:190px; display:flex; align-items:center; justify-content:center; overflow:visible; }}
  .grp p {{ margin:0; width:880px; text-align:center; font-family:'Montserrat', sans-serif; font-weight:900; font-size:76px; line-height:1.08;
           color:#FFFFFF; text-transform:uppercase; letter-spacing:-0.01em; text-shadow: 0 5px 0 rgba(40,10,70,0.75), 0 10px 26px rgba(0,0,0,0.5); }}
  .w {{ display:inline-block; margin:0 6px; }}
  .hl {{ color:{GOLD}; }}
</style>
<div id="root" data-composition-id="subtitulos" data-width="1080" data-height="1920" data-duration="{self.total}">
{''.join(html)}
</div>
<script>
(function () {{
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["subtitulos"] = tl;
}})();
</script>
</template>
"""

    def index(self, music_vol=0.12):
        def dur(p):
            return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                              capture_output=True, text=True).stdout), 3)
        D = {p.name: dur(p) for p in (self.out / "assets" / "audio").glob("*.wav")}
        lanes, audio = [], []
        for n, (t, name, vol) in enumerate(sorted(self.sfx_list)):
            d = D[name]; t = max(0, t)
            lane = next((i for i, busy in enumerate(lanes) if busy <= t), None)
            if lane is None: lanes.append(0); lane = len(lanes) - 1
            lanes[lane] = t + d
            audio.append(f'      <audio id="fx{n}" class="clip" src="assets/audio/{name}" data-start="{t}" data-duration="{d}" data-track-index="{6 + lane}" data-volume="{vol}"></audio>')
        T = self.total
        return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#1B0B3A; }} #root {{ position:relative; width:1080px; height:1920px; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
      <div id="mundo" data-composition-id="mundo" data-composition-src="compositions/mundo.html" data-start="0" data-duration="{T}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="subtitulos" data-composition-id="subtitulos" data-composition-src="compositions/subtitulos.html" data-start="0" data-duration="{T}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:40"></div>
      <audio id="voz" class="clip" src="assets/audio/voz.wav" data-start="0" data-duration="{D['voz.wav']}" data-track-index="3" data-volume="1"></audio>
      <audio id="musica" class="clip" src="assets/audio/musica.wav" data-start="0" data-duration="{T}" data-track-index="4" data-volume="{music_vol}" data-fade-out="2"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""

    def write(self, mundo_html, subs_html, music_vol=0.12):
        comp = self.out / "compositions"; comp.mkdir(exist_ok=True)
        (comp / "mundo.html").write_text(mundo_html, encoding="utf-8")
        (comp / "subtitulos.html").write_text(subs_html, encoding="utf-8")
        (self.out / "index.html").write_text(self.index(music_vol), encoding="utf-8")
        print(f"total {self.total}s; sfx {len(self.sfx_list)}")


SLAB_JS = r"""
// an engraved-looking slab with gold text on its face (years, dates, words)
function slabTex(text, sub, w, h) { return canvasTex(512, Math.round(512 * h / w), (g, W, H) => {
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#3A1A66"); gr.addColorStop(1, "#1B0B3A"); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  g.strokeStyle = "#FFC94A"; g.lineWidth = 10; g.strokeRect(14, 14, W - 28, H - 28);
  g.fillStyle = "#FFC94A"; g.textAlign = "center"; g.textBaseline = "middle"; g.font = `900 ${Math.round(H * (sub ? 0.36 : 0.46))}px Montserrat, sans-serif`;
  g.fillText(text, W / 2, sub ? H * 0.42 : H / 2);
  if (sub) { g.fillStyle = "#FFFFFF"; g.font = `800 ${Math.round(H * 0.13)}px Montserrat, sans-serif`; g.fillText(sub, W / 2, H * 0.76); } }); }
function slab(x, z, text, sub, w, h, color) {
  const face = new THREE.MeshStandardMaterial({ map: slabTex(text, sub, w, h), roughness: 0.4, emissive: 0xffffff, emissiveMap: slabTex(text, sub, w, h), emissiveIntensity: 0.35 });
  const side = new THREE.MeshStandardMaterial({ color: color || 0x2A0B4A, roughness: 0.5 });
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, 1.6), [side, side, side, side, face, side]);
  const g = new THREE.Group(); m.position.y = h / 2; g.add(m); g.position.set(x, 0, z); scene.add(g); return g;
}
function riseIn(g, t, t0, dur) { const u = eo((t - t0) / (dur || 0.5)); g.scale.set(1, Math.max(0.001, u), 1); g.visible = u > 0; }
"""
