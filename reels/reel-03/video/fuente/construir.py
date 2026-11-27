"""Build reel 03 (GTA 6 records) from the voice timings.

One continuous three.js world, "Leonida at sunset": ocean, palms, a lit skyline, and along the beach
promenade one data set per beat (towers of money, a wall of game boxes, a map, gold bars). The camera
travels from set to set; HTML labels are pinned to 3D points by projecting them every frame.
Writes ../index.html, ../compositions/mundo.html, ../compositions/subtitulos.html.
"""
import json, re, subprocess, unicodedata
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent
T = json.loads((HERE / "tiempos.json").read_text(encoding="utf-8"))
W = json.loads((HERE / "palabras.json").read_text(encoding="utf-8"))
LINES, TOTAL = T["lines"], T["total"]
WORDS = [w for seg in W["segments"] for w in seg["words"]]
SFX = []
PINK, ORANGE, TEAL, GOLD = "#FF3D8B", "#FF9A3C", "#2EE6D6", "#FFC94A"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def ls(i): return LINES[i]["start"]
def le(i): return LINES[i]["end"]


def wt(i, token, nth=0):
    alias = {"tres": ["3790", "3.790", "3"], "veinticuatro": ["24"], "treinta": ["32", "325"], "ochocientos": ["800"],
             "cinco": ["5"], "mil": ["1500", "1.500"], "seis": ["6"], "noventa": ["90"]}
    keys = [norm(token)] + [norm(a) for a in alias.get(norm(token), [])]
    cands = [w for w in WORDS if ls(i) - 0.6 <= w["s"] <= le(i) + 0.3]
    hits = [w for w in cands if any(norm(w["w"]).startswith(k) for k in keys)]
    if len(hits) <= nth:
        raise SystemExit(f"word '{token}' not in line {i}: {[w['w'] for w in cands]}")
    return round(hits[nth]["s"], 3)


def sfx(t, name, vol=0.5):
    SFX.append((round(t, 3), name, vol))


# ------------------------------------------------------------------ the world and its timeline
def build_mundo():
    # key moments (absolute seconds = local, the scene starts at 0)
    k = {
        "avatar": wt(0, "avatar"), "dia": wt(0, "dia"), "cines": wt(0, "cines"),
        "l1": ls(1), "millones1": wt(1, "millones"), "horas": wt(1, "horas"),
        "l2": ls(2), "loco": wt(2, "loco"),
        "l3": ls(3), "vendido": wt(3, "vendido"), "copias": wt(3, "copias"),
        "l4": ls(4), "ochocientos": wt(4, "ochocientos"),
        "l5": ls(5), "cinco": wt(5, "cinco"),
        "l6": ls(6), "trailer": wt(6, "trailer"), "noventa": wt(6, "noventa"), "dia6": wt(6, "dia"),
        "l7": ls(7), "leonida": wt(7, "leonida"), "grande7": wt(7, "grande"),
        "l8": ls(8), "vice": wt(8, "vice"), "doble": wt(8, "doble"), "santos": wt(8, "santos"),
        "l9": ls(9), "mil9": wt(9, "mil"), "dolares9": wt(9, "dolares"),
        "l10": ls(10), "pelicula": wt(10, "pelicula"),
        "l11": ls(11), "lanzamiento": wt(11, "lanzamiento"), "historia11": wt(11, "historia"),
        "l12": ls(12), "end": TOTAL,
    }
    K = json.dumps(k)
    css = f"""
  #root {{ position:absolute; inset:0; overflow:hidden; background:#1B0B3A; }}
  #mu-gl {{ position:absolute; left:0; top:0; width:1080px; height:1920px; }}
  .tag {{ position:absolute; left:0; top:0; transform: translate(-50%, -100%); white-space:nowrap; text-align:center; opacity:0;
         font-family:'Montserrat', sans-serif; font-weight:900; color:#fff; text-shadow: 0 0 0 #2A0B4A, 4px 4px 0 #2A0B4A, -4px 4px 0 #2A0B4A, 4px -4px 0 #2A0B4A, -4px -4px 0 #2A0B4A, 0 5px 0 #2A0B4A, 5px 0 0 #2A0B4A, -5px 0 0 #2A0B4A, 0 -5px 0 #2A0B4A, 0 14px 26px rgba(0,0,0,0.55); }}
  .tag small {{ display:table; margin:8px auto 0; font-family:'Inter', sans-serif; font-weight:800; font-size:28px; letter-spacing:0.05em; text-transform:uppercase;
               background:#2A0B4A; color:#fff; padding:6px 14px; border-radius:10px; text-shadow:none; }}
  .big {{ position:absolute; left:0; width:1080px; text-align:center; font-family:'Montserrat', sans-serif; font-weight:900; opacity:0;
         letter-spacing:-0.02em; line-height:0.95; }}
  .grad {{ color:{GOLD}; text-shadow: 0 0 0 #2A0B4A, 4px 4px 0 #2A0B4A, -4px 4px 0 #2A0B4A, 4px -4px 0 #2A0B4A, -4px -4px 0 #2A0B4A, 0 5px 0 #2A0B4A, 5px 0 0 #2A0B4A, -5px 0 0 #2A0B4A, 0 -5px 0 #2A0B4A, 0 14px 26px rgba(0,0,0,0.55); }}
  .plate {{ display:inline-block; background:{PINK}; color:#fff; padding:10px 26px 6px; border-radius:14px; }}
  .vig {{ position:absolute; inset:0; background: linear-gradient(180deg, rgba(10,0,30,0) 62%, rgba(18,4,40,0.72) 100%), radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 60%, rgba(10,0,30,0.5) 100%); }}
"""
    body = f"""
<canvas id="mu-gl" width="1080" height="1920"></canvas>
<div class="vig"></div>
<div class="tag" id="tg-avatar" style="font-size:64px">2.920 M$<small>Avatar · toda su historia</small></div>
<div class="tag" id="tg-gta1" style="font-size:78px"><span class="grad">3.790 M$</span><small>GTA 6 · un solo día</small></div>
<div class="big" id="bg-count" style="top:1060px;font-size:104px"><span class="grad" id="bg-count-n">0</span></div>
<div class="big" id="bg-24" style="top:1190px;font-size:54px"><span class="plate">EN 24 HORAS</span></div>
<div class="big" id="bg-pero" style="top:880px;font-size:150px"><span class="grad">PERO…</span></div>
<div class="tag" id="tg-copias" style="font-size:96px"><span class="grad">32,5 M</span><small>copias · antes de salir</small></div>
<div class="tag" id="tg-gta5" style="font-size:60px">800 M$<small>GTA 5 · día 1</small></div>
<div class="tag" id="tg-gta6" style="font-size:70px"><span class="grad">3.790 M$</span><small>GTA 6 · día 1</small></div>
<div class="big" id="bg-x5" style="left:30px;width:540px;top:840px;font-size:170px"><span class="grad">×4,7</span></div>
<div class="tag" id="tg-leonida" style="font-size:72px"><span class="grad">LEONIDA</span><small>el mapa más grande de Rockstar</small></div>
<div class="tag" id="tg-ls" style="font-size:44px">Los Santos<small>GTA 5</small></div>
<div class="tag" id="tg-vc" style="font-size:56px"><span class="grad">Vice City</span><small>×2</small></div>
<div class="tag" id="tg-views" style="font-size:96px"><span class="grad" id="tg-views-n">0</span><small>vistas del tráiler · 24 h</small></div>
<div class="tag" id="tg-peli" style="font-size:40px">La película<br>más cara</div>
<div class="tag" id="tg-oro" style="font-size:90px"><span class="grad">≈ 1.500 M$</span><small>presupuesto estimado</small></div>
<div class="big" id="bg-final" style="top:900px;font-size:92px"><span class="grad">EL LANZAMIENTO<br>MÁS GRANDE<br>DE LA HISTORIA</span></div>
<div class="big" id="bg-cta" style="top:880px;font-size:100px;color:#fff;text-shadow:0 0 0 #2A0B4A, 4px 4px 0 #2A0B4A, -4px 4px 0 #2A0B4A, 4px -4px 0 #2A0B4A, -4px -4px 0 #2A0B4A, 0 5px 0 #2A0B4A, 5px 0 0 #2A0B4A, -5px 0 0 #2A0B4A, 0 -5px 0 #2A0B4A, 0 14px 26px rgba(0,0,0,0.55)">¿JUGANDO<br><span class="grad">O ESPERANDO?</span></div>
"""
    js = r"""
const K = __K__;
const DUR = K.end;
// ---------------- renderer, camera
const canvas = document.getElementById("mu-gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false);
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x8a3a7a, 420, 1500);
const cam = new THREE.PerspectiveCamera(45, 1080 / 1920, 0.5, 4000);
function seeded(s) { let a = s >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const R = seeded(2026);
function canvasTex(w, h, draw, rep) { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; } return t; }

// ---------------- sky + sun
const skyTex = canvasTex(16, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
  gr.addColorStop(0, "#160634"); gr.addColorStop(0.38, "#5B1A6E"); gr.addColorStop(0.62, "#E8457E"); gr.addColorStop(0.8, "#FF8C55"); gr.addColorStop(1, "#FFC36B");
  g.fillStyle = gr; g.fillRect(0, 0, w, h); });
const sky = new THREE.Mesh(new THREE.SphereGeometry(2500, 32, 16), new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false }));
scene.add(sky);
const sunTex = canvasTex(512, 512, (g, w) => { const gr = g.createLinearGradient(0, 0, 0, w); gr.addColorStop(0, "#FFF2A8"); gr.addColorStop(1, "#FF5E8A");
  g.fillStyle = gr; g.beginPath(); g.arc(w / 2, w / 2, w / 2 - 4, 0, Math.PI * 2); g.fill();
  g.globalCompositeOperation = "destination-out"; for (let i = 0; i < 7; i++) { const y = w * 0.58 + i * 30; g.fillRect(0, y, w, 6 + i * 2.4); } });
const sun = new THREE.Mesh(new THREE.PlaneGeometry(520, 520), new THREE.MeshBasicMaterial({ map: sunTex, transparent: true, fog: false }));
sun.position.set(-40, 150, -1500); scene.add(sun);

// ---------------- ocean + beach + promenade
const sea = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000), new THREE.MeshStandardMaterial({ color: 0x1A0B35, roughness: 0.55, metalness: 0.35 }));
sea.rotation.x = -Math.PI / 2; sea.position.y = -0.6; scene.add(sea);
const glint = new THREE.Mesh(new THREE.PlaneGeometry(160, 1400), new THREE.MeshBasicMaterial({ map: canvasTex(64, 512, (g, w, h) => {
  for (let y = 0; y < h; y += 6) { g.fillStyle = `rgba(255,${180 + (y % 60)},120,${0.5 * (y / h)})`; g.fillRect(w * (0.5 - 0.4 * y / h) + (y * 37 % 11), y, w * 0.8 * y / h, 2); } }),
  transparent: true, depthWrite: false, fog: false }));
glint.rotation.x = -Math.PI / 2; glint.position.set(-40, -0.5, -820); scene.add(glint);
const sand = new THREE.Mesh(new THREE.PlaneGeometry(900, 140), new THREE.MeshStandardMaterial({ color: 0x6E3A52, roughness: 0.95 }));
sand.rotation.x = -Math.PI / 2; sand.position.set(30, 0, -30); scene.add(sand);
const walk = new THREE.Mesh(new THREE.PlaneGeometry(900, 26), new THREE.MeshStandardMaterial({ color: 0x7A3E66, roughness: 0.7 }));
walk.rotation.x = -Math.PI / 2; walk.position.set(30, 0.05, -52); scene.add(walk);
const land = new THREE.Mesh(new THREE.PlaneGeometry(1400, 900), new THREE.MeshStandardMaterial({ color: 0x3C2A55, roughness: 0.9 }));
land.rotation.x = -Math.PI / 2; land.position.set(30, 0.02, -550); scene.add(land);

// ---------------- skyline (lit windows)
const winTex = canvasTex(64, 128, (g, w, h) => { g.fillStyle = "#2B1E44"; g.fillRect(0, 0, w, h); const r = seeded(7);
  for (let y = 6; y < h; y += 12) for (let x = 5; x < w; x += 12) { const on = r() < 0.55;
    g.fillStyle = on ? (r() < 0.5 ? "#FFD08A" : "#FF9FC6") : "#3A2C58"; g.fillRect(x, y, 6, 7); } }, true);
const bGeo = new THREE.BoxGeometry(1, 1, 1); bGeo.translate(0, 0.5, 0);
const bMats = [0x8E6BB8, 0xB88AC8, 0x6F5AA0, 0xD6A2B8].map((c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.6 }));
for (let i = 0; i < 170; i++) {
  const x = -320 + R() * 700, z = -120 - R() * 520, near = Math.max(0, 1 - (-z - 120) / 520);
  const h = 14 + Math.pow(R(), 1.6) * (90 + 120 * (1 - Math.abs(x - 30) / 420)) * (0.6 + 0.4 * (1 - near));
  const w = 10 + R() * 18, d = 10 + R() * 18;
  const tex = winTex.clone(); tex.needsUpdate = true; tex.repeat.set(Math.max(1, w / 8), Math.max(1, h / 10));
  const m = new THREE.MeshStandardMaterial({ color: bMats[i % 4].color, roughness: 0.6, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.9, map: tex });
  const b = new THREE.Mesh(bGeo, m); b.scale.set(w, h, d); b.position.set(x, 0, z); scene.add(b);
}
// ---------------- palms
function palm(x, z, s, lean) {
  const g = new THREE.Group(); const trunkM = new THREE.MeshStandardMaterial({ color: 0x5A3A2E, roughness: 0.9 });
  let px = 0, py = 0;
  for (let i = 0; i < 6; i++) { const seg = new THREE.Mesh(new THREE.CylinderGeometry(0.55 - i * 0.05, 0.62 - i * 0.05, 2.2, 7), trunkM);
    px += lean * i * 0.12; seg.position.set(px, py + 1.1, 0); seg.rotation.z = -lean * 0.12 * i; g.add(seg); py += 2.1; }
  const leafM = new THREE.MeshStandardMaterial({ color: 0x1E6B4E, roughness: 0.8, side: THREE.DoubleSide });
  for (let j = 0; j < 8; j++) { const leaf = new THREE.Mesh(new THREE.ConeGeometry(1.1, 7, 3, 1, true), leafM);
    leaf.scale.set(1, 1, 0.25); leaf.position.set(px, py + 0.2, 0); leaf.rotation.set(0, j * Math.PI / 4, 1.95); leaf.translateY(3.2); g.add(leaf); }
  g.position.set(x, 0, z); g.scale.setScalar(s); scene.add(g);
}
for (let i = 0; i < 30; i++) palm(-260 + i * 19 + R() * 6, -92 - R() * 18, 1.6 + R() * 0.9, (R() - 0.5) * 1.6);

// ---------------- lights
scene.add(new THREE.HemisphereLight(0xffb3c8, 0x2a1450, 0.9));
const sunL = new THREE.DirectionalLight(0xffc49a, 1.4); sunL.position.set(-200, 160, -400); scene.add(sunL);
const fill = new THREE.DirectionalLight(0x9a8cff, 0.55); fill.position.set(150, 80, 200); scene.add(fill);

// ---------------- data sets along the promenade
const S = { A: -150, B: -90, C: -30, D: 30, G: 90, E: 150, F: 210 }; const Z = -50;
const brick = canvasTex(64, 64, (g, w, h) => { g.fillStyle = "#fff"; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(0,0,0,0.28)"; g.fillRect(0, h - 5, w, 5); }, true);
function tower(x, color, glow) {
  const m = new THREE.MeshStandardMaterial({ color, roughness: 0.35, metalness: 0.35, map: brick.clone(), emissive: glow || 0x000000, emissiveIntensity: 0.25 });
  m.map.needsUpdate = true; m.map.wrapS = m.map.wrapT = THREE.RepeatWrapping;
  const b = new THREE.Mesh(bGeo, m); b.position.set(x, 0, Z); b.scale.set(7, 0.001, 7); scene.add(b); return b;
}
const tAvatar = tower(S.A - 5, 0x55C6D9), tGta1 = tower(S.A + 5, 0xFF5C9A, 0xff3d8b);
const tGta5 = tower(S.D - 5, 0x8FA0C8), tGta6 = tower(S.D + 5, 0xFF5C9A, 0xff3d8b);
// cash rain (set B): bills fall and pile
const billM = new THREE.MeshStandardMaterial({ color: 0x5FBF73, roughness: 0.7, map: canvasTex(128, 64, (g, w, h) => {
  g.fillStyle = "#8DE09A"; g.fillRect(0, 0, w, h); g.strokeStyle = "#2E7D46"; g.lineWidth = 6; g.strokeRect(6, 6, w - 12, h - 12);
  g.fillStyle = "#2E7D46"; g.font = "bold 40px sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("$", w / 2, h / 2 + 2); }) });
const BILLS = 260, bills = new THREE.InstancedMesh(new THREE.BoxGeometry(2.6, 0.08, 1.2), billM, BILLS); scene.add(bills);
const billPlan = Array.from({ length: BILLS }, (_, i) => { const r = seeded(500 + i);
  return { x: S.B + (r() - 0.5) * 26, z: Z + (r() - 0.5) * 14, d: r() * 1.6, sp: 30 + r() * 25, ry: r() * 6.28, rx: (r() - 0.5) * 2, h: 0.2 + (i / BILLS) * 9 * (0.5 + r() * 0.5) }; });
// game boxes (set C): 32.5 boxes, 1 box = 1 million copies
const boxTex = canvasTex(256, 360, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#FFB24A"); gr.addColorStop(0.55, "#FF3D8B"); gr.addColorStop(1, "#5B1A8E");
  g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,255,255,0.92)"; g.font = "900 190px Montserrat, sans-serif"; g.textAlign = "center"; g.fillText("6", w / 2, h * 0.62);
  g.fillStyle = "#1B0B3A"; g.fillRect(0, 0, w, 34); });
const boxM = [0, 0, 0, 0, 0, 0].map((_, i) => new THREE.MeshStandardMaterial(i === 4 ? { map: boxTex, roughness: 0.4 } : { color: 0x2B1450, roughness: 0.5 }));
const boxes = []; const BOXN = 33;
for (let i = 0; i < BOXN; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(3.2, 4.4, 0.5), boxM);
  const col = i % 6, row = Math.floor(i / 6); b.userData = { x: S.C - 9 + col * 3.6, y: 2.4 + row * 4.8, d: i * 0.03 };
  if (i === BOXN - 1) b.scale.set(1, 0.5, 1); scene.add(b); boxes.push(b); }
// map (set E): Leonida outline, Los Santos square vs Vice City (2x area)
const mapG = new THREE.Group(); mapG.position.set(S.E, 0.2, Z); mapG.userData.k = 1.35; scene.add(mapG);
const leoShape = new THREE.Shape([[-14, -16], [10, -18], [16, -6], [12, 8], [16, 20], [4, 26], [-6, 18], [-16, 10], [-12, -2]].map(([x, y]) => new THREE.Vector2(x, y)));
const leo = new THREE.Mesh(new THREE.ExtrudeGeometry(leoShape, { depth: 1.2, bevelEnabled: false }), new THREE.MeshStandardMaterial({ color: 0x3F8F6B, roughness: 0.8 }));
leo.rotation.x = -Math.PI / 2; mapG.add(leo);
const lsT = new THREE.Mesh(new THREE.BoxGeometry(7, 2.4, 7), new THREE.MeshStandardMaterial({ color: 0x9AA6C8, roughness: 0.5 }));
lsT.position.set(-6, 1.2, 4); mapG.add(lsT);
const vcT = new THREE.Mesh(new THREE.BoxGeometry(9.9, 2.4, 9.9), new THREE.MeshStandardMaterial({ color: 0xFF5C9A, roughness: 0.4, emissive: 0xff3d8b, emissiveIntensity: 0.3 }));
vcT.position.set(6, 1.2, -6); mapG.add(vcT);
// gold (set F): 15 bars, each 100 M$
const goldM = new THREE.MeshStandardMaterial({ color: 0xFFC94A, roughness: 0.28, metalness: 0.9, emissive: 0x6a4200, emissiveIntensity: 0.25 });
const golds = []; for (let i = 0; i < 15; i++) { const g = new THREE.Mesh(new THREE.BoxGeometry(5.2, 1.6, 2.6), goldM);
  const layer = i < 5 ? 0 : i < 9 ? 1 : i < 12 ? 2 : i < 14 ? 3 : 4, idx = [0, 5, 9, 12, 14][layer], n = [5, 4, 3, 2, 1][layer];
  g.userData = { x: S.F + ((i - idx) - (n - 1) / 2) * 5.6, y: 0.8 + layer * 1.65, d: i * 0.07 }; scene.add(g); golds.push(g); }

// trailer billboard (set G)
const scrTex = canvasTex(640, 360, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, "#2A0E4E"); gr.addColorStop(1, "#7A1D5E");
  g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,255,255,0.95)"; g.beginPath(); g.moveTo(w / 2 - 50, h / 2 - 62); g.lineTo(w / 2 - 50, h / 2 + 62); g.lineTo(w / 2 + 64, h / 2); g.fill();
  g.fillStyle = "#FF3D8B"; g.fillRect(0, h - 14, w * 0.62, 14); g.fillStyle = "rgba(255,255,255,0.25)"; g.fillRect(w * 0.62, h - 14, w * 0.38, 14); });
const board = new THREE.Group(); board.position.set(S.G, 0, Z); scene.add(board);
const frameM = new THREE.MeshStandardMaterial({ color: 0x1B0B3A, roughness: 0.5 });
const scr = new THREE.Mesh(new THREE.BoxGeometry(30, 17, 0.8), [frameM, frameM, frameM, frameM, new THREE.MeshBasicMaterial({ map: scrTex }), frameM]);
scr.position.y = 15; board.add(scr);
[-9, 9].forEach((x) => { const post = new THREE.Mesh(new THREE.BoxGeometry(1, 7, 1), frameM); post.position.set(x, 3.5, -0.2); board.add(post); });
// "the most expensive film" stack next to the gold (set F)
const filmM = new THREE.MeshStandardMaterial({ color: 0x9AA0B4, roughness: 0.45, metalness: 0.6 });
const films = []; for (let i = 0; i < 5; i++) { const f = new THREE.Mesh(new THREE.BoxGeometry(5.2, 1.6, 2.6), filmM);
  const layer = i < 3 ? 0 : 1, idx = [0, 3][layer], n = [3, 2][layer];
  f.userData = { x: S.F + 17 + ((i - idx) - (n - 1) / 2) * 5.6, y: 0.8 + layer * 1.65, d: i * 0.07 }; scene.add(f); films.push(f); }
golds.forEach((g) => (g.userData.x -= 6));

// ---------------- camera path: [time, pos, look]
const st = (x, h, dist, lookH) => [[x, h, Z + dist], [x, lookH, Z]];
const keys = [
  [0, [S.A - 30, 70, 210], [S.A - 20, 40, -400]],
  [Math.max(0.9, K.avatar - 0.3), ...st(S.A, 6, 118, 30)],
  [K.cines, ...st(S.A, 6, 122, 30)],
  [K.l1 + 0.6, ...st(S.B, 12, 46, 7)],
  [K.horas + 0.3, ...st(S.B, 14, 50, 8)],
  [K.l2 + 0.15, [S.B + 20, 60, Z + 120], [S.B + 20, 30, Z - 200]],
  [K.l3 + 0.55, ...st(S.C, 12, 74, 18)],
  [K.copias + 0.6, ...st(S.C, 12, 78, 18)],
  [K.l4 + 0.6, ...st(S.D, 6, 118, 30)],
  [K.cinco + 0.6, ...st(S.D, 6, 122, 30)],
  [K.l6 + 0.6, ...st(S.G, 12, 84, 20)],
  [K.dia6 + 0.4, ...st(S.G, 12, 88, 20)],
  [K.l7 + 0.7, [S.E, 92, Z + 62], [S.E, 0, Z + 10]],
  [K.santos + 0.4, [S.E + 3, 86, Z + 58], [S.E + 2, 0, Z + 10]],
  [K.l9 + 0.6, ...st(S.F + 2, 9, 104, 12)],
  [K.l10 + 0.4, ...st(S.F + 2, 9, 108, 12)],
  [K.l11 + 0.1, ...st(S.F + 2, 10, 112, 12)],
  [K.l11 + 1.2, [30, 95, 260], [30, 60, -420]],
  [K.l12, [30, 80, 230], [30, 55, -420]],
  [DUR, [10, 70, 210], [20, 52, -420]],
];
const smooth = (x) => x * x * (3 - 2 * x);
function camAt(t) {
  let i = 0; while (i < keys.length - 2 && t > keys[i + 1][0]) i++;
  const [t0, p0, l0] = keys[i], [t1, p1, l1] = keys[i + 1];
  const u = smooth(Math.min(1, Math.max(0, (t - t0) / Math.max(0.001, t1 - t0))));
  const lerp = (a, b) => a.map((v, j) => v + (b[j] - v) * u);
  return [lerp(p0, p1), lerp(l0, l1)];
}
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const eo = (x) => 1 - Math.pow(1 - clamp01(x), 3);
const grow = (m, h, t, t0, dur) => { const v = Math.max(0.001, h * eo((t - t0) / dur)); m.scale.y = v; m.material.map.repeat.set(1, v / 1.6); return v; };

// ---------------- labels pinned to 3D points
const tags = {}; document.querySelectorAll(".tag").forEach((el) => (tags[el.id] = el));
const v3 = new THREE.Vector3();
function pin(id, x, y, z, op) { const el = tags[id]; v3.set(x, y, z).project(cam);
  const sx = (v3.x * 0.5 + 0.5) * 1080, sy = (-v3.y * 0.5 + 0.5) * 1920;
  el.style.left = sx.toFixed(1) + "px"; el.style.top = sy.toFixed(1) + "px"; el.style.opacity = (v3.z < 1 ? op : 0).toFixed(3); }
const win = (t, a, b, f) => clamp01(Math.min((t - a) / (f || 0.25), (b - t) / (f || 0.25)));

function render(t) {
  const [p, l] = camAt(t); cam.position.set(p[0], p[1], p[2]); cam.lookAt(l[0], l[1], l[2]); cam.updateMatrixWorld(true);
  // A: Avatar (2.920) vs GTA 6 day one (3.790)
  const hA = grow(tAvatar, 29.2, t, K.avatar - 0.2, 0.9), hG = grow(tGta1, 37.9, t, K.dia, 1.0);
  pin("tg-avatar", S.A - 5, hA + 2, Z, win(t, K.avatar + 0.3, K.l1 + 0.3));
  pin("tg-gta1", S.A + 5, hG + 2, Z, win(t, K.dia + 0.5, K.l1 + 0.3));
  // B: cash rain
  const mtx = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), sc = new THREE.Vector3(1, 1, 1), ps = new THREE.Vector3();
  billPlan.forEach((b, i) => { const tt = t - K.l1 - b.d; let y = 120;
    if (tt > 0) y = Math.max(b.h, 60 - b.sp * tt - 4 * tt * tt); const landed = y <= b.h + 0.001;
    e.set(landed ? 0 : b.rx + tt * 3, b.ry + (landed ? 0 : tt * 2), landed ? 0 : tt * 1.5); q.setFromEuler(e);
    ps.set(b.x, t < K.l1 ? -50 : y, b.z); mtx.compose(ps, q, sc); bills.setMatrixAt(i, mtx); });
  bills.instanceMatrix.needsUpdate = true;
  // C: the wall of game boxes (1 box = 1 million copies)
  boxes.forEach((b) => { const u = eo((t - K.vendido - b.userData.d) / 0.5);
    b.position.set(b.userData.x, b.userData.y - (b === boxes[BOXN - 1] ? 1.1 : 0) + (1 - u) * 40, Z); b.rotation.set((1 - u) * 1.2, (1 - u) * 2, 0); b.visible = u > 0; });
  pin("tg-copias", S.C, 31, Z, win(t, K.copias - 0.1, K.l4 + 0.2));
  // D: GTA 5 (800) vs GTA 6 (3.790)
  const h5 = grow(tGta5, 8, t, K.ochocientos - 0.1, 0.6), h6 = grow(tGta6, 37.9, t, K.l5 + 0.1, 1.0);
  pin("tg-gta5", S.D - 5, h5 + 2, Z, win(t, K.ochocientos + 0.2, K.l6 + 0.3));
  pin("tg-gta6", S.D + 5, h6 + 2, Z, win(t, K.l5 + 0.7, K.l6 + 0.3));
  // G: the trailer billboard and its views
  const bu = eo((t - K.l6 + 0.2) / 0.5); board.scale.set(Math.max(0.001, bu), Math.max(0.001, bu), 1); board.visible = bu > 0;
  pin("tg-views", S.G, 28.5, Z, win(t, K.noventa - 0.3, K.l7 + 0.3));
  // E: the map
  const mu = eo((t - K.leonida + 0.3) / 0.6); mapG.scale.set(1.35, Math.max(0.01, mu) * 1.35, 1.35);
  lsT.scale.y = Math.max(0.01, eo((t - K.l8) / 0.4)); vcT.scale.y = Math.max(0.01, eo((t - K.doble + 0.1) / 0.4));
  pin("tg-leonida", S.E - 3, 3, Z + 18, win(t, K.leonida, K.l8 + 0.2));
  pin("tg-ls", S.E - 8.1, 4, Z + 5.4, win(t, K.santos - 0.4, K.l9 + 0.2));
  pin("tg-vc", S.E + 8.1, 4, Z - 8.1, win(t, K.vice, K.l9 + 0.2));
  // F: gold bars vs the most expensive film
  golds.forEach((g) => { const u = eo((t - K.mil9 + 0.4 - g.userData.d) / 0.35); g.position.set(g.userData.x, g.userData.y + (1 - u) * 25, Z); g.visible = u > 0; });
  films.forEach((f) => { const u = eo((t - K.pelicula + 0.2 - f.userData.d) / 0.35); f.position.set(f.userData.x, f.userData.y + (1 - u) * 25, Z); f.visible = u > 0; });
  pin("tg-oro", S.F - 6, 10.5, Z, win(t, K.dolares9 - 0.2, K.l11 + 0.3));
  pin("tg-peli", S.F + 17, 5.5, Z, win(t, K.pelicula + 0.2, K.l11 + 0.3));
  // the sun sinks slowly over the whole film
  sun.position.y = 150 - 40 * (t / DUR);
  renderer.render(scene, cam);
}
const clock = { t: 0 };
tl.to(clock, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(clock.t) }, 0);
render(0);
// ---------------- big overlay lines (timeline-driven)
const cnt = document.getElementById("bg-count-n"), num = { v: 0 };
const fmt = (v) => Math.round(v).toLocaleString("es-ES").replace(/ /g, ".") + " $";
tl.fromTo("#bg-count", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.6)" }, K.l1);
tl.fromTo(num, { v: 0 }, { v: 3790000000, duration: K.millones1 - K.l1 + 0.3, ease: "power2.out", onUpdate: () => (cnt.textContent = fmt(num.v)) }, K.l1);
tl.fromTo("#bg-24", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, K.horas - 0.25);
tl.to(["#bg-count", "#bg-24"], { opacity: 0, duration: 0.18 }, K.l2 - 0.1);
tl.fromTo("#bg-pero", { opacity: 0, scale: 1.6, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }, K.loco - 0.2);
tl.to("#bg-pero", { opacity: 0, duration: 0.2 }, K.l3 + 0.2);
tl.fromTo("#bg-x5", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, K.cinco);
tl.to("#bg-x5", { opacity: 0, duration: 0.2 }, K.l6 + 0.1);
tl.fromTo("#bg-final", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, K.lanzamiento);
tl.to("#bg-final", { opacity: 0, duration: 0.25 }, K.l12 - 0.1);
tl.fromTo("#bg-cta", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, K.l12);
const vn = document.getElementById("tg-views-n"), vv = { v: 0 };
tl.fromTo(vv, { v: 0 }, { v: 90000000, duration: 0.9, ease: "power2.out", onUpdate: () => (vn.textContent = Math.round(vv.v).toLocaleString("es-ES").replace(/\u00a0/g, ".")) }, K.noventa - 0.3);
""".replace("__K__", K)
    # sounds
    sfx(0.05, "barrido-largo.wav", 0.45)
    sfx(k["avatar"] - 0.2, "subida-1.wav", 0.35)
    sfx(k["dia"] + 0.9, "golpe.wav", 0.55)
    sfx(k["l1"], "monedas.wav", 0.45)
    sfx(k["horas"] - 0.25, "pop-1.wav", 0.45)
    sfx(k["l2"] - 0.1, "barrido-1.wav", 0.5)
    sfx(k["loco"] - 0.2, "golpe.wav", 0.5)
    for j in range(0, 33, 3):
        sfx(k["vendido"] + j * 0.03 + 0.4, f"caja-{j % 2 + 1}.wav", 0.25)
    sfx(k["ochocientos"] + 0.4, "pop-2.wav", 0.4)
    sfx(k["l5"] + 0.1, "subida-2.wav", 0.35)
    sfx(k["cinco"], "golpe.wav", 0.6)
    sfx(k["l6"], "barrido-1.wav", 0.4)
    sfx(k["noventa"] - 0.3, "subida-2.wav", 0.3)
    sfx(k["l7"], "barrido-2.wav", 0.45)
    sfx(k["doble"] - 0.1, "pop-1.wav", 0.45)
    for j in range(0, 15, 2):
        sfx(k["mil9"] - 0.1 + j * 0.07, "oro.wav", 0.3)
    sfx(k["pelicula"], "pop-2.wav", 0.4)
    sfx(k["l11"] + 0.2, "barrido-largo.wav", 0.4)
    sfx(k["lanzamiento"] - 1.2, "subida-1.wav", 0.4)
    sfx(k["lanzamiento"] + 0.25, "impacto.wav", 0.55)
    sfx(k["l12"], "pop-2.wav", 0.5)
    dur = TOTAL
    return f"""<template>
<style>{css}</style>
<div id="root" data-composition-id="mundo" data-width="1080" data-height="1920" data-duration="{dur}">
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


# ------------------------------------------------------------------ captions
CAPS = [
    "En un solo día, GTA 6 ganó más dinero que Avatar en toda su historia en cines.",
    "3.790 millones de dólares, en 24 horas.",
    "Pero lo más loco no es eso.",
    "Antes de salir, ya había vendido 32,5 millones de copias.",
    "GTA 5 ganó 800 millones en su primer día.",
    "GTA 6 multiplicó esa cifra casi por cinco.",
    "Su primer tráiler ya había hecho 90 millones de vistas en un solo día.",
    "Y su mapa, Leonida, es el más grande que Rockstar ha creado.",
    "Solo Vice City es el doble de Los Santos.",
    "Se estima que costó hasta 1.500 millones de dólares.",
    "Más que cualquier película jamás filmada.",
    "Esto ya no es un videojuego. Es el lanzamiento más grande de la historia del entretenimiento.",
]
HL = {"día,", "avatar", "3.790", "loco", "32,5", "800", "cinco.", "leonida,", "doble", "1.500", "videojuego.", "historia",
      "jugando,", "esperando?", "90", "película"}


def build_subs():
    groups = []
    for i, text in enumerate(CAPS):  # the last spoken line is shown as the big CTA instead
        toks = text.split()
        chunks, cur = [], []
        for tkn in toks:
            cur.append(tkn)
            if len(cur) >= 3 or (tkn[-1] in ",.?" and len(cur) >= 2):
                chunks.append(cur); cur = []
        if cur:
            if chunks and len(cur) == 1: chunks[-1] += cur
            else: chunks.append(cur)
        a, b = ls(i), le(i)
        tot = sum(len(t) + 1 for t in toks); pos = 0
        for ch in chunks:
            n = sum(len(t) + 1 for t in ch)
            groups.append((round(a + (b - a) * pos / tot, 3), round(a + (b - a) * (pos + n) / tot, 3), ch)); pos += n
    starts = [max(0.05, s - 0.06) for s, _, _ in groups]
    html, js = [], []
    for k, (s, e, ch) in enumerate(groups):
        nxt = starts[k + 1] if k + 1 < len(groups) else TOTAL
        end = min(nxt, max(e + 0.35, s + 0.5))
        if k == len(groups) - 1: end = min(TOTAL, e + 0.35)
        start = 0.0 if k == 0 else starts[k]
        words = []
        for j, w in enumerate(ch):
            cls = "w hl" if w.lower() in HL else "w"
            words.append(f'<span class="{cls}" id="su-{k}-{j}">{w}</span>')
            t_w = round(s + (e - s) * j / len(ch), 3)
            if k > 0:
                js.append(f'tl.fromTo("#su-{k}-{j}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "back.out(2.2)" }}, {t_w});')
        html.append(f'<div class="grp clip" id="su-{k}" data-start="{start}" data-duration="{round(end - start, 3)}" data-track-index="0"><p>{" ".join(words)}</p></div>')
    return f"""<template>
<style>
  #root {{ position:absolute; inset:0; pointer-events:none; }}
  .grp {{ position:absolute; left:0; top:300px; width:1080px; height:190px; display:flex; align-items:center; justify-content:center; overflow:visible; }}
  .grp p {{ margin:0; width:880px; text-align:center; font-family:'Montserrat', sans-serif; font-weight:900; font-size:76px; line-height:1.08;
           color:#FFFFFF; text-transform:uppercase; letter-spacing:-0.01em;
           text-shadow: 0 5px 0 rgba(40,10,70,0.75), 0 10px 26px rgba(0,0,0,0.5); }}
  .w {{ display:inline-block; margin:0 6px; }}
  .hl {{ color:{GOLD}; }}
</style>
<div id="root" data-composition-id="subtitulos" data-width="1080" data-height="1920" data-duration="{TOTAL}">
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


def _dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                      capture_output=True, text=True).stdout), 3)


def build_index():
    DUR = {p.name: _dur(p) for p in (OUT / "assets" / "audio").glob("*.wav")}
    lanes, audio = [], []
    for n, (t, name, vol) in enumerate(sorted(SFX)):
        d = DUR[name]
        lane = next((i for i, busy in enumerate(lanes) if busy <= t), None)
        if lane is None: lanes.append(0); lane = len(lanes) - 1
        lanes[lane] = t + d
        audio.append(f'      <audio id="fx{n}" class="clip" src="assets/audio/{name}" data-start="{max(0, t)}" data-duration="{d}" data-track-index="{6 + lane}" data-volume="{vol}"></audio>')
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#1B0B3A; }}
      #root {{ position:relative; width:1080px; height:1920px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="mundo" data-composition-id="mundo" data-composition-src="compositions/mundo.html" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="subtitulos" data-composition-id="subtitulos" data-composition-src="compositions/subtitulos.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:40"></div>
      <audio id="voz" class="clip" src="assets/audio/voz.wav" data-start="0" data-duration="{DUR['voz.wav']}" data-track-index="3" data-volume="1"></audio>
      <audio id="musica" class="clip" src="assets/audio/musica.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="0.13" data-fade-out="2"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    comp = OUT / "compositions"; comp.mkdir(exist_ok=True)
    (comp / "mundo.html").write_text(build_mundo(), encoding="utf-8")
    (comp / "subtitulos.html").write_text(build_subs(), encoding="utf-8")
    (OUT / "index.html").write_text(build_index(), encoding="utf-8")
    print(f"total {TOTAL}s; sfx {len(SFX)}")


main()
