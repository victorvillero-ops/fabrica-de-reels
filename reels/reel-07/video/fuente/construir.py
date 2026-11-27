"""Reel 07 — 7 secretos de GTA 6 que los jugadores han encontrado. Leonida at sunset, one low-poly set per secret:
a dog with sunglasses on a jet ski, a comms tower whose egg splats on a passing car, a giant newspaper, the skunk ape in the
swamp, a living-room console, a house + polaroid + the garage conspiracist, and a night road in Kelly County with a UFO.
The last line runs back into the hook so the reel loops."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "serie"))
from serie import Reel, GOLD, PINK

R = Reel(Path(__file__).parent)
w = R.wt
K = {
    "perro": w(0, "perro"), "moto": w(0, "moto"),
    "l1": R.ls(1), "primero": w(1, "primero"), "siete": w(1, "7", ["siete"]),
    "l2": R.ls(2), "torre": w(2, "torre"), "nido": w(2, "nido"),
    "l3": R.ls(3), "tira": w(3, "tira"), "estampa": w(3, "estampa"), "coche3": w(3, "coche"),
    "l4": R.ls(4), "periodico": w(4, "periodico"), "anuncia": w(4, "anuncia"), "leonida": w(4, "leonida"), "libre": w(4, "libre"),
    "furries": w(4, "furries", ["furris", "furri"]),
    "l5": R.ls(5), "bigfoot": w(5, "bigfoot", ["big"]), "aqui": w(5, "aqui"), "simio": w(5, "simio"), "pantanos": w(5, "pantanos"),
    "l6": R.ls(6), "casa6": w(6, "casa"), "consola": w(6, "consola"), "videojuegos": w(6, "videojuegos"),
    "l7": R.ls(7), "foto": w(7, "foto"), "otro": w(7, "otro"), "anio": w(7, "2021", ["dos"]),
    "l8": R.ls(8), "garaje": w(8, "garaje"), "convencido": w(8, "convencido"), "videojuego": w(8, "videojuego"),
    "l9": R.ls(9), "solo9": w(9, "solo"), "dos9": w(9, "2", ["dos"]), "condado": w(9, "condado"), "kelly": w(9, "kelly"),
    "l10": R.ls(10), "salva": w(10, "salva"), "ovni": w(10, "ovni"), "traele": w(10, "traele", ["trae"]), "coche10": w(10, "coche"),
    "abducido": w(10, "abducido"),
    "l11": R.ls(11), "y11": w(11, "y"), "recuerda": w(11, "recuerda"),
    "end": R.total,
}
k = K

# ------------------------------------------------------------------ HUD (night conditions) and DOM overlays
PERSON = (f'<svg class="b" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#1B0B3A" stroke="{GOLD}" stroke-width="6"/>'
          f'<circle cx="50" cy="36" r="12" fill="{GOLD}"/><path d="M28 76 Q28 54 50 54 Q72 54 72 76 Z" fill="{GOLD}"/></svg>')
def item(label, inner):
    return f'<div class="it"><div class="lab">{label}</div>{inner}</div>'
HOUSE_SVG = """<svg viewBox="0 0 376 300" width="376" height="300">
<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A3A8E"/><stop offset="0.6" stop-color="#F0708E"/><stop offset="1" stop-color="#FFC27A"/></linearGradient></defs>
<rect width="376" height="300" fill="url(#pg)"/><circle cx="300" cy="120" r="40" fill="#FFE7A0" opacity="0.9"/>
<rect y="232" width="376" height="68" fill="#5E4A3A"/>
<polygon points="40,150 140,96 240,150" fill="#7A2A5E"/><rect x="52" y="148" width="176" height="86" fill="#F2A7C3"/>
<rect x="228" y="168" width="92" height="66" fill="#F8D6E2"/><rect x="224" y="162" width="100" height="10" fill="#7A2A5E"/>
<g fill="#E9D9C2">""" + "".join(f'<rect x="238" y="{176 + i * 13}" width="72" height="9"/>' for i in range(4)) + """</g>
<rect x="70" y="170" width="34" height="28" fill="#FFD08A"/><rect x="118" y="170" width="34" height="28" fill="#FFD08A"/><rect x="168" y="186" width="24" height="48" fill="#FF3D8B"/>
<path d="M20 234 Q26 170 30 120" stroke="#3A2A22" stroke-width="8" fill="none"/><g fill="#1E5B42"><ellipse cx="18" cy="118" rx="26" ry="8"/><ellipse cx="42" cy="114" rx="26" ry="8"/></g>
<rect width="376" height="300" fill="#C9A47A" opacity="0.18"/></svg>"""

body = f"""
<style>
  .hud {{ position:absolute; left:0; top:540px; width:1080px; display:flex; justify-content:center; align-items:flex-end; gap:30px; opacity:0; }}
  .it {{ display:flex; flex-direction:column; align-items:center; }}
  .lab {{ font-family:'Inter',sans-serif; font-weight:800; font-size:30px; letter-spacing:0.08em; color:#fff; background:#2A0B4A; padding:4px 14px; border-radius:10px; margin-bottom:10px; }}
  .b {{ width:118px; height:118px; display:block; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  .pill {{ display:inline-block; font-family:'Montserrat',sans-serif; font-weight:900; font-size:56px; color:{GOLD}; background:#1B0B3A; border:5px solid {GOLD};
          border-radius:20px; padding:16px 26px 10px; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  #cnt {{ position:absolute; left:64px; top:556px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:54px; color:#2A0B4A; background:{GOLD};
         padding:10px 20px 4px; border-radius:16px; transform:rotate(-6deg); opacity:0; box-shadow:0 8px 0 #2A0B4A; }}
  #night {{ position:absolute; inset:0; opacity:0; background: linear-gradient(180deg, rgba(10,12,50,0.75) 0%, rgba(20,20,70,0.25) 55%, rgba(8,8,40,0.7) 100%); mix-blend-mode: multiply; }}
  #swamp {{ position:absolute; inset:0; opacity:0; background: radial-gradient(ellipse 80% 60% at 50% 58%, rgba(150,230,160,0.10) 0%, rgba(20,70,40,0.62) 100%); mix-blend-mode: multiply; }}
  #glitch {{ position:absolute; inset:0; opacity:0; }}
  #glitch div {{ position:absolute; left:0; width:1080px; mix-blend-mode:screen; }}
  #polaroid {{ position:absolute; left:330px; top:735px; width:420px; height:470px; padding:22px 22px 0; background:#FBF7EF; border-radius:6px; opacity:0;
              box-shadow: 0 24px 50px rgba(0,0,0,0.55); }}
  #polaroid .yr {{ margin-top:16px; text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; font-size:72px; color:#2A0B4A; opacity:0; }}
</style>
<div id="night"></div><div id="swamp"></div>
<div id="glitch"><div style="top:760px;height:34px;background:rgba(46,230,214,0.55)"></div><div style="top:880px;height:16px;background:rgba(255,61,139,0.6)"></div>
  <div style="top:990px;height:46px;background:rgba(255,201,74,0.4)"></div><div style="top:1120px;height:22px;background:rgba(46,230,214,0.5)"></div></div>
<div class="big" id="bg-title" style="top:600px;font-size:150px;opacity:1"><span class="grad">GTA 6</span><br><span class="plate" style="font-size:60px">7 SECRETOS</span><br>
  <span style="font-size:32px;letter-spacing:0.01em">QUE YA HAN ENCONTRADO LOS JUGADORES</span></div>
<div id="cnt">1/7</div>
<div class="hud" id="h9">{item("SOLO", PERSON)}<div id="h9b" style="opacity:0">{item("A PARTIR DE LAS", '<span class="pill">2:00</span>')}</div></div>
<div class="tag" id="tg-perro" style="font-size:64px"><span class="grad">PERRO SOCORRISTA</span><small>con gafas de sol</small></div>
<div class="tag" id="tg-nido" style="font-size:66px"><span class="grad">NIDO</span><small>con huevos</small></div>
<div class="tag" id="tg-ape" style="font-size:64px"><span class="grad">SIMIO MOFETA</span><small>el bigfoot de leonida</small></div>
<div class="tag" id="tg-juegos" style="font-size:62px"><span class="grad">JUEGOS ENTEROS</span><small>en la consola de jason</small></div>
<div class="big" id="bg-conspi" style="top:680px;font-size:56px"><span style="display:inline-block;background:rgba(27,11,58,0.9);padding:16px 30px 10px;border-radius:18px"><span class="grad">CREE QUE VIVE</span><br>EN UN VIDEOJUEGO</span></div>
<div class="big" id="bg-kelly" style="top:900px;font-size:62px"><span class="grad">CONDADO DE KELLY</span><br><span class="plate" style="font-size:34px">TRAS EL CAPÍTULO 1</span></div>
<div class="tag" id="tg-mujer" style="font-size:62px"><span class="grad">SÁLVALA</span></div>
<div class="tag" id="tg-coche" style="font-size:60px"><span class="grad">SU COCHE</span></div>
<div class="big" id="bg-6" style="top:900px;font-size:84px"><span class="plate">Y QUEDAN 6</span></div>
<div class="big" id="bg-plaf" style="top:690px;font-size:110px"><span class="stamp" style="color:{GOLD};border-color:{GOLD}">¡PLAF!</span></div>
<div class="big" id="bg-otro" style="top:650px;font-size:48px"><span class="plate">ESCONDIDA EN OTRO GTA</span></div>
<div id="polaroid">{HOUSE_SVG}<div class="yr">2021</div></div>
<div class="big" id="bg-abd" style="top:1080px;font-size:80px"><span class="stamp">ABDUCIDO: TÚ</span></div>
<div class="big" id="bg-cta" style="top:800px;font-size:100px">¿CUÁL VAS<br>A PROBAR<br><span class="grad">PRIMERO?</span></div>
"""

sets_js = r"""
const std = (c, o) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.7 }, o || {}));
const bas = (c, o) => new THREE.MeshBasicMaterial(Object.assign({ color: c }, o || {}));
function mk(geo, mat, x, y, z, parent) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); (parent || scene).add(m); return m; }
const UPV = new THREE.Vector3(0, 1, 0);
function beam(a, b, r, mat, parent) { const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), d = B.clone().sub(A);
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, d.length(), 6), mat); m.position.copy(A).add(B).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(UPV, d.normalize()); (parent || scene).add(m); return m; }
const HEMI = scene.children.find((o) => o.isHemisphereLight);
const ZR = 12;
// ---- beach road with a dashed gold centre line
const roadTex = canvasTex(512, 64, (g, W, H) => { g.fillStyle = "#2A1E3A"; g.fillRect(0, 0, W, H);
  g.fillStyle = "#FFC94A"; for (let x = 0; x < W; x += 128) g.fillRect(x, H / 2 - 3, 70, 6);
  g.fillStyle = "#E8C8D8"; g.fillRect(0, 2, W, 3); g.fillRect(0, H - 5, W, 3); }, true);
roadTex.repeat.set(2200 / 24, 1);
const road = mk(new THREE.PlaneGeometry(2200, 14), new THREE.MeshStandardMaterial({ map: roadTex, roughness: 0.85 }), 400, 0.06, ZR); road.rotation.x = -Math.PI / 2;
// palms on the sea side, with gaps where a set needs a clear view
const RS = seeded(707);
const GAPS = [[-330, -190], [355, 445], [770, 870], [990, 1110]];
for (let x = -420; x < 1300; x += 30 + RS() * 8) { if (GAPS.some(([a, b]) => x > a && x < b)) continue; palm(x, ZR + 14 + RS() * 6, 1.3 + RS() * 0.5, (RS() - 0.5) * 1.4); }

// ---- shared builders: car (faces +x) and a low-poly person
function makeCar(color) {
  const g = new THREE.Group(); scene.add(g);
  const paint = std(color, { roughness: 0.35, metalness: 0.3 }), glass = std(0x2A1A4A, { roughness: 0.1, metalness: 0.6 });
  const add = (geo, mat, x, y, z) => mk(geo, mat, x, y, z, g);
  add(new THREE.BoxGeometry(4.6, 0.9, 2.0), paint, 0, 0.75, 0);
  add(new THREE.BoxGeometry(2.4, 0.75, 1.8), glass, -0.35, 1.575, 0);
  add(new THREE.BoxGeometry(2.2, 0.12, 1.84), paint, -0.35, 1.98, 0);
  const wheelM = std(0x15101F, { roughness: 0.8 }), wheels = [];
  for (const [x, z] of [[1.45, 1.0], [1.45, -1.0], [-1.45, 1.0], [-1.45, -1.0]]) { const wh = add(new THREE.CylinderGeometry(0.4, 0.4, 0.34, 18), wheelM, x, 0.4, z); wh.rotation.x = Math.PI / 2; wheels.push(wh); }
  const headM = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xFFF2C0, emissiveIntensity: 1.2 });
  const tailM = new THREE.MeshStandardMaterial({ color: 0xff2040, emissive: 0xff2040, emissiveIntensity: 0.9 });
  for (const z of [0.65, -0.65]) { add(new THREE.BoxGeometry(0.08, 0.2, 0.42), headM, 2.31, 0.9, z); add(new THREE.BoxGeometry(0.08, 0.2, 0.42), tailM, -2.31, 0.9, z); }
  g.scale.setScalar(1.6);
  return { g, headM, wheels };
}
function person(shirt, pants, skinC, hairC, longHair) {
  const g = new THREE.Group(); scene.add(g);
  mk(new THREE.CylinderGeometry(0.24, 0.2, 0.9, 10), std(pants), 0, 0.45, 0, g);
  mk(new THREE.CylinderGeometry(0.3, 0.25, 0.75, 10), std(shirt), 0, 1.27, 0, g);
  const head = mk(new THREE.SphereGeometry(0.23, 14, 10), std(skinC), 0, 1.86, 0, g);
  const hair = mk(new THREE.SphereGeometry(0.25, 14, 10), std(hairC), 0, 1.93, -0.02, g); hair.scale.set(1, 0.6, 1);
  if (longHair) { const lh = mk(new THREE.BoxGeometry(0.44, 0.5, 0.2), std(hairC), 0, 1.72, -0.16, g); }
  const arms = [1, -1].map((s) => { const p = new THREE.Group(); p.position.set(s * 0.37, 1.58, 0); g.add(p);
    mk(new THREE.CylinderGeometry(0.09, 0.08, 0.7, 8), std(shirt), 0, -0.35, 0, p); return p; });
  g.userData.arms = arms; g.userData.head = head; g.scale.setScalar(1.6);
  return g;
}

// ================= 1. dog with sunglasses on a jet ski, rescuing a swimmer
const DOGZ = 80;
const ring = mk(new THREE.TorusGeometry(1.15, 0.36, 10, 24), std(0xFF6A3D, { roughness: 0.5 }), 7, -0.45, DOGZ); ring.rotation.x = Math.PI / 2;
const swimmer = person(0x2EE6D6, 0x2A1A4A, 0xC98B6B, 0x2A1A1A); swimmer.position.set(7, -1.9, DOGZ);
const jet = new THREE.Group(); scene.add(jet);
const jp = std(0xFF3D8B, { roughness: 0.35, metalness: 0.3 }), jw = std(0xF4F0FF, { roughness: 0.4 }), jd = std(0x1B0B3A), goldM = std(0xFFC94A, { metalness: 0.6, roughness: 0.3 });
mk(new THREE.BoxGeometry(3.4, 0.55, 1.3), jw, 0, 0.1, 0, jet);
mk(new THREE.BoxGeometry(3.0, 0.35, 1.2), jp, -0.1, 0.5, 0, jet);
{ const nose = mk(new THREE.ConeGeometry(0.66, 1.4, 4), jp, 2.35, 0.3, 0, jet); nose.rotation.set(Math.PI / 4, 0, -Math.PI / 2); }
mk(new THREE.BoxGeometry(1.6, 0.3, 0.6), jd, -0.5, 0.82, 0, jet);
mk(new THREE.CylinderGeometry(0.08, 0.1, 0.7, 8), jd, 0.95, 0.95, 0, jet);
{ const bar = mk(new THREE.CylinderGeometry(0.06, 0.06, 1.3, 8), goldM, 0.95, 1.3, 0, jet); bar.rotation.x = Math.PI / 2; }
const fur = std(0xD08B4B), furD = std(0x6B3A1E);
const dog = new THREE.Group(); dog.position.set(-0.35, 0.95, 0); jet.add(dog);
mk(new THREE.BoxGeometry(0.9, 0.85, 0.62), fur, 0, 0.45, 0, dog);
mk(new THREE.BoxGeometry(0.62, 0.56, 0.56), fur, 0.28, 1.08, 0, dog);
mk(new THREE.BoxGeometry(0.36, 0.26, 0.36), fur, 0.7, 0.98, 0, dog);
mk(new THREE.BoxGeometry(0.1, 0.1, 0.16), jd, 0.9, 1.05, 0, dog);
for (const s of [1, -1]) { const e = mk(new THREE.BoxGeometry(0.16, 0.34, 0.12), furD, 0.18, 1.36, s * 0.26, dog); e.rotation.x = s * 0.35;
  mk(new THREE.BoxGeometry(0.52, 0.16, 0.16), fur, 0.62, 0.6, s * 0.2, dog); }
mk(new THREE.BoxGeometry(0.08, 0.09, 0.78), goldM, 0.62, 1.24, 0, dog);
const lensM = std(0x14061F, { roughness: 0.1, metalness: 0.6, emissive: 0xFF3D8B, emissiveIntensity: 1.3 });
for (const s of [1, -1]) { mk(new THREE.BoxGeometry(0.1, 0.24, 0.36), goldM, 0.62, 1.12, s * 0.2, dog); mk(new THREE.BoxGeometry(0.12, 0.2, 0.3), lensM, 0.64, 1.12, s * 0.2, dog);
  mk(new THREE.BoxGeometry(0.4, 0.05, 0.04), goldM, 0.42, 1.2, s * 0.37, dog); }
dog.rotation.y = 0.6;
const tail = mk(new THREE.CylinderGeometry(0.05, 0.08, 0.5, 6), fur, -0.5, 0.55, 0, dog); tail.rotation.z = 0.9;
jet.scale.setScalar(1.5);
const wakeM = bas(0xFFFFFF, { transparent: true, opacity: 0, depthWrite: false });
const wake = mk(new THREE.PlaneGeometry(16, 1.8), wakeM, 0, -0.5, DOGZ); wake.rotation.x = -Math.PI / 2;
const sprayM = bas(0xFFFFFF, { transparent: true, opacity: 0.85 });
const SPRAY = []; for (let i = 0; i < 12; i++) SPRAY.push(mk(new THREE.SphereGeometry(0.35, 8, 6), sprayM, 0, -5, DOGZ));

// ================= 2. comms tower with a nest; an egg falls on a passing car
const TX = 220, TZ = 4, TH = 28;
const steel = std(0xD9C8E8, { metalness: 0.5, roughness: 0.4 }), steelR = std(0xFF3D8B, { metalness: 0.3, roughness: 0.5 });
const tower = new THREE.Group(); tower.position.set(TX, 0, TZ); scene.add(tower);
const legPt = (y, sx, sz) => { const h = 3 - 2.2 * y / TH; return [sx * h, y, sz * h]; };
const CORN = [[1, 1], [1, -1], [-1, -1], [-1, 1]];
for (const [sx, sz] of CORN) beam(legPt(0, sx, sz), legPt(TH, sx, sz), 0.18, steel, tower);
for (let y = 0, n = 0; y < TH; y += 4, n++) for (let c = 0; c < 4; c++) { const [ax, az] = CORN[c], [bx, bz] = CORN[(c + 1) % 4];
  beam(legPt(y, ax, az), legPt(y + 4, bx, bz), 0.07, steel, tower); beam(legPt(y + 4, ax, az), legPt(y + 4, bx, bz), 0.1, n % 2 ? steel : steelR, tower); }
mk(new THREE.BoxGeometry(3.2, 0.4, 3.2), steel, 0, TH, 0, tower);
beam([0, TH, 0], [0, TH + 4, 0], 0.12, steel, tower);
const beaconM = std(0xff2040, { emissive: 0xff2040, emissiveIntensity: 2 });
mk(new THREE.SphereGeometry(0.4, 12, 8), beaconM, 0, TH + 4.2, 0, tower);
for (const [x, z, r] of [[1.4, -1.4, 0.6], [-1.4, -1.2, -0.7]]) { const d = mk(new THREE.CylinderGeometry(1.0, 1.0, 0.25, 18), steel, x, TH - 2.2, z, tower); d.rotation.set(Math.PI / 2, r, 0); }
beam([0, TH - 0.4, 0], [0, TH - 0.4, 8.6], 0.14, steelR, tower);
const nestM = std(0x6B4A2E, { roughness: 1 });
{ const nest = mk(new THREE.TorusGeometry(0.85, 0.36, 8, 16), nestM, 0, TH, 8.2, tower); nest.rotation.x = Math.PI / 2;
  mk(new THREE.CylinderGeometry(0.85, 0.6, 0.3, 14), nestM, 0, TH - 0.2, 8.2, tower); }
const eggM = std(0xFFF4DC, { roughness: 0.4 });
for (const [x, z] of [[-0.3, 7.9], [0.05, 8.55]]) { const e = mk(new THREE.SphereGeometry(0.4, 12, 10), eggM, x, TH + 0.35, z, tower); e.scale.set(1, 1.3, 1); }
const egg = mk(new THREE.SphereGeometry(0.6, 14, 10), eggM, 0, 0, 0); egg.scale.set(1, 1.3, 1);
{ const bird = new THREE.Group(); bird.position.set(-0.9, TH + 0.5, 8.1); tower.add(bird); const bm = std(0xFF3D8B);
  mk(new THREE.SphereGeometry(0.42, 12, 10), bm, 0, 0, 0, bird).scale.set(1.3, 0.9, 0.9); mk(new THREE.SphereGeometry(0.26, 10, 8), bm, 0.45, 0.4, 0, bird);
  const bk = mk(new THREE.ConeGeometry(0.1, 0.3, 6), goldM, 0.75, 0.4, 0, bird); bk.rotation.z = -Math.PI / 2; }
const car1 = makeCar(0xFF3D8B);
const splat = new THREE.Group(); splat.position.set(-0.35, 2.06, 0); car1.g.add(splat);
const yolkM = std(0xFFB800, { roughness: 0.25, emissive: 0xFF9A00, emissiveIntensity: 0.25 });
mk(new THREE.SphereGeometry(0.5, 16, 10), yolkM, 0, 0, 0, splat).scale.set(1.4, 0.14, 1.0);
mk(new THREE.SphereGeometry(0.3, 12, 8), yolkM, 0.1, 0.05, 0.05, splat).scale.set(1, 0.5, 1);
for (let i = 0; i < 5; i++) { const s = mk(new THREE.TetrahedronGeometry(0.14), eggM, Math.cos(i * 1.3) * 0.7, 0.06, Math.sin(i * 1.3) * 0.5, splat); s.rotation.set(i, i * 2, i); }
const DROPS = []; { const rd = seeded(31); for (let i = 0; i < 16; i++) { const a = rd() * Math.PI * 2, s = 2 + rd() * 4;
  DROPS.push({ m: mk(new THREE.SphereGeometry(0.12 + rd() * 0.12, 8, 6), i % 4 ? yolkM : eggM, 0, -9, 0), v: [Math.cos(a) * s, 3 + rd() * 5, Math.sin(a) * s] }); } }

// ================= 3. a giant newspaper (canvas texture)
const NP = document.createElement("canvas"); NP.width = 720; NP.height = 1000; const npg = NP.getContext("2d");
const npTex = new THREE.CanvasTexture(NP); npTex.encoding = THREE.sRGBEncoding; let npHL = -1;
function drawPaper(hl) { const g = npg, W = 720, H = 1000;
  g.fillStyle = "#F4ECDD"; g.fillRect(0, 0, W, H);
  g.fillStyle = "#FF3D8B"; g.fillRect(30, 30, W - 60, 120);
  g.textAlign = "center"; g.textBaseline = "middle"; g.fillStyle = "#fff"; g.font = "900 62px Montserrat"; g.fillText("VICE CITY HORN", W / 2, 93);
  g.fillStyle = "#2A0B4A"; g.fillRect(30, 162, W - 60, 6); g.font = "800 26px Montserrat"; g.fillText("EDICIÓN ESPECIAL  ·  ÚLTIMA HORA", W / 2, 190); g.fillRect(30, 210, W - 60, 3);
  if (hl > 0) { g.fillStyle = "#FFC94A"; g.fillRect(40, 362, (W - 80) * hl, 232); }
  g.fillStyle = "#1B0B3A"; g.font = "900 104px Montserrat"; g.fillText("LEONIDA,", W / 2, 296); g.fillText("LIBRE DE", W / 2, 420); g.fillText("FURRIES", W / 2, 540);
  g.font = "italic 700 38px Montserrat"; g.fillStyle = "#5B3A6E"; g.fillText("«Governor declares", W / 2, 620); g.fillText("Leonida furry-free»", W / 2, 662);
  g.fillStyle = "#D9CBB4"; g.fillRect(40, 700, 300, 270); g.fillStyle = "#6B3A1E"; g.save(); g.translate(0, 30);
  g.beginPath(); g.ellipse(190, 845, 56, 46, 0, 0, Math.PI * 2); g.fill();
  for (const [x, y] of [[132, 770], [170, 745], [212, 745], [250, 770]]) { g.beginPath(); g.ellipse(x, y, 20, 26, 0, 0, Math.PI * 2); g.fill(); }
  g.strokeStyle = "#E0302F"; g.lineWidth = 16; g.beginPath(); g.arc(190, 812, 112, 0, Math.PI * 2); g.stroke();
  g.beginPath(); g.moveTo(111, 733); g.lineTo(269, 891); g.stroke(); g.restore();
  g.fillStyle = "#9A8A7A"; for (let y = 708; y < 965; y += 22) { g.fillRect(372, y, 308 - ((y * 7) % 60), 8); } }
const paper = new THREE.Group(); paper.position.set(400, 10.5, 8); scene.add(paper);
mk(new THREE.PlaneGeometry(13, 18), new THREE.MeshBasicMaterial({ map: npTex, toneMapped: false }), 0, 0, 0.02, paper);
{ const back = mk(new THREE.PlaneGeometry(13, 18), bas(0xE8DCC8), 0, 0, -0.02, paper); back.rotation.y = Math.PI; }

// ================= 4. swamp with the skunk ape
const SX = -260;
{ const water = mk(new THREE.PlaneGeometry(170, 100), std(0x23402F, { roughness: 0.25, metalness: 0.4 }), SX, -0.35, 90); water.rotation.x = -Math.PI / 2;
  const mud = mk(new THREE.PlaneGeometry(110, 37), std(0x4A3424, { roughness: 1 }), SX, 0.1, 38); mud.rotation.x = -Math.PI / 2; }
const trunkM = std(0x3A2A22, { roughness: 1 }), leafA = std(0x1E4A32, { roughness: 0.9, flatShading: true }), leafB = std(0x2B5A3A, { roughness: 0.9, flatShading: true });
function mangrove(x, z, s) { const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s); scene.add(g);
  for (let i = 0; i < 5; i++) { const a = i * 1.26; beam([Math.cos(a) * 1.3, -0.3, Math.sin(a) * 1.3], [0, 1.7, 0], 0.11, trunkM, g); }
  beam([0, 1.6, 0], [0.4, 6.4, 0.2], 0.3, trunkM, g);
  for (const [dx, dy, dz, r, m] of [[0.4, 7, 0.2, 2.6, leafA], [-1.4, 6.3, 0.6, 1.9, leafB], [1.8, 6.5, -0.4, 2.0, leafB]]) mk(new THREE.IcosahedronGeometry(r, 0), m, dx, dy, dz, g);
  const moss = mk(new THREE.ConeGeometry(0.35, 2.2, 5), std(0x6E7A5A), -1.4, 4.6, 0.6, g); moss.rotation.x = Math.PI; }
{ const rm = seeded(404); mangrove(SX - 11, 71, 1.2); mangrove(SX + 9, 74, 1.1); mangrove(SX - 2, 84, 1.3);
  for (let i = 0; i < 20; i++) { const x = SX - 48 + rm() * 96, z = 60 + rm() * 60; if (Math.abs(x - SX) < 14 && z < 70) continue; mangrove(x, z, 0.8 + rm() * 0.6); }
  const reedM = std(0x5E6B3A); for (let i = 0; i < 46; i++) { const r = mk(new THREE.ConeGeometry(0.07, 1.4 + rm() * 1.2, 4), reedM, SX - 40 + rm() * 80, 0.6, 54 + rm() * 4); r.rotation.z = (rm() - 0.5) * 0.4; } }
const ape = new THREE.Group(); scene.add(ape);
const hair = std(0x4A3326, { roughness: 1, flatShading: true }), hairD = std(0x2E1F17, { roughness: 1, flatShading: true });
mk(new THREE.IcosahedronGeometry(1, 1), hair, 0, 2.65, 0, ape).scale.set(0.95, 1.35, 0.72);
const apeHead = new THREE.Group(); apeHead.position.set(0.15, 4.15, 0); ape.add(apeHead);
mk(new THREE.IcosahedronGeometry(0.58, 1), hair, 0, 0, 0, apeHead);
mk(new THREE.SphereGeometry(0.36, 12, 10), std(0x8A6A55), 0.32, -0.08, 0, apeHead).scale.set(0.55, 0.9, 0.95);
for (const s of [1, -1]) mk(new THREE.SphereGeometry(0.06, 8, 6), std(0xFFE08A, { emissive: 0xFFD060, emissiveIntensity: 1.2 }), 0.5, 0.06, s * 0.15, apeHead);
const apeLegs = [1, -1].map((s) => { const p = new THREE.Group(); p.position.set(0, 1.6, s * 0.42); ape.add(p); mk(new THREE.CylinderGeometry(0.34, 0.28, 1.65, 8), hairD, 0, -0.8, 0, p); return p; });
const apeArms = [1, -1].map((s) => { const p = new THREE.Group(); p.position.set(0.1, 3.5, s * 0.95); ape.add(p); mk(new THREE.CylinderGeometry(0.26, 0.2, 2.1, 8), hair, 0, -1.05, 0, p); return p; });
const PRINTS = []; { const pm = std(0x22160F, { roughness: 1 });
  for (let i = 0; i < 6; i++) { const g = new THREE.Group(); const u = i / 5; g.position.set(SX - 1 - 1.5 * u + (i % 2 ? 0.7 : -0.7), 0.2, 39 + 14 * u); g.rotation.y = 0.1; scene.add(g);
    const sole = mk(new THREE.CircleGeometry(0.5, 16), pm, 0, 0, 0, g); sole.rotation.x = -Math.PI / 2; sole.scale.set(1.1, 2.2, 1);
    for (let j = 0; j < 5; j++) { const toe = mk(new THREE.CircleGeometry(0.13, 10), pm, -0.32 + j * 0.16, 0, -1.02 + Math.abs(j - 2) * 0.06, g); toe.rotation.x = -Math.PI / 2; }
    PRINTS.push(g); } }
const puffM = []; const PUFFS = []; for (let i = 0; i < 6; i++) { const m = bas(0x9BE36A, { transparent: true, opacity: 0, depthWrite: false }); puffM.push(m); PUFFS.push(mk(new THREE.SphereGeometry(0.6, 10, 8), m, 0, -9, 0)); }

// ================= 5. living room with a console and a lit TV
const RX = 600, RZ = 80;
const room = new THREE.Group(); room.position.set(RX, 0, RZ); scene.add(room);
{ const woodTex = canvasTex(256, 256, (g, W, H) => { g.fillStyle = "#6E3E36"; g.fillRect(0, 0, W, H); for (let y = 0; y < H; y += 32) { g.fillStyle = y % 64 ? "#7E4A3E" : "#5E3430"; g.fillRect(0, y, W, 30); } }, true);
  woodTex.repeat.set(4, 4);
  mk(new THREE.BoxGeometry(18, 0.8, 16), std(0x3A2030), 0, -0.4, 0, room);
  mk(new THREE.PlaneGeometry(18, 16), std(0xffffff, { map: woodTex }), 0, 0.02, 0, room).rotation.x = -Math.PI / 2;
  const wallM = bas(0x0A0420);
  mk(new THREE.PlaneGeometry(18, 8), wallM, 0, 4, 7, room).rotation.y = Math.PI;
  mk(new THREE.PlaneGeometry(16, 8), wallM, -9, 4, 0, room).rotation.y = Math.PI / 2;
  mk(new THREE.PlaneGeometry(16, 8), wallM, 9, 4, 0, room).rotation.y = -Math.PI / 2;
  mk(new THREE.PlaneGeometry(18, 16), bas(0x050212), 0, 8, 0, room).rotation.x = Math.PI / 2;
  mk(new THREE.BoxGeometry(5.6, 3.3, 0.3), std(0x0E0818, { roughness: 0.3, metalness: 0.5 }), 0, 3.9, 6.75, room);
  mk(new THREE.BoxGeometry(7, 1.1, 1.2), std(0x2A1A4A), 0, 0.55, 6.3, room);
  mk(new THREE.BoxGeometry(1.7, 0.42, 1.0), std(0xF4F0FF, { roughness: 0.3 }), -2.2, 1.31, 6.2, room);
  const sofaM = std(0x8A2A6E, { roughness: 0.9 }), cushM = std(0xFF3D8B, { roughness: 0.9 });
  mk(new THREE.BoxGeometry(7.5, 0.9, 2.4), sofaM, 0, 0.45, -4.5, room); mk(new THREE.BoxGeometry(7.5, 1.7, 0.6), sofaM, 0, 1.3, -5.6, room);
  for (const s of [1, -1]) mk(new THREE.BoxGeometry(0.6, 1.3, 2.4), sofaM, s * 3.75, 0.65, -4.5, room);
  for (const x of [-2.4, 0, 2.4]) mk(new THREE.BoxGeometry(2.3, 0.3, 2.0), cushM, x, 1.05, -4.4, room);
  mk(new THREE.BoxGeometry(0.75, 0.16, 0.42), std(0x1B0B3A), 1.2, 1.28, -4.1, room);
  mk(new THREE.CircleGeometry(4.2, 32), std(0x6A3A2A, { roughness: 1 }), 0, 0.05, 1, room).rotation.x = -Math.PI / 2;
  const winTexR = canvasTex(128, 128, (g, W, H) => { const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#5B1A6E"); gr.addColorStop(0.7, "#FF7A6A"); gr.addColorStop(1, "#FFC36B");
    g.fillStyle = gr; g.fillRect(0, 0, W, H); g.fillStyle = "#2A0B3A"; g.fillRect(0, H * 0.82, W, H); g.fillRect(W * 0.2, H * 0.4, 5, H * 0.45);
    g.beginPath(); g.ellipse(W * 0.2, H * 0.4, 22, 6, 0.3, 0, 7); g.fill(); g.strokeStyle = "#2A1240"; g.lineWidth = 8; g.strokeRect(0, 0, W, H); g.fillRect(W / 2 - 3, 0, 6, H); });
  mk(new THREE.PlaneGeometry(3.4, 3), new THREE.MeshBasicMaterial({ map: winTexR, toneMapped: false }), -6, 4.6, 6.95, room).rotation.y = Math.PI;
  mk(new THREE.CylinderGeometry(0.06, 0.06, 4, 8), goldM, 6.4, 2, 5, room);
  mk(new THREE.ConeGeometry(0.8, 1, 16, 1, true), std(0xFFE0A0, { emissive: 0xFFC070, emissiveIntensity: 1.2, side: THREE.DoubleSide }), 6.4, 4.2, 5, room); }
const consLight = mk(new THREE.BoxGeometry(1.2, 0.06, 0.02), std(0xFF3D8B, { emissive: 0xFF3D8B, emissiveIntensity: 2 }), -2.2, 1.31, 5.69, room);
const SC = document.createElement("canvas"); SC.width = 384; SC.height = 216; const scg = SC.getContext("2d");
const scTex = new THREE.CanvasTexture(SC); scTex.encoding = THREE.sRGBEncoding; let scF = -1;
function drawScreen(t) { const g = scg, W = 384, H = 216, f = Math.floor(t * 30); if (f === scF) return; scF = f;
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#2A0B4A"); gr.addColorStop(1, "#FF3D8B"); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  g.fillStyle = "#FFC94A"; g.beginPath(); g.arc(W * 0.72, H * 0.55, 42, 0, 7); g.fill();
  g.fillStyle = "#3A1660"; for (let i = 0; i < 9; i++) { const x = ((i * 56 - f * 1.5) % (W + 60) + W + 60) % (W + 60) - 50; g.fillRect(x, H * 0.75 - 30 - (i * 37 % 50), 40, 90); }
  g.fillStyle = "#1B0B3A"; g.fillRect(0, H * 0.75, W, H * 0.25);
  g.fillStyle = "#FFC94A"; for (let i = 0; i < 10; i++) { const x = ((i * 48 - f * 5) % W + W) % W; g.fillRect(x, H * 0.75, 6, H * 0.25); }
  g.fillStyle = "#2EE6D6"; g.fillRect(74, H * 0.75 - 22 - 56 * Math.abs(Math.sin(t * 3.2)), 22, 22);
  for (let i = 0; i < 3; i++) { const x = ((180 + i * 130 - f * 5) % (W + 40) + W + 40) % (W + 40) - 20; g.fillStyle = "#FFE7A0"; g.beginPath(); g.arc(x, H * 0.5, 8, 0, 7); g.fill(); }
  g.fillStyle = "#fff"; g.font = "900 20px Montserrat"; g.textAlign = "left"; g.textBaseline = "top"; g.fillText("PUNTOS " + String((f * 7) % 100000).padStart(5, "0"), 12, 10);
  g.textAlign = "right"; g.fillText("NIVEL 3", W - 12, 10); scTex.needsUpdate = true; }
mk(new THREE.PlaneGeometry(5.1, 2.9), new THREE.MeshBasicMaterial({ map: scTex, toneMapped: false }), 0, 3.9, 6.58, room).rotation.y = Math.PI;
{ const tvL = new THREE.PointLight(0x9A7CFF, 1.3, 22); tvL.position.set(RX, 3.9, RZ + 4.5); scene.add(tvL); }

// ================= 6. house with a garage and the conspiracist inside
const HX = 820, HZ = -6;
const house = new THREE.Group(); house.position.set(HX, 0, HZ); scene.add(house);
{ const wallH = std(0xF2A7C3, { roughness: 0.8 }), wallG = std(0xF8D6E2, { roughness: 0.8 }), roofM = std(0x7A2A5E, { roughness: 0.7 });
  mk(new THREE.BoxGeometry(16, 6.5, 10), wallH, -4, 3.25, 0, house);
  const roof = mk(new THREE.ConeGeometry(10.5, 4, 4), roofM, -4, 8.5, 0, house); roof.rotation.y = Math.PI / 4; roof.scale.set(1.15, 1, 0.75);
  mk(new THREE.BoxGeometry(0.3, 4.8, 10), wallG, 11.85, 2.4, 0, house);
  mk(new THREE.BoxGeometry(8, 4.8, 0.3), std(0x5A3A5E), 8, 2.4, -4.85, house);
  mk(new THREE.BoxGeometry(8.6, 0.4, 10.6), roofM, 8, 5.0, 0, house);
  mk(new THREE.BoxGeometry(0.6, 4.8, 0.3), wallG, 4.3, 2.4, 4.9, house); mk(new THREE.BoxGeometry(0.6, 4.8, 0.3), wallG, 11.7, 2.4, 4.9, house);
  mk(new THREE.PlaneGeometry(8, 10), std(0x3A2E3E), 8, 0.03, 0, house).rotation.x = -Math.PI / 2;
  const winM = std(0xFFD08A, { emissive: 0xFFC070, emissiveIntensity: 0.8 });
  for (const x of [-9.5, -5.8]) mk(new THREE.BoxGeometry(2.2, 1.8, 0.1), winM, x, 3.6, 5.03, house);
  mk(new THREE.BoxGeometry(1.6, 3, 0.15), std(0xFF3D8B), -1.8, 1.5, 5.05, house);
  mk(new THREE.PlaneGeometry(8, 12), std(0x5A4A5E, { roughness: 0.9 }), 8, 0.05, 11, house).rotation.x = -Math.PI / 2;
  mk(new THREE.PlaneGeometry(18, 12), std(0x3E6B4A, { roughness: 1 }), -4, 0.04, 11, house).rotation.x = -Math.PI / 2;
  palm(HX - 16, HZ + 8, 1.4, 0.3); palm(HX + 17, HZ + 6, 1.25, -0.4);
  const corkTex = canvasTex(512, 260, (g, W, H) => { g.fillStyle = "#A9744A"; g.fillRect(0, 0, W, H); const r = seeded(9); const pts = [];
    for (let i = 0; i < 9; i++) { const x = 30 + r() * (W - 110), y = 20 + r() * (H - 90), wdt = 60 + r() * 30; g.fillStyle = i % 3 ? "#F4F0E6" : "#FFE07A"; g.fillRect(x, y, wdt, 50 + r() * 20);
      pts.push([x + wdt / 2, y + 6]); }
    g.strokeStyle = "#E0302F"; g.lineWidth = 4; g.beginPath(); pts.forEach(([x, y], i) => { const [a, b] = pts[(i * 4 + 3) % pts.length]; g.moveTo(x, y); g.lineTo(a, b); }); g.stroke();
    g.fillStyle = "#E0302F"; pts.forEach(([x, y]) => { g.beginPath(); g.arc(x, y, 7, 0, 7); g.fill(); });
    g.fillStyle = "#2A0B4A"; g.font = "900 90px Montserrat"; g.fillText("?", W * 0.78, H * 0.62); g.fillText("?", W * 0.12, H * 0.9); });
  mk(new THREE.PlaneGeometry(5.4, 2.8), std(0xffffff, { map: corkTex, emissive: 0xffffff, emissiveMap: corkTex, emissiveIntensity: 0.25 }), 8, 2.9, -4.68, house);
  const gl = new THREE.PointLight(0xFFB070, 1.4, 12); gl.position.set(HX + 8, 4.2, HZ + 1); scene.add(gl); }
const doorTex = canvasTex(256, 160, (g, W, H) => { g.fillStyle = "#EDE2F0"; g.fillRect(0, 0, W, H); g.fillStyle = "#C9B4D4"; for (let y = 18; y < H; y += 36) g.fillRect(0, y, W, 5); }, false);
const gdoor = mk(new THREE.BoxGeometry(7.2, 4.4, 0.2), std(0xffffff, { map: doorTex }), 8, 2.2, 5.0, house);
const conspi = person(0x7AC74F, 0x3A2A55, 0xD9A07A, 0x5A3A2A); conspi.position.set(HX + 8, 0, HZ - 1.5);
mk(new THREE.ConeGeometry(0.3, 0.75, 8), std(0xE6E6F2, { metalness: 1, roughness: 0.25 }), 0, 2.4, 0, conspi);

// ================= 7. night road in Kelly County: abandoned car, UFO, abduction
const NX = 1050;
{ const pm = std(0x173A2C, { roughness: 0.9, flatShading: true }), tm = std(0x3A2A22); const rp = seeded(88);
  for (let i = 0; i < 34; i++) { const x = NX - 40 + rp() * 85, z = 22 + rp() * 40; if (Math.abs(x - NX - 10) < 8 && z < 40) continue;
    const g = new THREE.Group(); g.position.set(x, 0, z); const s = 1 + rp() * 0.8; g.scale.setScalar(s); scene.add(g);
    mk(new THREE.CylinderGeometry(0.25, 0.32, 2, 6), tm, 0, 1, 0, g);
    for (let j = 0; j < 3; j++) mk(new THREE.ConeGeometry(2.4 - j * 0.6, 3, 7), pm, 0, 2.6 + j * 1.7, 0, g); } }
const car2 = makeCar(0xFFC94A);
const HBM = bas(0xFFF2B0, { transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
const HB = [0.65, -0.65].map((z) => { const c = mk(new THREE.ConeGeometry(1.3, 7, 16, 1, true), HBM, 2.31 + 3.5, 0.9, z, car2.g); c.rotation.z = Math.PI / 2; return c; });
const woman = person(0xFF3D8B, 0x2A1A4A, 0xC98B6B, 0x3A1A0A, true);
const player2 = person(0x2EE6D6, 0x2A1A4A, 0xC98B6B, 0x2A1A1A);
const ufo = new THREE.Group(); scene.add(ufo);
mk(new THREE.SphereGeometry(1, 32, 16), std(0xB8A8D8, { metalness: 0.8, roughness: 0.25 }), 0, 0, 0, ufo).scale.set(5, 1.1, 5);
mk(new THREE.SphereGeometry(1.7, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), std(0x2EE6D6, { emissive: 0x2EE6D6, emissiveIntensity: 0.7, transparent: true, opacity: 0.9 }), 0, 0.6, 0, ufo);
mk(new THREE.CircleGeometry(2.2, 24), bas(0xFFE7A0), 0, -1.12, 0, ufo).rotation.x = Math.PI / 2;
const rims = new THREE.Group(); ufo.add(rims);
for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; mk(new THREE.SphereGeometry(0.3, 8, 6), i % 2 ? bas(0xFF3D8B) : bas(0xFFC94A), Math.cos(a) * 4.7, 0, Math.sin(a) * 4.7, rims); }
const ufoBeamM = bas(0xFFF2A8, { transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
const ufoBeam = mk(new THREE.CylinderGeometry(1.1, 3.4, 1, 24, 1, true), ufoBeamM, 0, 0, 0);
const moon = mk(new THREE.SphereGeometry(60, 24, 16), bas(0xFFF4D6, { fog: false }), 1000, 800, 1800); moon.visible = false;
const stars = (() => { const sp = [], r = seeded(77); for (let i = 0; i < 600; i++) { const th = r() * Math.PI * 2, ph = 0.05 + r() * 1.3, rr = 2300;
  sp.push(rr * Math.cos(ph) * Math.cos(th), rr * Math.sin(ph), rr * Math.cos(ph) * Math.sin(th)); }
  const gg = new THREE.BufferGeometry(); gg.setAttribute("position", new THREE.Float32BufferAttribute(sp, 3));
  const p = new THREE.Points(gg, new THREE.PointsMaterial({ color: 0xffffff, size: 2.5, sizeAttenuation: false, fog: false })); p.visible = false; scene.add(p); return p; })();
"""

# ------------------------------------------------------------------ camera (absolute keys; a CUT is two keys 0.05 s apart)
SX, NX, HX, HZ = -260, 1050, 820, -6
P = {
    "dogA": ((15, 5.2, 63), (2, 4.2, 81)), "dogA2": ((14, 4.8, 64), (2, 3.8, 81)),
    "dogB": ((9, 3.8, 69), (1.5, 3.0, 80.5)), "dogB2": ((8.5, 3.8, 69.5), (1.5, 3.0, 80.5)),
    "dogW": ((14, 7, 56), (0, 3.4, 84)), "dogEnd": ((16, 5.4, 62), (2, 4.4, 81)), "dogEnd2": ((15, 5.2, 63), (2, 4.2, 81)), "dogW2": ((16, 7.4, 55), (0, 3.4, 84)),
    "towerUp": ((250, 15, -30), (220, 25, 10)), "towerUp2": ((248, 15.5, -28), (220, 25, 10)),
    "towerTop": ((238, 37, -6), (220.3, 25, 12.2)), "towerHit": ((238, 8, -9), (221, 3.4, 12)), "towerHit2": ((240, 7, -9), (228, 3, 12)),
    "paperA": ((400, 8.6, 66), (400, 8.6, 8)), "paperB": ((400, 8.4, 64.5), (400, 8.4, 8)), "paperB2": ((400, 8.4, 64), (400, 8.4, 8)),
    "swampA": ((SX - 1, 5.5, 31), (SX, 0, 50)), "swampA2": ((SX - 1.5, 5.2, 33), (SX, 0.3, 51)),
    "swampB": ((SX - 3, 3.8, 44), (SX - 1, 5.0, 64)), "swampB2": ((SX - 2, 3.8, 45), (SX + 1, 5.0, 64)),
    "roomA": ((603, 4.4, 70), (600, 3.0, 86)), "roomA2": ((601.5, 4.0, 71.5), (600, 3.0, 86)), "roomB": ((600, 3.6, 72), (600, 3.4, 86)),
    "houseA": ((840, 6.5, 38), (820, 4.5, -6)), "houseB": ((834, 4.5, 26), (822, 4, -6)),
    "garage": ((828, 3.2, 12), (828, 3.7, -8)), "garage2": ((828, 3.0, 10.5), (828, 3.7, -8)),
    "nightA": ((1036, 5, -8), (1048, 2.5, 18)), "nightA2": ((1035, 5.4, -10), (1048, 2.7, 18)),
    "nightB": ((1044, 6, -14), (1056, 10, 28)), "nightB2": ((1045, 6, -13), (1056, 10, 27)), "nightC": ((1046, 5.5, -12), (1057, 10, 28)),
}
KEYS = []
def key(t, name): KEYS.append((round(t, 3), P[name]))
def cut(t, name): KEYS.append((round(t - 0.05, 3), KEYS[-1][1])); key(t, name)
key(0, "dogA"); key(k["perro"] - 0.3, "dogA2"); key(k["perro"] + 0.6, "dogB"); key(k["l1"] - 0.1, "dogB2"); key(k["l1"] + 0.9, "dogW"); key(k["l2"] - 0.25, "dogW2")
cut(k["l2"] - 0.1, "towerUp"); key(k["tira"] - 0.15, "towerUp2")
cut(k["tira"] - 0.05, "towerTop"); key(k["tira"] + 0.45, "towerTop"); key(k["estampa"], "towerHit"); key(k["l4"] - 0.2, "towerHit2")
cut(k["l4"] - 0.1, "paperA"); key(k["anuncia"], "paperA"); key(k["furries"] + 0.3, "paperB"); key(k["l5"] - 0.2, "paperB2")
cut(k["l5"] - 0.1, "swampA"); key(k["aqui"] - 0.1, "swampA2"); key(k["simio"] + 0.2, "swampB"); key(k["l6"] - 0.2, "swampB2")
cut(k["l6"] - 0.1, "roomA"); key(k["consola"], "roomA2"); key(k["l7"] - 0.2, "roomB")
cut(k["l7"] - 0.1, "houseA"); key(k["l8"] - 0.1, "houseB"); key(k["garaje"] + 0.9, "garage"); key(k["l9"] - 0.2, "garage2")
cut(k["l9"] - 0.1, "nightA"); key(k["condado"] - 0.2, "nightA2"); key(k["condado"] + 0.8, "nightB"); key(k["abducido"], "nightB2"); key(k["l11"] + 0.8, "nightC"); key(k["recuerda"] - 0.65, "nightC")
cut(k["recuerda"] - 0.55, "dogEnd"); key(R.total, "dogEnd2")
assert all(b[0] > a[0] for a, b in zip(KEYS, KEYS[1:])), KEYS
keys_js = "const keys = [\n" + ",\n".join(f"  [{t}, {list(e)}, {list(l)}]" for t, (e, l) in KEYS) + "\n];\n"

render_js = r"""
  const pinL = (id, x, y, z, o) => { pin(id, x, y, z, o); const el = tags[id]; el.style.top = Math.max(parseFloat(el.style.top), 900).toFixed(1) + "px";
    const hw = el.offsetWidth / 2 + 24; el.style.left = Math.min(Math.max(parseFloat(el.style.left), hw), 1080 - hw).toFixed(1) + "px"; };
  // ---- night (Kelly County) is a hard cut in and out
  const nf = (t >= K.l9 - 0.1 && t < K.recuerda - 0.55) ? 1 : 0;
  sky.material.color.setRGB(1 - 0.86 * nf, 1 - 0.86 * nf, 1 - 0.72 * nf);
  sun.visible = glint.visible = !nf && !(t >= K.l7 - 0.1 && t < K.l9 - 0.1); moon.visible = stars.visible = !!nf;
  sunL.intensity = 1.4 * (1 - 0.88 * nf); fill.intensity = 0.55 + 0.25 * nf; fill.color.setHex(nf ? 0x6A7CFF : 0x9a8cff);
  HEMI.intensity = 0.9 * (1 - 0.55 * nf); scene.fog.color.setHex(nf ? 0x0A0A24 : 0x8a3a7a);
  renderer.toneMappingExposure = 1.05 - 0.12 * nf;
  { const dogS = t < K.l2 - 0.1 || t >= K.recuerda - 0.55; sea.material.metalness = dogS ? 0.05 : 0.35; sea.material.roughness = dogS ? 0.95 : 0.55;
    if (dogS) fill.intensity = 0.2; }
  document.getElementById("night").style.opacity = (0.6 * nf).toFixed(2);
  // ---- 1. dog on the jet ski
  const endS = t >= K.recuerda - 0.55, ja = 1.0, jb = 5.4;
  const ju = endS ? 1 : clamp01(t / 4.4), jx = -1.5 + 2 * eo(ju), spd = endS ? 0 : 0.35 * Math.pow(1 - ju, 2);
  jet.position.set(jx, -0.42 + 0.1 * Math.sin(t * 3.1), DOGZ); jet.rotation.set(0.04 * Math.sin(t * 1.7), 0, 0.04 * Math.sin(t * 2.3) + 0.1 * spd);
  tail.rotation.x = 0.7 * Math.sin(t * 13);
  wake.position.set(jx - 12, -0.5, DOGZ); wakeM.opacity = 0.6 * spd;
  SPRAY.forEach((s, i) => { const ph = (t * 2.2 + i / SPRAY.length) % 1; s.position.set(jx - 3 - ph * 4, -0.4 + 3 * ph * (1 - ph), DOGZ + (i % 2 ? 1 : -1) * (0.8 + ph * 1.5));
    s.scale.setScalar(Math.max(0.001, spd * (1 - ph))); });
  const wave = !endS && t < jb + 0.3;
  swimmer.position.y = -1.9 + 0.08 * Math.sin(t * 2); ring.position.y = -0.45 + 0.08 * Math.sin(t * 2);
  swimmer.userData.arms.forEach((a, i) => { a.rotation.z = (i ? -1 : 1) * (wave ? 2.5 + 0.35 * Math.sin(t * 9 + i) : 0.3); });
  pinL("tg-perro", jx + 1, 7.2, DOGZ, win(t, K.perro - 0.1, K.l1 - 0.05));
  // ---- 2. tower, egg, car
  beaconM.emissiveIntensity = Math.floor(t * 1.5) % 2 ? 0.3 : 2.5;
  const t0e = K.tira + 0.3, tHit = K.estampa, eY0 = TH + 0.3, gE = 2 * (eY0 - 3.35) / Math.pow(tHit - t0e, 2), ex = TX + 0.35, ez = TZ + 8.2;
  egg.visible = t < tHit;
  if (t < t0e) { egg.position.set(ex, eY0, ez); egg.rotation.z = t > K.tira - 0.1 ? 0.3 * Math.sin((t - K.tira) * 30) : 0; }
  else if (t < tHit) { const d = t - t0e; egg.position.set(ex, eY0 - 0.5 * gE * d * d, ez); egg.rotation.z = d * 8; }
  const cd = t - tHit, c1x = ex + 0.56 + (cd < 0 ? 9 * cd : (cd < 2.05 ? 9 * cd - 2.2 * cd * cd : 9.2));
  car1.g.position.set(c1x, 0, ZR); car1.g.visible = t > K.l3 - 0.4 && t < K.l4; car1.wheels.forEach((wh) => { wh.rotation.y = -c1x / 0.64; });
  { const s = eo((t - tHit) / 0.12); splat.visible = t > tHit; splat.scale.setScalar(Math.max(0.001, s)); }
  DROPS.forEach((d) => { const dt = t - tHit; d.m.visible = dt > 0 && dt < 0.8;
    if (d.m.visible) d.m.position.set(ex + d.v[0] * dt, 3.4 + d.v[1] * dt - 9 * dt * dt, ez + d.v[2] * dt); });
  pinL("tg-nido", TX, TH + 1.5, TZ + 8.2, win(t, K.torre - 0.2, K.tira - 0.08));
  // ---- 3. newspaper spins in
  { const pe = eo((t - (K.periodico - 0.6)) / 0.9); paper.visible = t > K.l4 - 0.2 && t < K.l5;
    paper.rotation.set(0, 0.04 * Math.sin(t * 1.3), (1 - pe) * Math.PI * 4); paper.scale.setScalar(0.02 + 0.98 * pe);
    const hl = Math.round(clamp01((t - K.libre + 0.15) / 0.6) * 40) / 40; if (hl !== npHL) { npHL = hl; drawPaper(hl); npTex.needsUpdate = true; } }
  // ---- 4. swamp: footprints, then the skunk ape walks out
  PRINTS.forEach((p, i) => { const u = eo((t - (K.bigfoot - 0.1 + i * 0.16)) / 0.18); p.scale.setScalar(Math.max(0.001, u)); });
  { const au = clamp01((t - K.bigfoot) / (K.l6 - K.bigfoot)), ax = SX - 8 + 13 * au, ph = (t - K.bigfoot) * 5.5;
    ape.visible = t > K.bigfoot - 0.1 && t < K.l6; ape.position.set(ax, 0.08 * Math.abs(Math.sin(ph)), 63);
    apeLegs.forEach((l, i) => { l.rotation.z = (i ? -1 : 1) * 0.45 * Math.sin(ph); }); apeArms.forEach((a, i) => { a.rotation.z = (i ? 1 : -1) * 0.35 * Math.sin(ph); });
    apeHead.rotation.y = 0.9 * win(t, K.simio, K.l6, 0.3);
    PUFFS.forEach((p, i) => { const q = (t * 0.7 + i / 6) % 1; p.position.set(ax - 0.6 + Math.sin(i * 2.1) * 0.8, 2.6 + q * 3.2, 63 + Math.cos(i * 1.7) * 0.8);
      p.scale.setScalar(0.5 + q * 1.4); puffM[i].opacity = ape.visible ? 0.32 * (1 - q) : 0; });
    pinL("tg-ape", ax, 6.6, 63, win(t, K.simio - 0.1, K.l6 - 0.1)); }
  document.getElementById("swamp").style.opacity = (t > K.l5 - 0.1 && t < K.l6 - 0.1) ? "1" : "0";
  // ---- 5. living room
  if (t > K.l6 - 0.3 && t < K.l7 + 0.1) drawScreen(t);
  consLight.material.emissiveIntensity = 1.2 + 0.8 * Math.sin(t * 4);
  pinL("tg-juegos", RX - 1, 0.4, RZ + 5.5, win(t, K.casa6, K.l7 - 0.1));
  // ---- 6. garage door rolls up; the conspiracist gestures at his board
  { const gu = eo((t - K.garaje + 0.15) / 0.9), gh = 4.4 * (1 - 0.92 * gu); gdoor.scale.y = gh / 4.4; gdoor.position.y = 4.6 - gh / 2;
    conspi.userData.arms[0].rotation.z = 1.2 + 0.25 * Math.sin(t * 5); conspi.userData.arms[1].rotation.z = -0.3 - 0.15 * Math.sin(t * 3); conspi.rotation.y = 0.25 * Math.sin(t * 1.4);
  }
  // ---- 7. night: blinking car, UFO, the woman, then you
  const night = !!nf, cu = eo((t - (K.coche10 - 0.45)) / 1.0);
  car2.g.visible = night; woman.visible = night; ufo.visible = night && t > K.condado - 0.2;
  car2.g.position.set(NX - 4 + 10 * cu, 0, ZR + 3 + 9 * cu); car2.g.rotation.y = -0.8 * Math.sin(Math.PI * cu); car2.wheels.forEach((wh) => { wh.rotation.y = -cu * 20; });
  { const bl = cu > 0 ? 1 : (Math.floor(t * 3) % 2 === 0 ? 1 : 0); car2.headM.emissiveIntensity = 0.2 + 2.4 * bl; HBM.opacity = 0.3 * bl; }
  const A = 4.5 * eo((K.ovni - K.salva + 0.3) / 1.6);
  let wy = 0; if (t > K.salva - 0.3 && t < K.ovni) wy = 4.5 * eo((t - K.salva + 0.3) / 1.6); else if (t >= K.ovni) wy = A * (1 - eo((t - K.ovni) / 0.6));
  woman.position.set(NX + 12, wy, 34); woman.rotation.y = wy > 0 ? t * 1.5 : 0;
  woman.userData.arms.forEach((a, i) => { a.rotation.z = (i ? -1 : 1) * (wy > 0.2 ? 2.3 + 0.3 * Math.sin(t * 8) : 0.3); });
  const PX = NX + 8.5, PZ = 27; const pu = eo((t - K.abducido) / 1.3);
  player2.visible = night && t > K.coche10 + 0.55 && t < K.l11 + 0.2; player2.position.set(PX, 9.5 * pu, PZ); player2.rotation.y = pu * 6; player2.scale.setScalar(1.6 * (1 - 0.5 * pu));
  player2.userData.arms.forEach((a, i) => { a.rotation.z = (i ? -1 : 1) * (pu > 0.05 ? 2.4 : 0.3); });
  { const uIn = eo((t - (K.condado - 0.1)) / 1.2), toP = eo((t - (K.coche10 + 0.1)) / 0.8), aw = clamp01((t - (K.l11 - 0.1)) / 1.3);
    const ux = NX + 12 + (PX - NX - 12) * toP + 45 * (1 - uIn) - 90 * aw * aw, uz = 34 + (PZ - 34) * toP, uy = 15 + 0.4 * Math.sin(t * 2) + 4 * aw;
    ufo.position.set(ux, uy, uz); ufo.rotation.z = 0.06 * Math.sin(t * 1.6); rims.rotation.y = t * 2;
    const on = (t > K.salva - 0.3 && t < K.ovni) || (t > K.abducido - 0.25 && t < K.l11 - 0.1);
    ufoBeam.visible = night && on; ufoBeamM.opacity = 0.32 + 0.06 * Math.sin(t * 23);
    ufoBeam.position.set(ux, (uy - 1) / 2, uz); ufoBeam.scale.set(1, Math.max(0.01, uy - 1), 1); }
  pinL("tg-mujer", NX + 12, wy + 4.4, 34, win(t, K.salva + 0.45, K.traele - 0.1));
  pinL("tg-coche", car2.g.position.x, 4.4, car2.g.position.z, win(t, K.traele, K.abducido - 0.2));
"""

def show(sel, t, end, kind="pop"):
    a = (f'tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {t:.3f});' if kind == "pop" else
         f'tl.fromTo("{sel}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {t:.3f});')
    return a + f'\ntl.to("{sel}", {{ opacity: 0, duration: 0.18 }}, {end:.3f});'
def stamp(sel, t, end, rot=-6):
    return (f'tl.fromTo("{sel}", {{ opacity: 0, scale: 1.8, rotation: {rot} }}, {{ opacity: 1, scale: 1, rotation: {rot}, duration: 0.18, ease: "power4.out" }}, {t:.3f});'
            f'\ntl.to("{sel}", {{ opacity: 0, duration: 0.2 }}, {end:.3f});')

ov = [
    f'tl.fromTo("#bg-title", {{ scale: 1.0 }}, {{ scale: 1.04, duration: {k["perro"] - 0.3:.3f}, ease: "none" }}, 0);',
    f'tl.to("#bg-title", {{ opacity: 0, y: -30, duration: 0.22, ease: "power2.in" }}, {k["perro"] - 0.3:.3f});',
    show("#bg-6", k["primero"] - 0.1, k["l2"] - 0.15, "up"),
    stamp("#bg-plaf", k["estampa"] - 0.02, k["l4"] - 0.2, -8),
    f'tl.fromTo("#polaroid", {{ opacity: 0, y: 90, rotation: 10, scale: 0.8 }}, {{ opacity: 1, y: 0, rotation: -5, scale: 1, duration: 0.45, ease: "back.out(1.5)" }}, {k["foto"] - 0.15:.3f});',
    f'tl.to("#polaroid", {{ opacity: 0, y: 60, duration: 0.25, ease: "power2.in" }}, {k["l8"] - 0.3:.3f});',
    show("#bg-otro", k["otro"] - 0.1, k["l8"] - 0.2, "up"),
    f'tl.fromTo("#polaroid .yr", {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {k["anio"] - 0.05:.3f});',
    show("#h9", k["solo9"] - 0.1, k["l10"] - 0.1),
    show("#bg-conspi", k["convencido"] - 0.15, k["l9"] - 0.2, "up"),
    f'tl.fromTo("#h9b", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {k["dos9"] - 0.1:.3f});',
    show("#bg-kelly", k["condado"] - 0.15, k["salva"] + 0.35, "up"),
    stamp("#bg-abd", k["abducido"] - 0.05, k["l11"] - 0.15),
    f'tl.fromTo("#bg-cta", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {k["l11"]:.3f});',
    f'tl.to("#bg-cta", {{ opacity: 0, duration: 0.15 }}, {k["recuerda"] - 0.72:.3f});',
    f'tl.fromTo("#bg-title", {{ opacity: 0, y: 0, scale: 1.1 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "power3.out", immediateRender: false }}, {k["recuerda"] - 0.45:.3f});',
]
# glitch flicker when he says "videojuego"
for i, (o, x) in enumerate([(1, 0), (0, 0), (1, -14), (0, 0), (1, 10), (0, 0)]):
    ov.append(f'tl.set("#glitch", {{ opacity: {o}, x: {x} }}, {k["videojuego"] + i * 0.05:.3f});')
# the counter: 1/7 … 7/7
CNT = [(k["l1"], "1/7"), (k["l2"] - 0.1, "2/7"), (k["l4"] - 0.1, "3/7"), (k["l5"] - 0.1, "4/7"), (k["l6"] - 0.1, "5/7"), (k["l7"] - 0.1, "6/7"), (k["l9"] - 0.1, "7/7")]
ov.append(f'tl.fromTo("#cnt", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {k["l1"]:.3f});')
for t, txt in CNT[1:]:
    ov.append(f'tl.fromTo("#cnt", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, {t:.3f});')
ov.append(f'tl.to("#cnt", {{ opacity: 0, duration: 0.2 }}, {k["l11"] - 0.1:.3f});')
overlay_js = "\n".join(ov)
render_js = ("  const CNT = " + str([[round(t, 3), c] for t, c in CNT]) + ";\n"
             "  { let c = CNT[0][1]; for (const [a, b] of CNT) if (t >= a) c = b; const el = document.getElementById(\"cnt\"); if (el.textContent !== c) el.textContent = c; }\n"
             + render_js)

# ------------------------------------------------------------------ sound
R.sfx(0.05, "subida-1.wav", 0.35)
R.sfx(2.4, "lancha.wav", 0.35)
R.sfx(k["perro"], "ladrido.wav", 0.5)
R.sfx(k["perro"] + 0.5, "ladrido.wav", 0.4)
R.sfx(k["moto"] - 0.2, "chapoteo.wav", 0.4)
R.sfx(k["l1"] + 0.1, "pop-1.wav", 0.4)
R.sfx(k["siete"] - 0.15, "pop-1.wav", 0.45)
for key_, f in (("l2", "barrido-1.wav"), ("l4", "barrido-2.wav"), ("l5", "barrido-1.wav"), ("l6", "barrido-2.wav"), ("l7", "barrido-1.wav")):
    R.sfx(k[key_] - 0.12, f, 0.4)
R.sfx(k["nido"] - 0.1, "pop-2.wav", 0.4)
R.sfx(k["tira"] - 0.1, "tic.wav", 0.5)
R.sfx(k["tira"] + 0.3, "barrido-3.wav", 0.3)
R.sfx(k["estampa"] - 0.03, "cascaron.wav", 0.6)
R.sfx(k["estampa"] + 0.3, "claxon.wav", 0.35)
R.sfx(k["periodico"] - 0.6, "pagina.wav", 0.5)
R.sfx(k["libre"] - 0.15, "pop-3.wav", 0.4)
for i in range(6):
    R.sfx(k["bigfoot"] - 0.1 + i * 0.16, "caja-1.wav" if i % 2 else "caja-2.wav", 0.28)
R.sfx(k["aqui"], "rana.wav", 0.3)
R.sfx(k["simio"] - 0.1, "impacto.wav", 0.3)
R.sfx(k["consola"] - 0.1, "bip.wav", 0.4)
R.sfx(k["videojuegos"] - 0.1, "monedas.wav", 0.4)
R.sfx(k["foto"] - 0.15, "captura.wav", 0.5)
R.sfx(k["anio"] - 0.05, "sello.wav", 0.55)
R.sfx(k["garaje"] - 0.15, "barrido-largo.wav", 0.35)
R.sfx(k["videojuego"], "glitch.wav", 0.45)
R.sfx(k["l9"] - 0.12, "barrido-3.wav", 0.35)
R.sfx(k["l9"] - 0.1, "grillos.wav", 0.4)
R.sfx(k["solo9"] - 0.1, "tic.wav", 0.5)
R.sfx(k["dos9"] - 0.1, "tic-2.wav", 0.5)
R.sfx(k["condado"] - 0.1, "pop-2.wav", 0.4)
for t in (k["condado"] + 0.2, k["salva"] - 0.3, k["salva"] + 0.7):
    R.sfx(t, "ovni.wav", 0.3)
R.sfx(k["ovni"], "pop-4.wav", 0.4)
R.sfx(k["coche10"] - 0.45, "lancha.wav", 0.25)
R.sfx(k["abducido"] - 0.25, "ovni.wav", 0.35)
R.sfx(k["abducido"] - 0.05, "sello.wav", 0.6)
R.sfx(k["abducido"] + 0.75, "ovni.wav", 0.3)
R.sfx(k["l11"], "pop-1.wav", 0.5)
R.sfx(k["l11"] + 0.1, "subida-2.wav", 0.3)
R.sfx(k["recuerda"] - 0.6, "barrido-largo.wav", 0.35)
R.sfx(k["recuerda"] - 0.3, "subida-1.wav", 0.3)
R.sfx(max(57.05, k["recuerda"] + 0.2), "ladrido.wav", 0.3)

CAPS = [
    "En GTA 6, si te quedas tirado en el mar, puede rescatarte un perro con gafas... en moto de agua.",
    "Y ese es solo el primero de siete.",
    "Dos: en lo alto de una torre hay un nido.",
    "Tira un huevo, y se estampa contra un coche que pasa por debajo.",
    "Tres: el periódico del juego lo anuncia: Leonida, libre de furries.",
    "Cuatro: Bigfoot ha vuelto. Aquí es el simio mofeta, y vive en los pantanos.",
    "Cinco: en casa de Jason hay una consola con videojuegos enteros.",
    "Seis: hay una casa que ya salió en una foto escondida en otro GTA, en 2021.",
    "Y en su garaje vive alguien convencido de que está dentro de un videojuego.",
    "Y el último: ve solo, pasadas las 2 de la mañana, a una carretera del condado de Kelly.",
    "Salva a la mujer que se lleva un ovni, tráele su coche... y el abducido eres tú.",
    "¿Cuál vas a probar primero? Y si te da miedo el mar, recuerda que...",
]
HL = {"perro", "gafas", "agua", "siete", "dos", "torre", "nido", "huevo", "estampa", "tres", "periódico", "furries", "cuatro", "bigfoot",
      "simio", "mofeta", "cinco", "consola", "videojuegos", "seis", "foto", "2021", "garaje", "videojuego", "último", "2", "kelly",
      "ovni", "coche", "abducido", "tú", "primero?"}

# keep the voice >= 6 dB above every effect: cap each SFX gain from its measured loudness (voice is ~-19 LUFS)
import re as _re, subprocess as _sp, math as _m
_LU = {}
def _lufs(name):
    if name not in _LU:
        out = _sp.run(["ffmpeg", "-nostats", "-i", str(R.out / "assets" / "audio" / name), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        ms = [float(x) for x in _re.findall(r"M:\s*(-?[0-9.]+)", out)]
        _LU[name] = max(ms) if ms else -20.0
    return _LU[name]
def _cap(name, vol):
    if name == "grillos.wav": return vol
    soft = 0.15 if name in ("ovni.wav", "barrido-largo.wav", "subida-1.wav", "barrido-1.wav", "tic.wav", "pop-2.wav") else 0.2
    return round(min(vol, soft, 10 ** ((-27.0 - _lufs(name)) / 20)), 3)
R.sfx_list = [(t, n, _cap(n, v)) for t, n, v in R.sfx_list]

R.write(R.mundo(body, sets_js, keys_js, render_js, overlay_js, K), R.subs(CAPS, HL, sync="words"))
