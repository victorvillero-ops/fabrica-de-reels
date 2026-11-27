"""Reel 05 — Leonida in real life. A fictional Florida-like island rises from the sea in front of the sunset city;
the camera tours its regions, each with its own props and its real-world counterpart."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "serie"))
from serie import Reel

R = Reel(Path(__file__).parent)
w = R.wt
K = {
    "existe": w(0, "existe"), "real": w(0, "real"),
    "l1": R.ls(1), "florida": w(1, "florida"),
    "l2": R.ls(2), "miami": w(2, "miami"),
    "l3": R.ls(3), "y2002": w(3, "dos", ["2002"]),
    "l4": R.ls(4), "cayos4": w(4, "cayos", nth=1),
    "l5": R.ls(5), "largo": w(5, "largo"),
    "l6": R.ls(6), "everglades": w(6, "everglades", ["everglade", "evergl"]),
    "l7": R.ls(7), "humedal": w(7, "humedal"),
    "l8": R.ls(8), "panama": w(8, "panama"),
    "l9": R.ls(9), "okeechobee": w(9, "okee", ["oke", "oque", "oki"]),
    "l10": R.ls(10), "invento": w(10, "invento"),
    "l11": R.ls(11), "ciento": w(11, "ciento", ["105"]),
    "l12": R.ls(12), "grande12": w(12, "grande"),
    "l13": R.ls(13), "end": R.total,
}

body = """
<div class="big" id="bg-no" style="top:880px;font-size:130px"><span class="stamp">NO EXISTE</span></div>
<div class="big" id="bg-real" style="top:1040px;font-size:84px"><span class="plate">PERO ES REAL</span></div>
<div class="tag" id="tg-leo" style="font-size:110px"><span class="grad">LEONIDA</span><small id="tg-leo-s">el estado de GTA 6</small></div>
<div class="tag" id="tg-vc" style="font-size:80px"><span class="grad">VICE CITY</span><small>= Miami</small></div>
<div class="tag" id="tg-keys" style="font-size:66px"><span class="grad">LEONIDA KEYS</span><small>= Cayos de Florida</small></div>
<div class="tag" id="tg-lento" style="font-size:62px"><span class="grad">KEY LENTO</span><small>≈ Key Largo</small></div>
<div class="tag" id="tg-gr" style="font-size:72px"><span class="grad">GRASSRIVERS</span><small>= Everglades</small></div>
<div class="tag" id="tg-pg" style="font-size:66px"><span class="grad">PORT GELLHORN</span><small>≈ Panama City</small></div>
<div class="tag" id="tg-am" style="font-size:76px"><span class="grad">AMBROSIA</span><small>≈ Lago Okeechobee</small></div>
<div class="tag" id="tg-ka" style="font-size:72px"><span class="grad">MONTE KALAGA</span><small>inventado</small></div>
<div class="big" id="bg-2002" style="top:1010px;font-size:70px"><span class="plate">GTA VICE CITY · 2002</span></div>
<div class="big" id="bg-hum" style="top:1000px;font-size:64px"><span class="grad">MAYOR HUMEDAL</span><br><span class="plate" style="font-size:44px">SUBTROPICAL DE EE. UU.</span></div>
<div class="big" id="bg-105" style="top:1040px;font-size:70px"><span class="plate">FLORIDA REAL: 105 m</span></div>
<div class="big" id="bg-ka" style="top:1020px;font-size:74px"><span class="stamp">NO EXISTE EN FLORIDA</span></div>
<div class="big" id="bg-big" style="top:880px;font-size:88px"><span class="grad">EL MAPA<br>MÁS GRANDE</span><br><span class="plate" style="font-size:52px">DE ROCKSTAR</span></div>
<div class="big" id="bg-cta" style="top:860px;font-size:96px">¿CUÁL<br><span class="grad">VISITARÍAS</span><br>PRIMERO?</div>
"""

sets_js = r"""
const OX = 0, OZ = 380, Z = 0;                         // island centre (world)
const isl = new THREE.Group(); isl.position.set(OX, 0, OZ); scene.add(isl);
const P = [[-260, -200], [60, -200], [95, -150], [110, -60], [125, 30], [130, 120], [118, 190], [95, 240], [70, 262], [50, 250], [35, 200],
           [10, 130], [-10, 60], [-30, 0], [-60, -60], [-120, -120], [-200, -140], [-260, -150]];
const shape = new THREE.Shape(P.map(([x, z]) => new THREE.Vector2(x, -z)));
const landM = new THREE.MeshStandardMaterial({ color: 0x4E9A6E, roughness: 0.85 });
const sideM = new THREE.MeshStandardMaterial({ color: 0xD8A57A, roughness: 0.9 });
const land3 = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: 6, bevelEnabled: true, bevelThickness: 1.5, bevelSize: 2.5, bevelSegments: 2 }), [landM, sideM]);
land3.rotation.x = -Math.PI / 2; land3.position.y = -4; isl.add(land3);
const R2 = seeded(77);
function box(w, h, d, color, x, z, y0, opts) { const m = new THREE.Mesh(bGeo, new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.6 }, opts || {})));
  m.scale.set(w, h, d); m.position.set(x, (y0 || 0) + 2, z); isl.add(m); return m; }
// Vice City (south-east coast): lit towers
const vc = new THREE.Group(); isl.add(vc);
for (let i = 0; i < 26; i++) { const x = 80 + R2() * 40, z = 140 + R2() * 70, h = 6 + Math.pow(R2(), 1.4) * 26, s = 4 + R2() * 4;
  const tex = winTex.clone(); tex.needsUpdate = true; tex.repeat.set(1, Math.max(1, h / 6));
  const m = new THREE.Mesh(bGeo, new THREE.MeshStandardMaterial({ color: [0xB88AC8, 0x8E6BB8, 0xD6A2B8][i % 3], emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.9, map: tex, roughness: 0.5 }));
  m.scale.set(s, h, s); m.position.set(x, 2, z); vc.add(m); }
// Leonida Keys: a chain of islets curving south-west from the tip
const keys3 = new THREE.Group(); isl.add(keys3); const KEYS = [];
for (let i = 0; i < 10; i++) { const a = i / 9, x = 62 - a * 140, z = 272 + Math.sin(a * Math.PI) * 30 + a * 40, r = i === 2 ? 11 : 4 + R2() * 4;
  const k = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 1.15, 4, 18), [landM, sideM, landM].length ? landM : landM); k.scale.set(1.6, 1, 1);
  k.position.set(x, -2, z); keys3.add(k); KEYS.push([x, z]); }
const LENTO = KEYS[2];
// Grassrivers (south interior): swamp, reeds, an airboat
const swamp = new THREE.Mesh(new THREE.CylinderGeometry(34, 34, 1, 32), new THREE.MeshStandardMaterial({ color: 0x2F6B57, roughness: 0.3, metalness: 0.2 }));
swamp.scale.set(1, 1, 1.5); swamp.position.set(45, 2.2, 175); isl.add(swamp);
const reedM = new THREE.MeshStandardMaterial({ color: 0x9BBF5A, roughness: 0.9 });
for (let i = 0; i < 70; i++) { const a = R2() * 6.28, r = 8 + R2() * 30, rd = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.4, 4 + R2() * 4, 4), reedM);
  rd.position.set(45 + Math.cos(a) * r, 4.5, 175 + Math.sin(a) * r * 1.4); rd.rotation.z = (R2() - 0.5) * 0.4; isl.add(rd); }
const boat = new THREE.Group(); boat.position.set(40, 3.2, 170); isl.add(boat);
const hull = new THREE.Mesh(new THREE.BoxGeometry(8, 1.4, 4), new THREE.MeshStandardMaterial({ color: 0xE8E8F0, roughness: 0.4 })); boat.add(hull);
const fan = new THREE.Mesh(new THREE.TorusGeometry(2.2, 0.35, 8, 20), new THREE.MeshStandardMaterial({ color: 0x333344 })); fan.position.set(-3.2, 2.6, 0); fan.rotation.y = Math.PI / 2; boat.add(fan);
// Port Gellhorn (north-west coast): cranes and containers
const port = new THREE.Group(); isl.add(port);
for (let i = 0; i < 3; i++) { const x = -225 + i * 22, z = -150;
  const mast = new THREE.Mesh(new THREE.BoxGeometry(2.4, 26, 2.4), new THREE.MeshStandardMaterial({ color: 0xFF7A3D })); mast.position.set(x, 13, z); port.add(mast);
  const arm = new THREE.Mesh(new THREE.BoxGeometry(22, 2, 2), new THREE.MeshStandardMaterial({ color: 0xFF7A3D })); arm.position.set(x + 6, 25, z + 6); arm.rotation.y = -0.6; port.add(arm); }
for (let i = 0; i < 24; i++) { const c = new THREE.Mesh(new THREE.BoxGeometry(7, 3, 3), new THREE.MeshStandardMaterial({ color: [0x3D7BFF, 0xFF3D8B, 0xFFC94A, 0x2EE6D6][i % 4], roughness: 0.5 }));
  c.position.set(-235 + (i % 6) * 8, 3.5 + Math.floor(i / 12) * 3.1, -172 + (Math.floor(i / 6) % 2) * 4); port.add(c); }
// Ambrosia (north-centre): the lake, sugar-cane rows, a mill
const lake = new THREE.Mesh(new THREE.CylinderGeometry(24, 24, 1, 40), new THREE.MeshStandardMaterial({ color: 0x3D8FD8, roughness: 0.15, metalness: 0.4 }));
lake.position.set(40, 2.2, -40); isl.add(lake);
const cropM = new THREE.MeshStandardMaterial({ color: 0xC9D86A, roughness: 0.8 });
for (let r = 0; r < 9; r++) { const row = new THREE.Mesh(new THREE.BoxGeometry(46, 1.6, 2.2), cropM); row.position.set(-10, 3, -95 + r * 6); isl.add(row); }
const mill = box(10, 9, 8, 0xB0B4C8, 10, -110, 0); const chim = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.8, 18, 10), new THREE.MeshStandardMaterial({ color: 0x8A8FA8 }));
chim.position.set(16, 11, -112); isl.add(chim);
// Mount Kalaga (north): a mountain Florida doesn't have
const mtn = new THREE.Mesh(new THREE.ConeGeometry(34, 48, 9), new THREE.MeshStandardMaterial({ color: 0x6E6A8E, roughness: 0.9, flatShading: true }));
mtn.position.set(-70, 24, -170); isl.add(mtn);
const snow = new THREE.Mesh(new THREE.ConeGeometry(12, 17, 9), new THREE.MeshStandardMaterial({ color: 0xF4F2FF, roughness: 0.6, flatShading: true }));
snow.position.set(-70, 41.5, -170); isl.add(snow);
// region rings: a pink halo marks the region being talked about
const ringM = new THREE.MeshBasicMaterial({ color: 0xFF3D8B, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false });
function ring(x, z, r) { const m = new THREE.Mesh(new THREE.RingGeometry(r, r + 2.6, 48), ringM.clone()); m.rotation.x = -Math.PI / 2; m.position.set(x, 6, z); isl.add(m); return m; }
const rings = { vc: ring(100, 175, 44), keys: ring(0, 300, 82), gr: ring(45, 175, 52), pg: ring(-215, -160, 34), am: ring(25, -65, 58), ka: ring(-70, -170, 40) };
const W = (x, z) => [OX + x, OZ + z];
"""

keys_js = r"""
const over = (h, back) => [[OX, h, OZ + back], [OX - 20, 0, OZ - 10]];
const at = (x, z, h, back) => [[OX + x, h, OZ + z + back], [OX + x, 0, OZ + z]];
const keys = [
  [0, [OX, 260, OZ + 700], [OX, 20, OZ - 120]],
  [K.l1 - 0.3, ...over(520, 560)],
  [K.l2 - 0.1, ...over(500, 540)],
  [K.l2 + 0.8, ...at(100, 175, 95, 120)], [K.l4 - 0.2, ...at(100, 175, 90, 112)],
  [K.l4 + 0.8, ...at(10, 290, 180, 200)], [K.l5 + 0.2, ...at(10, 290, 170, 190)],
  [K.l5 + 0.9, ...at(LENTO[0], LENTO[1], 60, 80)], [K.l6 - 0.2, ...at(LENTO[0], LENTO[1], 58, 76)],
  [K.l6 + 0.8, ...at(45, 175, 85, 110)], [K.l8 - 0.2, ...at(45, 175, 80, 104)],
  [K.l8 + 0.8, ...at(-215, -160, 80, 110)], [K.l9 - 0.2, ...at(-215, -160, 76, 104)],
  [K.l9 + 0.8, ...at(25, -65, 110, 140)], [K.l10 - 0.2, ...at(25, -65, 104, 132)],
  [K.l10 + 0.8, ...at(-70, -170, 70, 150)], [K.l12 - 0.2, ...at(-70, -170, 66, 140)],
  [K.l12 + 1.0, ...over(560, 600)],
  [DUR, ...over(600, 640)],
];
"""

render_js = r"""
  const ui = eo((t - 0.2) / 1.2); isl.scale.set(1, Math.max(0.01, ui), 1); isl.position.y = -6 * (1 - ui);
  fan.rotation.x = t * 40;
  boat.position.x = 40 + Math.sin(t * 0.8) * 10;
  pin("tg-leo", OX - 40, 20, OZ + 40, win(t, K.l1 + 0.4, K.l2 + 0.1));
  document.getElementById("tg-leo-s").textContent = t < K.florida - 0.1 ? "el estado de GTA 6" : "≈ Florida";
  const R_ = (r, a, b) => { r.material.opacity = 0.85 * win(t, a, b, 0.3); };
  R_(rings.vc, K.l2, K.l4); R_(rings.keys, K.l4, K.l6); R_(rings.gr, K.l6, K.l8); R_(rings.pg, K.l8, K.l9); R_(rings.am, K.l9, K.l10); R_(rings.ka, K.l10, K.l12 + 0.3);
  pin("tg-vc", OX + 100, 34, OZ + 175, win(t, K.l2 + 0.6, K.l4 + 0.1));
  pin("tg-keys", OX + 5, 14, OZ + 300, win(t, K.l4 + 0.7, K.l5 + 0.6));
  pin("tg-lento", OX + LENTO[0], 8, OZ + LENTO[1], win(t, K.l5 + 0.8, K.l6 + 0.1));
  pin("tg-gr", OX + 45, 14, OZ + 175, win(t, K.l6 + 0.6, K.l8 + 0.1));
  pin("tg-pg", OX - 215, 32, OZ - 160, win(t, K.l8 + 0.6, K.l9 + 0.1));
  pin("tg-am", OX + 25, 16, OZ - 65, win(t, K.l9 + 0.6, K.l10 + 0.1));
  pin("tg-ka", OX - 70, 56, OZ - 170, win(t, K.l10 + 0.6, K.l12 + 0.1));
"""

overlay_js = r"""
tl.fromTo("#bg-no", { opacity: 0, scale: 1.8, rotation: -7 }, { opacity: 1, scale: 1, rotation: -7, duration: 0.18, ease: "power4.out" }, K.existe);
tl.fromTo("#bg-real", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, K.real - 0.1);
tl.to(["#bg-no", "#bg-real"], { opacity: 0, duration: 0.2 }, K.l1 + 0.2);
tl.fromTo("#bg-ka", { opacity: 0, scale: 1.8, rotation: 6 }, { opacity: 1, scale: 1, rotation: 6, duration: 0.18, ease: "power4.out" }, K.invento - 0.4);
tl.to("#bg-ka", { opacity: 0, duration: 0.2 }, K.l11 - 0.1);
tl.fromTo("#bg-2002", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, K.y2002 - 0.2);
tl.to("#bg-2002", { opacity: 0, duration: 0.2 }, K.l4 - 0.1);
tl.fromTo("#bg-hum", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, K.humedal - 0.2);
tl.to("#bg-hum", { opacity: 0, duration: 0.2 }, K.l8 - 0.1);
tl.fromTo("#bg-105", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, K.ciento - 0.2);
tl.to("#bg-105", { opacity: 0, duration: 0.2 }, K.l12 - 0.1);
tl.fromTo("#bg-big", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, K.grande12 - 0.2);
tl.to("#bg-big", { opacity: 0, duration: 0.2 }, K.l13 - 0.15);
tl.fromTo("#bg-cta", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, K.l13);
"""

k = K
R.sfx(0.05, "barrido-largo.wav", 0.45)
R.sfx(0.3, "subida-1.wav", 0.35)
R.sfx(k["existe"], "sello.wav", 0.6)
R.sfx(k["real"] - 0.1, "pop-1.wav", 0.45)
for key in ("l2", "l4", "l5", "l6", "l8", "l9", "l10"):
    R.sfx(k[key] + 0.05, "barrido-1.wav" if key in ("l2", "l5", "l8", "l10") else "barrido-2.wav", 0.4)
R.sfx(k["miami"], "pop-2.wav", 0.4)
R.sfx(k["l4"] + 0.7, "agua.wav", 0.35)
R.sfx(k["everglades"], "pop-2.wav", 0.4)
R.sfx(k["l6"] + 0.4, "lancha.wav", 0.3)
R.sfx(k["panama"], "pop-2.wav", 0.4)
R.sfx(k["okeechobee"], "pop-2.wav", 0.4)
R.sfx(k["invento"] - 0.4, "sello.wav", 0.6)
R.sfx(k["l12"] + 0.1, "barrido-largo.wav", 0.4)
R.sfx(k["grande12"] - 0.2, "impacto.wav", 0.45)
R.sfx(k["y2002"] - 0.2, "pop-1.wav", 0.4)
R.sfx(k["humedal"] - 0.2, "pop-1.wav", 0.4)
R.sfx(k["ciento"] - 0.2, "pop-1.wav", 0.4)
R.sfx(k["l13"], "pop-1.wav", 0.5)

CAPS = [
    "Leonida no existe. Pero casi todo en ella es real.",
    "Es el estado de GTA 6, y está inspirado en Florida.",
    "Vice City es Miami: rascacielos, playas y noches de neón.",
    "Y no es nueva: ya apareció en GTA Vice City, en 2002.",
    "Los Cayos de Leonida copian los Cayos de Florida.",
    "Key Lento, por ejemplo, está inspirado en Key Largo.",
    "Grassrivers son los Everglades: pantanos, lanchas de aire y caimanes.",
    "Los Everglades reales son el mayor humedal subtropical de Estados Unidos.",
    "Port Gellhorn recuerda a la costa del golfo, como Panama City.",
    "Ambrosia, a los pueblos azucareros junto al lago Okeechobee.",
    "Y el monte Kalaga, no existe en Florida. Rockstar lo inventó.",
    "El punto más alto de la Florida real mide apenas 105 metros.",
    "Un estado entero, en el mapa más grande que Rockstar ha hecho.",
    None,
]
HL = {"2002.", "humedal", "105", "existe.", "real.", "florida.", "miami:", "cayos", "largo.", "everglades:", "panama", "city.", "okeechobee.", "kalaga,", "inventó.", "grande"}

R.write(R.mundo(body, sets_js, keys_js, render_js, overlay_js, K), R.subs(CAPS, HL))
