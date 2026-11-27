"""Reel 04 — GTA 6: 13 years, a hack and two delays. A timeline walked along the Leonida promenade."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "serie"))
from serie import Reel, SLAB_JS

R = Reel(Path(__file__).parent)
w = R.wt
N = {"trece": ["13"], "doscientos": ["200"], "noventa": ["90"], "tres": ["3790", "3.790", "3"], "diecinueve": ["19"], "siete": ["7"]}
K = {
    "mal": w(0, "mal"),
    "l1": R.ls(1), "vendio": w(1, "vendio"), "doscientos": w(1, "doscientos", N["doscientos"]),
    "l2": R.ls(2), "confirmo": w(2, "confirmo"), "febrero": w(2, "febrero"),
    "l3": R.ls(3), "hackeo": w(3, "hackeo"),
    "l4": R.ls(4), "noventa4": w(4, "noventa", N["noventa"]), "videos": w(4, "videos"),
    "l5": R.ls(5), "trailer": w(5, "trailer"), "filtro5": w(5, "filtro"),
    "l6": R.ls(6), "noventa6": w(6, "noventa", N["noventa"]), "dia6": w(6, "dia"),
    "l7": R.ls(7), "retrasos": w(7, "retrasos"), "mayo": w(7, "mayo"),
    "l8": R.ls(8), "noviembre8": w(8, "noviembre"),
    "l9": R.ls(9), "salio": w(9, "salio"),
    "l10": R.ls(10), "tres": w(10, "tres", N["tres"]), "dolares": w(10, "dolares"),
    "l11": R.ls(11), "valio": w(11, "valio"), "end": R.total,
}

body = """
<div class="big" id="bg-13" style="top:820px;font-size:190px;opacity:1"><span class="grad">13 AÑOS</span><br><span class="plate" style="font-size:58px">PARA UN SOLO JUEGO</span></div>
<div class="tag" id="tg-v" style="font-size:84px"><span class="grad">+200 M</span><small>copias de GTA 5</small></div>
<div class="big" id="bg-conf" style="top:960px;font-size:110px"><span class="stamp" style="color:#3BFF8A;border-color:#3BFF8A">CONFIRMADO</span></div>
<div class="tag" id="tg-hack" style="font-size:88px"><span class="grad">90 VIDEOS</span><small>filtrados por un hacker</small></div>
<div class="big" id="bg-hack" style="top:1010px;font-size:118px"><span class="stamp">HACKEADO</span></div>
<div class="tag" id="tg-views" style="font-size:96px"><span class="grad" id="tg-views-n">0</span><small>vistas del tráiler · 24 h</small></div>
<div class="tag" id="tg-retrasos" style="font-size:80px"><span class="grad">2 RETRASOS</span></div>
<div class="tag" id="tg-gold" style="font-size:86px"><span class="grad">3.790 M$</span><small>en un solo día</small></div>
<div class="big" id="bg-sum" style="top:820px;font-size:92px">13 AÑOS<br><span class="grad">1 FILTRACIÓN</span><br>2 RETRASOS</div>
<div class="big" id="bg-cta" style="top:860px;font-size:104px">¿VALIÓ<br><span class="grad">LA PENA?</span></div>
"""

sets_js = SLAB_JS + r"""
const S = { B: -120, C: -60, D: 0, E: 62, F: 128, G: 196 }; const Z = -50;
const brick = canvasTex(64, 64, (g, w, h) => { g.fillStyle = "#fff"; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(0,0,0,0.28)"; g.fillRect(0, h - 5, w, 5); }, true);
function tower(x, color, glow) {
  const m = new THREE.MeshStandardMaterial({ color, roughness: 0.3, metalness: 0.6, map: brick.clone(), emissive: glow || 0x000000, emissiveIntensity: 0.3 });
  m.map.needsUpdate = true; m.map.wrapS = m.map.wrapT = THREE.RepeatWrapping;
  const b = new THREE.Mesh(bGeo, m); b.position.set(x, 0, Z); b.scale.set(7, 0.001, 7); scene.add(b); return b;
}
// B: 2013, GTA 5 — 20 boxes, each one = 10 million copies
const sl2013 = slab(S.B - 9, Z, "2013", "GTA 5", 12, 9);
const vTex = canvasTex(256, 360, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#7FB2FF"); gr.addColorStop(1, "#2A3F8E");
  g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,255,255,0.92)"; g.font = "900 190px Montserrat, sans-serif"; g.textAlign = "center"; g.fillText("5", w / 2, h * 0.62);
  g.fillStyle = "#1B0B3A"; g.fillRect(0, 0, w, 34); });
const vM = [0, 0, 0, 0, 0, 0].map((_, i) => new THREE.MeshStandardMaterial(i === 4 ? { map: vTex, roughness: 0.4 } : { color: 0x1F2D66, roughness: 0.5 }));
const vBoxes = []; for (let i = 0; i < 20; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(3.2, 4.4, 0.5), vM);
  const col = i % 4, row = Math.floor(i / 4); b.userData = { x: S.B + 3 + col * 3.6, y: 2.4 + row * 4.8, d: i * 0.04 }; scene.add(b); vBoxes.push(b); }
// C: February 2022, confirmed
const sl2022 = slab(S.C, Z, "2022", "FEBRERO", 14, 10);
// D: the hack — a screen whose 90 video tiles light up red one by one
const hackCv = document.createElement("canvas"); hackCv.width = 640; hackCv.height = 400; const hackG = hackCv.getContext("2d");
const hackT = new THREE.CanvasTexture(hackCv); hackT.encoding = THREE.sRGBEncoding; let hackN = -1;
function drawHack(n) { if (n === hackN) return; hackN = n; const g = hackG; g.fillStyle = "#12051F"; g.fillRect(0, 0, 640, 400);
  for (let k = 0; k < 90; k++) { const c = k % 10, r = Math.floor(k / 10), x = 24 + c * 60, y = 22 + r * 40;
    g.fillStyle = k < n ? "#FF3B5C" : "#2E1450"; g.fillRect(x, y, 52, 32);
    if (k < n) { g.fillStyle = "#fff"; g.beginPath(); g.moveTo(x + 21, y + 9); g.lineTo(x + 21, y + 23); g.lineTo(x + 33, y + 16); g.fill(); } }
  hackT.needsUpdate = true; }
drawHack(0);
const frameM = new THREE.MeshStandardMaterial({ color: 0x1B0B3A, roughness: 0.5 });
function screenOn(x, tex) { const g = new THREE.Group(); g.position.set(x, 0, Z); scene.add(g);
  const s = new THREE.Mesh(new THREE.BoxGeometry(30, 18.75, 0.8), [frameM, frameM, frameM, frameM, new THREE.MeshBasicMaterial({ map: tex }), frameM]); s.position.y = 15.5; g.add(s);
  [-9, 9].forEach((px) => { const post = new THREE.Mesh(new THREE.BoxGeometry(1, 7, 1), frameM); post.position.set(px, 3.5, -0.2); g.add(post); }); return g; }
const scrD = screenOn(S.D, hackT);
// E: the leaked first trailer
const trTex = canvasTex(640, 400, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#2A0E4E"); gr.addColorStop(1, "#7A1D5E");
  g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,255,255,0.95)"; g.beginPath(); g.moveTo(w / 2 - 50, h / 2 - 62); g.lineTo(w / 2 - 50, h / 2 + 62); g.lineTo(w / 2 + 64, h / 2); g.fill();
  g.fillStyle = "#FF3D8B"; g.fillRect(0, h - 14, w * 0.62, 14); g.fillStyle = "rgba(255,255,255,0.25)"; g.fillRect(w * 0.62, h - 14, w * 0.38, 14); });
const scrE = screenOn(S.E, trTex);
// F: three release dates, two struck through
const d1 = slab(S.F - 12, Z, "2025", "OTOÑO", 10, 7.5), d2 = slab(S.F, Z, "2026", "MAYO", 10, 7.5), d3 = slab(S.F + 12, Z, "2026", "NOVIEMBRE", 10, 7.5, 0x5A1050);
const redM = new THREE.MeshStandardMaterial({ color: 0xFF3B3B, emissive: 0xFF2020, emissiveIntensity: 0.6, roughness: 0.4 });
function strike(x) { const b = new THREE.Mesh(new THREE.BoxGeometry(13, 1.1, 0.5), redM); b.position.set(x, 3.75, Z + 1.2); b.rotation.z = -0.55; b.scale.x = 0.001; scene.add(b); return b; }
const st1 = strike(S.F - 12), st2 = strike(S.F);
// G: launch day and the money
const launch = slab(S.G - 8, Z, "19 NOV", "2026 · ¡POR FIN!", 12, 8, 0x5A1050);
const tGold = tower(S.G + 6, 0xFFC94A, 0x6a4200);
"""

keys_js = r"""
const st = (x, h, dist, lookH) => [[x, h, Z + dist], [x, lookH, Z]];
const keys = [
  [0, [-210, 85, 230], [-140, 42, -420]],
  [K.l1 - 0.2, [-150, 30, 130], [-125, 20, -150]],
  [K.l1 + 0.7, ...st(S.B, 6, 80, 21)], [K.l2 - 0.2, ...st(S.B, 6, 84, 21)],
  [K.l2 + 0.6, ...st(S.C, 7, 64, 8)], [K.l3 - 0.2, ...st(S.C, 7, 66, 8)],
  [K.l3 + 0.6, ...st(S.D, 8, 80, 23)], [K.l5 - 0.2, ...st(S.D, 8, 84, 23)],
  [K.l5 + 0.6, ...st(S.E, 8, 80, 24)], [K.l7 - 0.2, ...st(S.E, 8, 84, 24)],
  [K.l7 + 0.6, ...st(S.F, 5, 82, 11)], [K.l9 - 0.2, ...st(S.F, 5, 78, 11)],
  [K.l9 + 0.6, ...st(S.G, 5, 78, 20)], [K.l11 - 0.1, ...st(S.G, 5, 84, 22)],
  [K.l11 + 1.1, [30, 95, 260], [30, 60, -420]],
  [DUR, [10, 80, 230], [20, 52, -420]],
];
"""

render_js = r"""
  riseIn(sl2013, t, K.l1 - 0.3, 0.5);
  vBoxes.forEach((b) => { const u = eo((t - K.vendio - b.userData.d) / 0.45); b.position.set(b.userData.x, b.userData.y + (1 - u) * 40, Z); b.rotation.set((1 - u) * 1.2, (1 - u) * 2, 0); b.visible = u > 0; });
  pin("tg-v", S.B + 8.4, 27, Z, win(t, K.doscientos, K.l2 + 0.3));
  riseIn(sl2022, t, K.l2 + 0.2, 0.5);
  const sb = eo((t - K.l3 + 0.3) / 0.5); scrD.scale.set(Math.max(0.001, sb), Math.max(0.001, sb), 1); scrD.visible = sb > 0;
  drawHack(Math.round(90 * clamp01((t - K.l4) / (K.videos + 0.8 - K.l4))));
  pin("tg-hack", S.D, 31, Z, win(t, K.videos, K.l5 + 0.3));
  const se = eo((t - K.l5 + 0.3) / 0.5); scrE.scale.set(Math.max(0.001, se), Math.max(0.001, se), 1); scrE.visible = se > 0;
  pin("tg-views", S.E, 31, Z, win(t, K.noventa6 - 0.3, K.l7 + 0.3));
  riseIn(d1, t, K.l7 + 0.1, 0.4); riseIn(d2, t, K.mayo - 0.3, 0.4); riseIn(d3, t, K.noviembre8 - 0.3, 0.4);
  st1.scale.x = Math.max(0.001, eo((t - K.mayo) / 0.3)); st2.scale.x = Math.max(0.001, eo((t - K.noviembre8) / 0.3));
  pin("tg-retrasos", S.F, 12.5, Z, win(t, K.noviembre8 + 0.3, K.l9 + 0.2));
  riseIn(launch, t, K.l9 + 0.1, 0.5);
  const hg = grow(tGold, 37.9, t, K.tres - 0.1, 1.1);
  pin("tg-gold", S.G + 6, hg + 2, Z, win(t, K.tres + 0.6, K.l11 + 0.3));
"""

overlay_js = r"""
tl.to("#bg-13", { opacity: 0, duration: 0.2 }, K.l1 - 0.25);
tl.fromTo("#bg-conf", { opacity: 0, scale: 1.8, rotation: -8 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.18, ease: "power4.out" }, K.confirmo);
tl.to("#bg-conf", { opacity: 0, duration: 0.2 }, K.l3 + 0.05);
tl.fromTo("#bg-hack", { opacity: 0, scale: 1.8, rotation: 6 }, { opacity: 1, scale: 1, rotation: 6, duration: 0.16, ease: "power4.out" }, K.hackeo);
tl.to("#bg-hack", { opacity: 0, duration: 0.15 }, K.l4 + 0.4);
const vn = document.getElementById("tg-views-n"), vv = { v: 0 };
tl.fromTo(vv, { v: 0 }, { v: 90000000, duration: 0.9, ease: "power2.out", onUpdate: () => (vn.textContent = Math.round(vv.v).toLocaleString("es-ES").replace(/ /g, ".")) }, K.noventa6 - 0.3);
tl.fromTo("#bg-sum", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, K.l11);
tl.to("#bg-sum", { opacity: 0, duration: 0.2 }, K.valio - 0.2);
tl.fromTo("#bg-cta", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, K.valio);
"""

# sounds
k = K
R.sfx(0.05, "barrido-largo.wav", 0.45)
R.sfx(k["mal"], "golpe.wav", 0.35)
R.sfx(k["l1"] - 0.3, "barrido-1.wav", 0.4)
for j in range(0, 20, 3): R.sfx(k["vendio"] + j * 0.04 + 0.35, f"caja-{j % 2 + 1}.wav", 0.25)
R.sfx(k["l2"] + 0.2, "barrido-2.wav", 0.4)
R.sfx(k["confirmo"], "sello.wav", 0.6)
R.sfx(k["l3"] - 0.3, "barrido-1.wav", 0.4)
R.sfx(k["hackeo"], "glitch.wav", 0.55)
for j in range(8): R.sfx(k["l4"] + j * (k["videos"] + 0.8 - k["l4"]) / 8, "tic.wav", 0.18)
R.sfx(k["l5"] - 0.3, "barrido-2.wav", 0.4)
R.sfx(k["noventa6"] - 0.3, "subida-2.wav", 0.3)
R.sfx(k["l7"] + 0.1, "barrido-1.wav", 0.4)
R.sfx(k["mayo"], "golpe.wav", 0.45)
R.sfx(k["noviembre8"], "golpe.wav", 0.5)
R.sfx(k["l9"], "subida-1.wav", 0.35)
R.sfx(k["salio"] + 0.1, "impacto.wav", 0.5)
R.sfx(k["tres"], "monedas.wav", 0.45)
R.sfx(k["l11"], "barrido-largo.wav", 0.35)
R.sfx(k["valio"], "pop-2.wav", 0.5)

CAPS = [
    "GTA 6 tardó 13 años en llegar. Y casi todo salió mal antes de salir bien.",
    "GTA 5 salió en 2013, y vendió más de 200 millones de copias.",
    "Pero Rockstar no confirmó el 6 hasta febrero de 2022.",
    "Siete meses después, un adolescente hackeó la empresa,",
    "y filtró 90 videos del juego sin terminar.",
    "En 2023, el primer tráiler también se filtró.",
    "Y aun así, hizo 90 millones de vistas en un solo día.",
    "Luego llegaron los retrasos: de 2025 a mayo de 2026,",
    "y de mayo, a noviembre.",
    "El 19 de noviembre, por fin salió.",
    "Y en un solo día facturó 3.790 millones de dólares.",
    None,
]
HL = {"13", "mal", "200", "2022", "hackeó", "90", "filtró", "retrasos", "noviembre", "noviembre,", "salió", "3.790", "2013,", "2023,"}

R.write(R.mundo(body, sets_js, keys_js, render_js, overlay_js, K), R.subs(CAPS, HL))
