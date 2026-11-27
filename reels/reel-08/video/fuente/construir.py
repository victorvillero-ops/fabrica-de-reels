"""Reel 08 — 7 detalles de GTA 6 tan realistas que dan miedo. Low-poly people on the Leonida beach at sunset:
a pedestrian throws a drink, a crowd of 600.000 animations, sweat that grows with effort, weight and muscle,
local rain seen from the sea, the police identifying you, and the wind carrying speech bubbles.
Built on the series builder (reels/serie). The last line runs back into the hook so the reel loops."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "serie"))
from serie import Reel, GOLD, PINK

R = Reel(Path(__file__).parent)
w = R.wt
K = {
    "puede": w(0, "puede"), "tirar": w(0, "tirar"), "bebida": w(0, "bebida"), "encima": w(0, "encima"),
    "l1": R.ls(1), "caracter": w(1, "caracter"), "defienden": w(1, "defienden"), "huyen": w(1, "huyen"),
    "l2": R.ls(2), "siete": w(2, "siete", ["7"]),
    "l3": R.ls(3), "k600": w(3, "seiscientas", ["600"]), "animaciones": w(3, "animaciones"), "diez": w(3, "diez", ["10"]),
    "veces": w(3, "veces"), "gta5": w(3, "gta"),
    "l4": R.ls(4), "sudan": w(4, "sudan"), "entrenan": w(4, "entrenan"), "bailan": w(4, "bailan"), "parados": w(4, "parados"),
    "l5": R.ls(5), "comes": w(5, "comes"), "peso": w(5, "peso"), "gimnasio": w(5, "gimnasio"), "musculos": w(5, "musculos"),
    "l6": R.ls(6), "llover": w(6, "llover"), "sol": w(6, "sol"),
    "l7": R.ls(7), "sabe": w(7, "sabe"), "identifica": w(7, "identifica"),
    "l8": R.ls(8), "quitarte": w(8, "quitarte"), "gorra": w(8, "gorra"), "basta": w(8, "basta"),
    "ropa": w(8, "ropa"), "cara": w(8, "cara"), "coche": w(8, "coche"),
    "l9": R.ls(9), "loco": w(9, "loco"), "viento": w(9, "viento"),
    "l10": R.ls(10), "conversaciones": w(10, "conversaciones"), "calle": w(10, "calle"), "mas10": w(10, "mas"), "lejos": w(10, "lejos"),
    "l11": R.ls(11), "real": w(11, "real"), "antes": w(11, "antes"), "recuerda": w(11, "recuerda"),
    "end": R.total,
}
K["title_out"] = round(K["puede"] - 0.1, 3)

# ------------------------------------------------------------------ HUD pieces (inline SVG, our palette)
BURGER = ('<svg class="b" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#1B0B3A" stroke="#FFC94A" stroke-width="5"/>'
          '<path d="M24 46 Q50 18 76 46 Z" fill="#FFB347"/><rect x="22" y="48" width="56" height="7" rx="3" fill="#3FD07A"/>'
          '<rect x="24" y="56" width="52" height="10" rx="4" fill="#6B3A2A"/><path d="M24 68 H76 Q74 80 50 80 Q26 80 24 68 Z" fill="#FFB347"/></svg>')
DUMBBELL = ('<svg class="b" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#1B0B3A" stroke="#FFC94A" stroke-width="5"/>'
            '<rect x="30" y="46" width="40" height="8" fill="#C9B8FF"/><rect x="18" y="32" width="12" height="36" rx="3" fill="#FF3D8B"/>'
            '<rect x="70" y="32" width="12" height="36" rx="3" fill="#FF3D8B"/><rect x="11" y="39" width="8" height="22" rx="2" fill="#FF3D8B"/>'
            '<rect x="81" y="39" width="8" height="22" rx="2" fill="#FF3D8B"/></svg>')
def item(label, inner, iid=""):
    i = f' id="{iid}"' if iid else ""
    return f'<div class="it"{i}><div class="lab">{label}</div>{inner}</div>'

HUD = {
    "h3": item("SUDOR", '<div class="meter"><div id="sw-fill"></div></div>'),
    "h4": item("COMIDA", BURGER, "h4a") + item("PESO", '<span class="pill" id="kg">72 KG</span>') + item("GIMNASIO", DUMBBELL, "h4c"),
    "h6": item("LA POLICÍA", '<span class="pill" id="st">¿QUIÉN ERES?</span>'),
    "h6b": item("RECUERDA", '<span class="pill red">ROPA</span>', "c-ropa") + item("&nbsp;", '<span class="pill red">CARA</span>', "c-cara").replace('class="lab"', 'class="lab" style="visibility:hidden"')
           + item("&nbsp;", '<span class="pill red">COCHE</span>', "c-coche").replace('class="lab"', 'class="lab" style="visibility:hidden"'),
}

body = f"""
<style>
  .hud {{ position:absolute; left:230px; top:540px; width:800px; display:flex; justify-content:center; align-items:flex-end; gap:22px; opacity:0; }}
  .it {{ display:flex; flex-direction:column; align-items:center; }}
  .lab {{ font-family:'Inter',sans-serif; font-weight:800; font-size:30px; letter-spacing:0.08em; color:#fff; background:#2A0B4A; padding:4px 14px; border-radius:10px; margin-bottom:10px; }}
  .b {{ width:118px; height:118px; display:block; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  .pill {{ display:inline-block; font-family:'Montserrat',sans-serif; font-weight:900; font-size:44px; color:{GOLD}; background:#1B0B3A; border:5px solid {GOLD};
          border-radius:20px; padding:20px 24px 16px; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); white-space:nowrap; }}
  .pill.red, .pill.on {{ color:#fff; background:#E8213B; border-color:#fff; }}
  .meter {{ width:460px; height:64px; border-radius:32px; background:#1B0B3A; border:5px solid {GOLD}; overflow:hidden; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  #sw-fill {{ height:100%; width:10%; background:linear-gradient(90deg,#6FD8FF,#FF3D8B); border-radius:28px; }}
  #h4c {{ opacity:0; }} #h6b .it {{ opacity:0; }}
  #cnt {{ position:absolute; left:64px; top:556px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:54px; color:#2A0B4A; background:{GOLD};
         padding:10px 20px 4px; border-radius:16px; transform:rotate(-6deg); opacity:0; box-shadow:0 8px 0 #2A0B4A; }}
  #bars {{ position:absolute; left:90px; top:905px; width:900px; padding:26px 30px 22px; border-radius:26px; background:rgba(27,11,58,0.9); border:5px solid {GOLD};
          opacity:0; box-shadow:0 20px 40px rgba(0,0,0,0.5); }}
  #bars .row {{ display:flex; align-items:center; gap:18px; margin-bottom:22px; }}
  #bars .bl {{ width:150px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:44px; color:#fff; }}
  #bars .track {{ flex:1; height:56px; border-radius:14px; background:#3A2266; overflow:hidden; }}
  #bars .fillb {{ height:100%; width:100%; background:linear-gradient(90deg,{PINK},{GOLD}); border-radius:14px; transform-origin:left center; transform:scaleX(0); }}
  #bars .bv {{ width:230px; text-align:right; font-family:'Montserrat',sans-serif; font-weight:900; font-size:44px; color:{GOLD}; }}
  #bars .x10 {{ text-align:center; font-family:'Montserrat',sans-serif; font-weight:900; font-size:56px; opacity:0; }}
</style>
<div class="big" id="bg-title" style="top:500px;font-size:150px;opacity:1"><span class="grad">GTA 6</span><br><span class="plate" style="font-size:50px">7 DETALLES QUE DAN MIEDO</span></div>
<div id="cnt">1/7</div>
{''.join(f'<div class="hud" id="{k}">{v}</div>' for k, v in HUD.items())}
<div class="tag" id="tg-def" style="font-size:50px"><span class="grad">SE DEFIENDE</span></div>
<div class="tag" id="tg-huye" style="font-size:56px"><span class="grad">HUYE</span></div>
<div class="tag" id="tg-sw" style="font-size:56px"><span class="grad" id="tg-sw-t">ENTRENA</span></div>
<div class="tag" id="tg-w" style="font-size:56px"><span class="grad" id="tg-w-t">+ PESO</span></div>
<div class="tag" id="tg-rain" style="font-size:60px"><span class="grad">LLUVIA</span></div>
<div class="tag" id="tg-sun" style="font-size:60px"><span class="grad">SOL</span></div>
<div class="tag" id="tg-cerca" style="font-size:46px"><span class="grad">SE QUEDA CERCA</span></div>
<div class="tag" id="tg-lejos" style="font-size:46px"><span class="grad">LLEGA LEJOS</span></div>
<div class="big" id="bg-6" style="top:900px;font-size:84px"><span class="plate">Y QUEDAN 6</span></div>
<div class="big" id="bg-count" style="top:600px;font-size:150px"><span class="grad" id="num">0</span><br><span class="plate" style="font-size:56px">ANIMACIONES</span></div>
<div id="bars">
  <div class="row"><span class="bl">GTA 6</span><div class="track"><div class="fillb" id="b6"></div></div><span class="bv">600.000</span></div>
  <div class="row"><span class="bl">GTA 5</span><div class="track"><div class="fillb" id="b5" style="width:9.2%;background:#9B8BC8"></div></div><span class="bv">~55.000</span></div>
  <div class="x10"><span class="plate">MÁS DE ×10</span></div>
</div>
<div class="big" id="bg-ident" style="top:730px;font-size:72px"><span class="plate">TE IDENTIFICA</span></div>
<div class="big" id="bg-nobasta" style="top:740px;font-size:80px"><span class="stamp">NO BASTA</span></div>
<div class="big" id="bg-loco" style="top:640px;font-size:72px"><span class="plate">EL MÁS LOCO</span></div>
<div class="big" id="bg-viento" style="top:620px;font-size:140px"><span class="grad">EL VIENTO</span></div>
<div class="big" id="bg-cta" style="top:840px;font-size:96px">¿CUÁL TE PARECE<br><span class="grad">MÁS REAL?</span></div>
"""

sets_js = r"""
const ZR = 10, CS = 1.6;
const RS = seeded(808);
for (let i = 0; i < 16; i++) palm(-60 + i * 30 + RS() * 8, ZR + 16 + RS() * 6, 1.3 + RS() * 0.5, (RS() - 0.5) * 1.4);
const hsh = (i, c) => { const s = Math.sin(i * 127.1 + c * 311.7) * 43758.5453; return s - Math.floor(s); };
const tmpV = new THREE.Vector3(), tmpW = new THREE.Vector3();
// ---- low-poly person: legs, hip pivot (torso, head, arms), optional cap
const MAT = (c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.6 });
const SKIN = [0xC98B6B, 0x8D5A3E, 0xE0B090];
function person(x, z, ry, o) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; scene.add(g);
  const shirt = MAT(o.shirt), pants = MAT(o.pants || 0x2A1A4A), skin = MAT(o.skin || SKIN[0]);
  const P = { g, shirt, shirtHex: o.shirt, base: [x, z, ry, o.y || 0] };
  const leg = (s) => { const p = new THREE.Group(); p.position.set(0.13 * s, 0.9, 0); g.add(p);
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.1, 0.9, 8), pants); m.position.y = -0.45; p.add(m); p.userData.m = m; return p; };
  P.legL = leg(1); P.legR = leg(-1);
  const hip = new THREE.Group(); hip.position.y = 0.9; g.add(hip); P.hip = hip;
  P.torso = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.24, 0.75, 12), shirt); P.torso.position.y = 0.375; hip.add(P.torso);
  P.belly = new THREE.Mesh(new THREE.SphereGeometry(0.3, 12, 10), shirt); P.belly.position.set(0, 0.22, 0.08); P.belly.scale.setScalar(0.001); hip.add(P.belly);
  P.head = new THREE.Mesh(new THREE.SphereGeometry(0.22, 14, 10), skin); P.head.position.y = 0.97; hip.add(P.head);
  const arm = (s) => { const p = new THREE.Group(); p.position.set(0.39 * s, 0.68, 0); hip.add(p);
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.07, 0.66, 8), shirt); m.position.y = -0.33; p.add(m);
    const h = new THREE.Mesh(new THREE.SphereGeometry(0.095, 10, 8), skin); h.position.y = -0.7; p.add(h);
    const d = new THREE.Mesh(new THREE.SphereGeometry(0.17, 10, 8), shirt); d.scale.setScalar(0.001); p.add(d);
    p.userData = { m, h, d }; return p; };
  P.armL = arm(1); P.armR = arm(-1);
  if (o.cap) { P.cap = new THREE.Group(); const cm = MAT(o.cap);
    P.cap.add(new THREE.Mesh(new THREE.CylinderGeometry(0.235, 0.235, 0.1, 14), cm));
    const v = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.03, 0.24), cm); v.position.set(0, -0.03, 0.22); P.cap.add(v);
    P.cap.position.y = 1.15; hip.add(P.cap); }
  g.scale.setScalar(CS);
  return P;
}
function pose(P, q) {
  q = q || {};
  P.g.position.set(q.x ?? P.base[0], (q.y || 0) + P.base[3], q.z ?? P.base[1]); P.g.rotation.set(0, q.ry ?? P.base[2], 0);
  P.hip.position.y = 0.9 + (q.bob || 0); P.hip.rotation.set(q.tilt || 0, q.twist || 0, q.sway || 0);
  const aL = q.aL || [0, 0.12], aR = q.aR || [0, -0.12];
  P.armL.rotation.set(aL[0], 0, aL[1]); P.armR.rotation.set(aR[0], 0, aR[1]);
  P.legL.rotation.set(q.lL || 0, 0, q.sL || 0); P.legR.rotation.set(q.lR || 0, 0, -(q.sL || 0));
}
// ---- car (faces +x); police adds a stripe and a light bar
function makeCar(color, police) {
  const car = new THREE.Group(); scene.add(car);
  const paint = new THREE.MeshStandardMaterial({ color, roughness: 0.35, metalness: 0.3 });
  const glass = new THREE.MeshStandardMaterial({ color: 0x2A1A4A, roughness: 0.1, metalness: 0.6 });
  const add = (geo, mat, x, y, z) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); car.add(m); return m; };
  add(new THREE.BoxGeometry(4.6, 0.9, 2.0), paint, 0, 0.75, 0);
  add(new THREE.BoxGeometry(2.4, 0.75, 1.8), glass, -0.35, 1.575, 0);
  add(new THREE.BoxGeometry(2.2, 0.12, 1.84), paint, -0.35, 1.98, 0);
  const wheelM = new THREE.MeshStandardMaterial({ color: 0x15101F, roughness: 0.8 });
  for (const [x, z] of [[1.45, 1.0], [1.45, -1.0], [-1.45, 1.0], [-1.45, -1.0]]) {
    const wh = add(new THREE.CylinderGeometry(0.4, 0.4, 0.34, 18), wheelM, x, 0.4, z); wh.rotation.x = Math.PI / 2; }
  const headM = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xFFF2C0, emissiveIntensity: 1.2 });
  const tailM = new THREE.MeshStandardMaterial({ color: 0xff2040, emissive: 0xff2040, emissiveIntensity: 0.9 });
  for (const z of [0.65, -0.65]) { add(new THREE.BoxGeometry(0.08, 0.2, 0.42), headM, 2.31, 0.9, z); add(new THREE.BoxGeometry(0.08, 0.2, 0.42), tailM, -2.31, 0.9, z); }
  const out = { car };
  if (police) {
    add(new THREE.BoxGeometry(4.62, 0.32, 2.02), new THREE.MeshStandardMaterial({ color: 0x1B2A6B, roughness: 0.4 }), 0, 0.62, 0);
    out.red = new THREE.MeshStandardMaterial({ color: 0xff2030, emissive: 0xff2030, emissiveIntensity: 0.3 });
    out.blue = new THREE.MeshStandardMaterial({ color: 0x2060ff, emissive: 0x2060ff, emissiveIntensity: 0.3 });
    add(new THREE.BoxGeometry(0.5, 0.24, 0.8), out.red, -0.35, 2.16, 0.45); add(new THREE.BoxGeometry(0.5, 0.24, 0.8), out.blue, -0.35, 2.16, -0.45);
  }
  car.scale.setScalar(1.1);
  return out;
}
const dropGeo = new THREE.SphereGeometry(0.08, 8, 6);
const drinkM = new THREE.MeshStandardMaterial({ color: 0x9B2E6A, emissive: 0x6A1A48, emissiveIntensity: 0.5, roughness: 0.2 });
const sweatM = new THREE.MeshStandardMaterial({ color: 0xBFEFFF, emissive: 0x6FD8FF, emissiveIntensity: 0.7, roughness: 0.1 });
const drops = (n, m) => Array.from({ length: n }, () => { const d = new THREE.Mesh(dropGeo, m); d.visible = false; scene.add(d); return d; });

// ---- 1: the drink. Player (cap) vs pedestrian with a cup; one defends, one runs
const PL = person(-1.6, ZR, Math.PI / 2, { shirt: 0x2EE6D6, cap: 0xFFC94A });
const PA = person(1.6, ZR, -Math.PI / 2, { shirt: 0xFF3D8B, skin: SKIN[2], pants: 0x3A2A66 });
const PB = person(3.9, ZR + 3, Math.PI - 0.5, { shirt: 0xFFC94A, skin: SKIN[1] });
const PC = person(-3.9, ZR + 3, Math.PI + 0.5, { shirt: 0x9B5BFF });
const cup = new THREE.Group(); cup.position.y = -0.8; PA.armR.add(cup);
const cupBody = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.1, 0.34, 14), new THREE.MeshStandardMaterial({ color: 0xF4EEF8, roughness: 0.4 }));
cupBody.position.y = 0.12; cup.add(cupBody);
const band = new THREE.Mesh(new THREE.CylinderGeometry(0.142, 0.125, 0.1, 14), new THREE.MeshStandardMaterial({ color: 0xFF3D8B })); band.position.y = 0.13; cup.add(band);
const straw = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.32, 6), new THREE.MeshStandardMaterial({ color: 0xFFC94A })); straw.position.set(0.04, 0.38, 0); cup.add(straw);
const STREAM = drops(46, drinkM), SPLASH = drops(26, drinkM), DRIP = drops(12, drinkM);
// ---- 2: a crowd, each one doing its own animation
const CROWD = [];
const CCOL = [0xFF3D8B, 0xFFC94A, 0x2EE6D6, 0x9B5BFF, 0xFF8C55, 0x6FA8FF];
for (let j = 0; j < 12; j++) { const c = j % 4, r = Math.floor(j / 4);
  CROWD.push(person(60 - 3.9 + c * 2.6 + (r % 2) * 1.0, ZR - 1 + r * 3.2, Math.PI, { shirt: CCOL[j % 6], skin: SKIN[j % 3], cap: j % 3 === 0 ? 0x2A1A4A : null })); }
// ---- 3: sweat
const PS = person(120, ZR, Math.PI, { shirt: 0xFF3D8B, skin: SKIN[1], pants: 0x1B0B3A });
const SWEAT = drops(30, sweatM);
// ---- 4: weight and muscle, standing on a scale
const PW = person(180, ZR, Math.PI, { shirt: 0x2EE6D6, cap: 0xFFC94A, y: 0.2 });
const scaleBox = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.2, 1.2), new THREE.MeshStandardMaterial({ color: 0xEDE6F5, roughness: 0.4 }));
scaleBox.position.set(180, 0.1, ZR); scene.add(scaleBox);
const dial = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.04, 0.3), new THREE.MeshStandardMaterial({ color: 0x1B0B3A, emissive: 0xFFC94A, emissiveIntensity: 0.6 }));
dial.position.set(180, 0.21, ZR - 0.38); scene.add(dial);
// ---- 5: local weather seen from the sea: a rain cloud over one district
const CLX = -72, CLZ = -170, CLY = 80;
const cloud = new THREE.Group(); cloud.position.set(CLX, CLY, CLZ); scene.add(cloud);
const cloudM = new THREE.MeshStandardMaterial({ color: 0x4A3F66, roughness: 1, emissive: 0xC9D8FF, emissiveIntensity: 0, fog: false });
const RC = seeded(55);
for (let i = 0; i < 11; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(7 + RC() * 7, 14, 10), cloudM);
  s.position.set((RC() - 0.5) * 42, (RC() - 0.5) * 8, (RC() - 0.5) * 16); s.scale.y = 0.7; cloud.add(s); }
cloud.userData.k = 1.3;
const NR = 420, rainM = new THREE.MeshBasicMaterial({ color: 0xCFDAFF, transparent: true, opacity: 0.8, fog: false });
const rain = new THREE.InstancedMesh(new THREE.BoxGeometry(0.5, 5.5, 0.5), rainM, NR); scene.add(rain);
const RAIN = Array.from({ length: NR }, () => [CLX + (RC() - 0.5) * 56, CLZ + (RC() - 0.5) * 22, RC()]);
const rainObj = new THREE.Object3D();
const raysTex = canvasTex(512, 512, (g, W) => { g.translate(W / 2, W / 2); for (let i = 0; i < 16; i++) { g.rotate(Math.PI / 8);
  const gr = g.createLinearGradient(0, 0, W / 2, 0); gr.addColorStop(0, "rgba(255,230,140,0.9)"); gr.addColorStop(1, "rgba(255,200,90,0)");
  g.fillStyle = gr; g.beginPath(); g.moveTo(0, 0); g.lineTo(W / 2, -18); g.lineTo(W / 2, 18); g.closePath(); g.fill(); } });
const rays = new THREE.Sprite(new THREE.SpriteMaterial({ map: raysTex, transparent: true, opacity: 0, depthWrite: false, fog: false }));
rays.scale.set(1100, 1100, 1); scene.add(rays);
// ---- 6: police. Player, his pink car, a police car with a light bar
const PO = person(259.6, ZR, Math.PI, { shirt: 0x2EE6D6, cap: 0xFFC94A });
const pinkCar = makeCar(0xFF3D8B, false); pinkCar.car.position.set(256.2, 0, ZR + 3.6); pinkCar.car.rotation.y = -Math.PI / 2;
const cop = makeCar(0xF4F2FA, true); cop.car.rotation.y = Math.PI;
const ringM = () => new THREE.MeshBasicMaterial({ color: 0xFFC94A, transparent: true, opacity: 0, depthTest: false });
const ringTorso = new THREE.Mesh(new THREE.TorusGeometry(0.78, 0.07, 8, 40), ringM()); ringTorso.rotation.x = Math.PI / 2; ringTorso.position.set(259.6, 2.0, ZR);
const ringHead = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.07, 8, 40), ringM()); ringHead.position.set(259.6, 3.05, ZR - 0.2);
const ringCar = new THREE.Mesh(new THREE.TorusGeometry(3.4, 0.12, 8, 60), ringM()); ringCar.rotation.x = Math.PI / 2; ringCar.position.set(256.2, 0.3, ZR + 3.6);
const ringRed = new THREE.Mesh(new THREE.TorusGeometry(1.1, 0.09, 8, 40), new THREE.MeshBasicMaterial({ color: 0xFF2040, transparent: true, opacity: 0, depthTest: false }));
ringRed.rotation.x = Math.PI / 2; ringRed.position.set(259.6, 0.15, ZR);
[ringTorso, ringHead, ringCar, ringRed].forEach((r) => { r.renderOrder = 5; scene.add(r); });
const scan = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 0.08), new THREE.MeshBasicMaterial({ color: 0xFF3B3B, transparent: true, opacity: 0, depthTest: false }));
scan.renderOrder = 6; scan.position.set(259.6, 1, ZR - 0.7); scene.add(scan);
// ---- 7: the wind carries bits of conversation
const PV1 = person(338.2, ZR, Math.PI / 2 + 0.6, { shirt: 0xFFC94A, skin: SKIN[2] });
const PV2 = person(341.8, ZR, -Math.PI / 2 - 0.6, { shirt: 0x9B5BFF, skin: SKIN[1], cap: 0xFF3D8B });
const RW = seeded(77);
const streakM = () => new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide });
const STREAKS = Array.from({ length: 24 }, () => { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 0.08), streakM()); scene.add(m);
  return { m, y: 0.8 + RW() * 6.5, z: ZR - 3 + RW() * 6, L: 2 + RW() * 3.5, v: 0.22 + RW() * 0.18, ph: RW(), wob: RW() * 6 }; });
function bubbleTex(text) { return canvasTex(512, 256, (g, W, H) => {
  g.fillStyle = "#FFFFFF"; g.strokeStyle = "#FF3D8B"; g.lineWidth = 12;
  g.beginPath(); g.roundRect(14, 14, W - 28, H - 70, 50); g.fill(); g.stroke();
  g.beginPath(); g.moveTo(110, H - 62); g.lineTo(80, H - 10); g.lineTo(170, H - 62); g.closePath(); g.fill();
  g.beginPath(); g.moveTo(110, H - 58); g.lineTo(80, H - 10); g.lineTo(170, H - 58); g.stroke();
  g.fillStyle = "#2A0B4A"; g.textAlign = "center"; g.textBaseline = "middle"; g.font = "900 70px Montserrat, sans-serif"; g.fillText(text, W / 2, (H - 56) / 2 + 4); }); }
const BUB = [
  { P: PV2, t0: K.l10 + 0.55, d: 0.8, life: 1.45, fade: 0.6, txt: "¿EN SERIO?" },
  { P: PV1, t0: K.calle + 0.2, d: 4.8, life: 2.1, fade: 0.88, txt: "¡JAJAJA!" },
].map((b) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: bubbleTex(b.txt), transparent: true, opacity: 0, depthWrite: false }));
  s.renderOrder = 4; scene.add(s); return { ...b, s }; });
"""

keys_js = r"""
const F = (x, d, ey, ly, dx) => [[x + (dx || 0), ey, ZR - d], [x, ly, ZR]];
const SEA = [[0, 30, 150], [0, 46, -260]], SEA2 = [[-6, 32, 156], [0, 48, -260]];
const keys = [
  [0, ...F(0, 20, 2.8, 2.2, 3)],
  [K.title_out, ...F(0, 18, 2.7, 2.2, 2.4)],
  [K.encima, ...F(0, 17, 2.7, 2.2, 1.6)],
  [K.l1 - 0.1, ...F(0, 17, 2.7, 2.2, 1.4)],
  [K.l1 + 0.9, ...F(0, 30, 3.4, 2.8, -2)],
  [K.l2 - 0.03, ...F(0, 31, 3.5, 2.8, -3)],
  [K.l2, ...SEA],
  [K.l3 - 0.03, ...SEA2],
  [K.l3, [64, 9, ZR - 20], [60, 2.0, ZR + 3]],
  [K.l4 - 0.03, [56, 8.5, ZR - 19], [60, 2.0, ZR + 3]],
  [K.l4, ...F(120, 18, 2.7, 2.1, 2)],
  [K.l5 - 0.03, ...F(120, 17, 2.7, 2.1, -1.5)],
  [K.l5, ...F(180, 18, 2.9, 2.3, -2)],
  [K.l6 - 0.03, ...F(180, 17, 2.9, 2.3, 1.5)],
  [K.l6, [0, 30, 150], [-60, 46, -260]],
  [K.l7 - 0.03, [-12, 31, 142], [-64, 46, -260]],
  [K.l7, ...F(261.5, 24, 3.2, 2.6, 3)],
  [K.l8, ...F(261, 22, 3.1, 2.6, 0.5)],
  [K.l9 - 0.03, ...F(260.5, 21, 3.1, 2.6, -1.5)],
  [K.l9, ...F(340, 26, 3.4, 2.8, -3)],
  [K.l10, ...F(341.5, 24, 3.3, 2.8, 0)],
  [K.l11 - 0.03, ...F(342, 23.5, 3.3, 2.8, 1)],
  [K.l11, ...SEA],
  [K.antes - 0.03, ...SEA2],
  [K.antes, ...F(0, 22, 3.0, 2.2, 4)],
  [DUR, ...F(0, 20, 2.8, 2.2, 3)],
];
"""

render_js = r"""
  const pinL = (id, x, y, z, o, mt) => { pin(id, x, y, z, o); const el = tags[id]; const hw = el.offsetWidth / 2;
    el.style.left = Math.min(Math.max(parseFloat(el.style.left), hw + 30), 1050 - hw).toFixed(1) + "px";
    el.style.top = Math.max(parseFloat(el.style.top), mt || 900).toFixed(1) + "px"; };
  const S1 = t < K.l3, TAU = Math.PI * 2;
  // ---------- 1: the drink
  const up = eo((t - (K.tirar - 0.3)) / 0.35) * (1 - eo((t - (K.encima + 0.5)) / 0.4));
  const armA = -0.9 - 1.15 * up;
  pose(PA, { aR: [armA, -0.1], aL: [0, 0.12], tilt: 0.12 * up });
  cup.rotation.x = -armA * (1 - up);
  const s0 = K.tirar + 0.02, s1 = K.bebida + 0.25, FL = 0.3, th = s0 + FL;
  const hit = S1 ? eo((t - th) / 0.2) * (1 - eo((t - (K.l1 + 0.8)) / 0.6)) : 0;
  pose(PL, { tilt: -0.35 * hit, aL: [-1.7 * hit, 0.35 * hit], aR: [-1.7 * hit, -0.35 * hit], x: -1.6 - 0.35 * hit });
  const wet = S1 ? clamp01((t - th) / 0.4) : 0;
  PL.shirt.color.setHex(PL.shirtHex).lerp(new THREE.Color(0x1A6F78), 0.55 * wet);
  // one defends (fists up), one runs away
  const f = S1 ? win(t, K.defienden - 0.3, K.l3, 0.25) : 0;
  pose(PB, { aL: [-1.9 * f, -0.35 * f], aR: [-1.9 * f, 0.35 * f], y: 0.1 * Math.abs(Math.sin(t * 9)) * f, ry: Math.PI - 0.5 - 0.6 * f, tilt: 0.12 * f });
  const runT = t - (K.huyen - 0.15), run = S1 && runT > 0 ? 1 : 0;
  const rx = run ? -3.9 - 12 * Math.pow(clamp01(runT / 1.7), 1.4) : -3.9;
  const ryC = run ? Math.PI + 0.5 + (Math.PI / 2 - 0.5) * eo(runT / 0.2) : Math.PI + 0.5;
  const sw = run ? Math.sin(t * 15) * 0.9 : 0;
  pose(PC, { x: rx, ry: ryC, lL: sw, lR: -sw, aL: [-sw * 0.8, 0.15], aR: [sw * 0.8, -0.15], tilt: run ? 0.25 : 0, y: run ? 0.08 * Math.abs(Math.sin(t * 15)) : 0 });
  // crowd: each one its own move
  CROWD.forEach((P, j) => { const ph = j * 0.77, k = j % 6, sn = Math.sin(t * 6 + ph);
    if (k === 0) pose(P, { aL: [0, 2.6 + 0.35 * Math.sin(t * 9 + ph)] });
    else if (k === 1) pose(P, { y: 0.55 * Math.abs(Math.sin(t * 4.5 + ph)), aL: [0, 2.4], aR: [0, -2.4] });
    else if (k === 2) pose(P, { aL: [-1.4, -0.25 - 0.3 * Math.sin(t * 11 + ph)], aR: [-1.4, 0.25 + 0.3 * Math.sin(t * 11 + ph)] });
    else if (k === 3) pose(P, { ry: Math.PI + t * 3 + ph, aL: [0, 1.4], aR: [0, -1.4] });
    else if (k === 4) pose(P, { lL: 0.6 * sn, lR: -0.6 * sn, aL: [-0.6 * sn, 0.12], aR: [0.6 * sn, -0.12], bob: 0.04 * Math.abs(sn) });
    else pose(P, { sway: 0.25 * sn, twist: 0.3 * Math.sin(t * 3 + ph), aL: [-1.2 - 0.5 * sn, 0.4], aR: [-1.2 + 0.5 * sn, -0.4] }); });
  // ---------- 3: sweat grows with effort
  const I = clamp01(0.08 + 0.62 * eo((t - (K.entrenan - 0.3)) / 0.7) + 0.3 * eo((t - K.bailan) / 0.4) - 0.92 * eo((t - (K.parados - 0.1)) / 0.5));
  { const m1 = win(t, K.entrenan - 0.15, K.bailan, 0.15), m2 = win(t, K.bailan, K.parados, 0.15);
    const s = (1 - Math.cos(TAU * 1.7 * t)) / 2, d = Math.sin(TAU * 1.4 * t);
    pose(PS, { y: 0.28 * Math.sin(Math.PI * s) * m1 + 0.06 * Math.abs(d) * m2, sL: 0.28 * s * m1, sway: 0.24 * d * m2, twist: 0.3 * d * m2,
      aL: [(-1.4 - 0.7 * d) * m2, 0.12 + 2.5 * s * m1 + 0.3 * m2], aR: [(-1.4 + 0.7 * d) * m2, -(0.12 + 2.5 * s * m1 + 0.3 * m2)],
      bob: 0.015 * Math.sin(t * 3) }); }
  // ---------- 4: food widens, the gym builds muscle
  const fat = eo((t - (K.comes - 0.1)) / 0.9), mus = eo((t - (K.gimnasio - 0.1)) / 0.9);
  { const flex = mus * (1 - 0.15 * Math.sin(t * 8));
    pose(PW, { aL: [0, 0.12 + 1.45 * flex], aR: [0, -(0.12 + 1.45 * flex)], bob: 0.015 * Math.sin(t * 3) });
    const tw = 1 + 0.5 * fat - 0.22 * mus; PW.torso.scale.set(tw + 0.25 * mus, 1, tw);
    PW.belly.scale.setScalar(Math.max(0.001, fat * (1 - 0.7 * mus)));
    [PW.legL, PW.legR].forEach((l) => l.userData.m.scale.set(1 + 0.4 * fat - 0.1 * mus, 1, 1 + 0.4 * fat - 0.1 * mus));
    [PW.armL, PW.armR].forEach((a) => { const r = 1 + 0.35 * fat + 0.9 * mus; a.userData.m.scale.set(r, 1, r); a.userData.d.scale.setScalar(Math.max(0.001, mus * 1.25)); }); }
  // ---------- 6: police
  const pc = eo((t - (K.l7 - 0.1)) / 1.3);
  cop.car.position.set(292 - 27.5 * pc, 0, ZR + 1.2);
  { const on = t > K.l7 - 0.1 && t < K.l9, ph = Math.floor(t * 6) % 2;
    cop.red.emissiveIntensity = on ? (ph ? 2.8 : 0.2) : 0.3; cop.blue.emissiveIntensity = on ? (ph ? 0.2 : 2.8) : 0.3; }
  const capUp = clamp01((t - (K.quitarte - 0.1)) / 0.45), capFly = clamp01((t - K.gorra) / 0.7);
  const handUp = eo(capUp) * (1 - eo((t - (K.gorra + 0.15)) / 0.4));
  pose(PO, { ry: Math.PI - 0.55 * eo((t - (K.l7 + 0.4)) / 0.5) * (1 - eo((t - (K.l8 - 0.2)) / 0.4)), aR: [-0.3 * handUp, -0.12 - 2.75 * handUp], tilt: 0.05 * Math.sin(t * 2) });
  if (PO.cap) { if (capFly > 0) { PO.cap.position.set(-0.4 - 1.0 * capFly, 1.5 + 0.5 * Math.sin(Math.PI * capFly) - 2.4 * capFly * capFly, 0.2 * capFly); PO.cap.rotation.set(0, 0, 3 * capFly); }
    else { PO.cap.position.set(-0.4 * eo(capUp), 1.15 + 0.35 * eo(capUp), 0); PO.cap.rotation.set(0, 0, 0.6 * eo(capUp)); } }
  { const sc = win(t, K.sabe - 0.1, K.identifica + 0.15, 0.1); scan.material.opacity = 0.95 * sc;
    scan.position.y = 0.2 + 3.4 * (0.5 - 0.5 * Math.cos(TAU * (t - K.sabe) / 0.9));
    const pu = 1 + 0.12 * Math.sin(t * 8);
    ringRed.material.opacity = 0.9 * win(t, K.identifica, K.l9 - 0.05, 0.15); ringRed.scale.setScalar(pu);
    ringTorso.material.opacity = win(t, K.ropa - 0.05, K.l9 - 0.05, 0.12); ringTorso.scale.setScalar(pu);
    ringHead.material.opacity = win(t, K.cara - 0.05, K.l9 - 0.05, 0.12); ringHead.scale.setScalar(pu);
    ringCar.material.opacity = win(t, K.coche - 0.05, K.l9 - 0.05, 0.12); ringCar.scale.setScalar(pu); }
  const st = document.getElementById("st"); const ident = t >= K.identifica - 0.05;
  { const txt = ident ? "IDENTIFICADO" : "¿QUIÉN ERES?"; if (st.textContent !== txt) st.textContent = txt; st.classList.toggle("on", ident); }
  // ---------- 7: two people chatting
  pose(PV1, { aR: [-0.7 - 0.45 * Math.sin(t * 5), -0.25], tilt: 0.06 * Math.sin(t * 4), bob: 0.02 * Math.sin(t * 7) });
  pose(PV2, { aL: [-0.6 - 0.5 * Math.sin(t * 4.3 + 1), 0.3], tilt: 0.06 * Math.sin(t * 3.4 + 2) });

  scene.updateMatrixWorld(true);
  // ---------- particles (need world positions)
  cupBody.getWorldPosition(tmpV); PL.head.getWorldPosition(tmpW);
  STREAM.forEach((d, i) => { const ti = s0 + (s1 - s0) * i / STREAM.length, u = (t - ti) / FL; d.visible = S1 && u >= 0 && u <= 1;
    if (d.visible) { const j = (hsh(i, 1) - 0.5) * 0.3; d.position.set(tmpV.x + (tmpW.x - tmpV.x) * u, tmpV.y + 0.15 + (tmpW.y + 0.1 - tmpV.y) * u + 0.7 * Math.sin(Math.PI * u) + j, tmpV.z + (tmpW.z - tmpV.z) * u + j);
      d.scale.setScalar(1.2 + 0.6 * hsh(i, 2)); } });
  SPLASH.forEach((d, i) => { const ti = th + (s1 - s0) * i / SPLASH.length, u = (t - ti) / 0.5; d.visible = S1 && u >= 0 && u <= 1;
    if (d.visible) { const a = hsh(i, 3) * TAU, sp = 1.2 + 1.4 * hsh(i, 4), vy = 1.5 + 2.5 * hsh(i, 5), tt = u * 0.5;
      d.position.set(tmpW.x - 0.2 + Math.cos(a) * sp * tt * 2, tmpW.y + 0.2 + vy * tt - 9.8 * tt * tt, tmpW.z + Math.sin(a) * sp * tt * 2); d.scale.setScalar(0.9 * (1 - 0.5 * u)); } });
  DRIP.forEach((d, i) => { const per = 0.8, c = Math.floor((t + hsh(i, 6) * per) / per), u = ((t + hsh(i, 6) * per) / per) % 1;
    d.visible = S1 && t > th + 0.4 && t < K.l2 && hsh(i, c) < 0.8;
    if (d.visible) { const a = hsh(i, c + 9) * TAU; d.position.set(tmpW.x + Math.cos(a) * 0.4, tmpW.y - 0.3 - 3.0 * u * u, tmpW.z + Math.sin(a) * 0.4); d.scale.setScalar(0.8); } });
  PS.head.getWorldPosition(tmpV);
  SWEAT.forEach((d, i) => { const per = 0.75, ph = hsh(i, 11) * per, c = Math.floor((t + ph) / per), u = ((t + ph) / per) % 1;
    d.visible = t > K.l4 - 0.2 && t < K.l5 && hsh(i, c + 50) < I;
    if (d.visible) { const a = hsh(i, c + 70) * TAU, r = 0.38; d.position.set(tmpV.x + Math.cos(a) * r * (1 + u), tmpV.y + 0.15 * Math.sin(a) - 2.6 * u * u, tmpV.z - 0.3 + Math.sin(a) * 0.15);
      d.scale.setScalar(0.8 * (1 - 0.3 * u)); } });
  // ---------- weather
  const cl = eo((t - (K.l6 - 0.25)) / 0.5) * (1 - eo((t - (K.l7 + 0.05)) / 0.3));
  cloud.visible = cl > 0.01; cloud.scale.setScalar(Math.max(0.01, cl) * 1.3);
  cloudM.emissiveIntensity = 1.6 * Math.exp(-Math.pow((t - K.llover) / 0.07, 2)) + 1.2 * Math.exp(-Math.pow((t - K.llover - 0.5) / 0.06, 2));
  const rv = win(t, K.llover - 0.35, K.l7 + 0.05, 0.25); rain.visible = rv > 0.01; rainM.opacity = 0.8 * rv;
  if (rain.visible) { RAIN.forEach(([x, z, p], i) => { const u = (p + t * 1.4) % 1; rainObj.position.set(x, (CLY - 4) * (1 - u), z); rainObj.updateMatrix(); rain.setMatrixAt(i, rainObj.matrix); });
    rain.instanceMatrix.needsUpdate = true; }
  const sunY = 150 - 40 * (t / DUR);
  rays.position.set(-40, sunY, -1490); rays.material.rotation = t * 0.35; rays.material.opacity = 0.85 * win(t, K.sol - 0.25, K.l7 + 0.05, 0.25);
  pinL("tg-rain", CLX, 0, CLZ, win(t, K.llover - 0.1, K.l7 - 0.05));
  pinL("tg-sun", -40, sunY, -1500, win(t, K.sol - 0.1, K.l7 - 0.05), 820);
  // ---------- wind streaks and bubbles
  const wv = win(t, K.viento - 0.3, K.l11 - 0.05, 0.3);
  STREAKS.forEach((s) => { const u = (s.ph + t * s.v) % 1; s.m.visible = wv > 0.01;
    s.m.position.set(324 + u * 36, s.y + 0.25 * Math.sin(t * 3 + s.wob), s.z); s.m.scale.set(s.L, 1, 1);
    s.m.material.opacity = 0.75 * wv * Math.sin(Math.PI * u); });
  BUB.forEach((b, i) => { const u = (t - b.t0) / b.life; b.s.visible = u >= 0 && u <= 1;
    if (b.s.visible) { b.P.head.getWorldPosition(tmpV); const x = tmpV.x + b.d * eo(u * 1.15), y = tmpV.y + 1.0 + 0.6 * u + 0.12 * Math.sin(u * 9);
      b.s.position.set(x, y, ZR - 0.6); const sc = 1 - 0.3 * u; b.s.scale.set(3.6 * sc, 1.8 * sc, 1);
      b.s.material.opacity = clamp01(u / 0.08) * (1 - clamp01((u - b.fade) / (1 - b.fade))); b.pos = [x, y]; } });
  { const b0 = BUB[0], b1 = BUB[1];
    if (b0.pos) pinL("tg-cerca", b0.pos[0], b0.pos[1] + 1.0, ZR - 0.6, win(t, b0.t0 + 0.12, b0.t0 + 1.3, 0.15), 720);
    else tags["tg-cerca"].style.opacity = "0";
    if (b1.pos) pinL("tg-lejos", b1.pos[0], b1.pos[1] + 1.0, ZR - 0.6, win(t, b1.t0 + 0.3, b1.t0 + 1.95, 0.15), 715);
    else tags["tg-lejos"].style.opacity = "0"; }
  // ---------- pinned labels
  pinL("tg-def", PB.g.position.x, 3.9, ZR + 3, win(t, K.defienden - 0.1, K.l2 - 0.05));
  pinL("tg-huye", rx, 3.9, ZR + 3, win(t, K.huyen - 0.05, K.l2 - 0.05));
  { const txt = t < K.bailan ? "ENTRENA" : t < K.parados - 0.05 ? "BAILA" : "PARADO"; const el = document.getElementById("tg-sw-t"); if (el.textContent !== txt) el.textContent = txt; }
  pinL("tg-sw", 120, 4.5, ZR, win(t, K.entrenan - 0.1, K.l5 - 0.05), 730);
  { const txt = t < K.gimnasio - 0.1 ? "+ PESO" : "+ MÚSCULO"; const el = document.getElementById("tg-w-t"); if (el.textContent !== txt) el.textContent = txt; }
  pinL("tg-w", 180, 4.8, ZR, win(t, K.comes, K.l6 - 0.05), 770);
  // ---------- HUD values
  document.getElementById("sw-fill").style.width = (8 + 92 * I).toFixed(1) + "%";
  { const kg = Math.round(72 + 16 * fat - 6 * mus) + " KG"; const el = document.getElementById("kg"); if (el.textContent !== kg) el.textContent = kg; }
  { const a = K.k600 - 0.25, b = K.animaciones + 0.25, u = clamp01((t - a) / (b - a)); const v = Math.round(600000 * (1 - Math.pow(1 - u, 2.2)) / 1000) * 1000;
    const txt = String(v).replace(/\B(?=(\d{3})+(?!\d))/g, "."); const el = document.getElementById("num"); if (el.textContent !== txt) el.textContent = txt; }
"""

def show(sel, t, end, kind="pop"):
    a = (f'tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {round(t, 3)});' if kind == "pop" else
         f'tl.fromTo("{sel}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {round(t, 3)});')
    return a + f'\ntl.to("{sel}", {{ opacity: 0, duration: 0.18 }}, {round(end, 3)});'

k = K
ov = [
    'tl.fromTo("#bg-title", { opacity: 1, scale: 1.0 }, { opacity: 1, scale: 1.04, duration: ' + str(k["title_out"]) + ', ease: "none" }, 0);',
    f'tl.to("#bg-title", {{ opacity: 0, y: -30, duration: 0.2, ease: "power2.in" }}, {k["title_out"] - 0.1});',
    show("#bg-6", k["siete"] - 0.6, k["l3"] - 0.1, "up"),
    show("#bg-count", k["k600"] - 0.35, k["l4"] - 0.1, "up"),
    f'tl.fromTo("#bars", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {k["diez"] - 0.35});',
    f'tl.to("#b6", {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, {k["diez"] - 0.15});',
    f'tl.to("#b5", {{ scaleX: 1, duration: 0.35, ease: "power3.out" }}, {k["gta5"] - 0.1});',
    f'tl.fromTo("#bars .x10", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {k["veces"] - 0.05});',
    f'tl.to("#bars", {{ opacity: 0, duration: 0.18 }}, {k["l4"] - 0.1});',
    show("#h3", k["l4"] + 0.3, k["l5"] - 0.05),
    show("#h4", k["comes"] - 0.15, k["l6"] - 0.05),
    f'tl.fromTo("#h4c", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {k["gimnasio"] - 0.1});',
    f'tl.fromTo("#kg", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {k["comes"] + 0.3});',
    show("#h6", k["l7"] + 0.4, k["ropa"] - 0.25),
    f'tl.fromTo("#st", {{ scale: 1.3 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {k["identifica"] - 0.05});',
    show("#bg-ident", k["identifica"] - 0.05, k["l8"] - 0.05),
    f'tl.fromTo("#bg-nobasta", {{ opacity: 0, scale: 1.8, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.18, ease: "power4.out" }}, {k["basta"] - 0.1});',
    f'tl.to("#bg-nobasta", {{ opacity: 0, duration: 0.2 }}, {k["ropa"] - 0.25});',
    f'tl.set("#h6b", {{ opacity: 1 }}, {k["ropa"] - 0.15});',
    *[f'tl.fromTo("#{cid}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {k[word] - 0.1});'
      for cid, word in (("c-ropa", "ropa"), ("c-cara", "cara"), ("c-coche", "coche"))],
    f'tl.to("#h6b", {{ opacity: 0, duration: 0.18 }}, {k["l9"] - 0.05});',
    show("#bg-loco", k["l9"] + 0.1, k["viento"] - 0.1),
    f'tl.fromTo("#bg-viento", {{ opacity: 0, x: -120 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {k["viento"] - 0.05});',
    f'tl.to("#bg-viento", {{ opacity: 0, x: 160, duration: 0.3, ease: "power2.in" }}, {k["l10"] + 0.5});',
    f'tl.fromTo("#bg-cta", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {k["l11"] - 0.3});',
    f'tl.to("#bg-cta", {{ opacity: 0, duration: 0.18 }}, {k["antes"] - 0.25});',
    f'tl.fromTo("#bg-title", {{ opacity: 0, y: 0, scale: 1.1 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "power3.out" }}, {k["recuerda"] - 0.3});',
]
# the counter: 1/7 … 7/7, swapped with a little pop at each detail
CNT = [(k["title_out"] + 0.1, "1/7"), (k["l3"], "2/7"), (k["l4"], "3/7"), (k["l5"], "4/7"), (k["l6"], "5/7"), (k["l7"], "6/7"), (k["l9"], "7/7")]
ov.append(f'tl.fromTo("#cnt", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {CNT[0][0]});')
for t, txt in CNT[1:]:
    ov.append(f'tl.fromTo("#cnt", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {t});')
ov.append(f'tl.to("#cnt", {{ opacity: 0, duration: 0.2 }}, {k["l11"] - 0.1});')
overlay_js = "\n".join(ov)
render_js = ("  const CNT = " + str([[t, c] for t, c in CNT]) + ";\n"
             "  { let c = CNT[0][1]; for (const [a, b] of CNT) if (t >= a) c = b; const el = document.getElementById(\"cnt\"); if (el.textContent !== c) el.textContent = c; }\n"
             + render_js)

# ------------------------------------------------------------------ sound
R.sfx(0.05, "subida-1.wav", 0.35)
R.sfx(k["tirar"] - 0.25, "barrido-2.wav", 0.3)
R.sfx(k["tirar"] + 0.05, "agua.wav", 0.45)
R.sfx(k["tirar"] + 0.33, "salpicadura.wav", 0.6)
R.sfx(k["title_out"] + 0.1, "pop-1.wav", 0.4)
R.sfx(k["defienden"] - 0.1, "golpe.wav", 0.3)
R.sfx(k["defienden"] - 0.1, "pop-2.wav", 0.4)
R.sfx(k["huyen"] - 0.1, "barrido-3.wav", 0.4)
R.sfx(k["siete"] - 0.15, "pop-1.wav", 0.45)
for key in ("l3", "l4", "l5", "l7", "l9"):
    R.sfx(k[key] + 0.02, "barrido-1.wav" if key in ("l3", "l5", "l9") else "barrido-2.wav", 0.4)
R.sfx(k["l2"], "barrido-largo.wav", 0.3)
for i in range(7):
    R.sfx(k["k600"] - 0.25 + i * 0.17, "tic-2.wav", 0.3)
R.sfx(k["animaciones"] + 0.2, "registradora.wav", 0.35)
R.sfx(k["diez"] - 0.15, "subida-2.wav", 0.3)
R.sfx(k["veces"] - 0.05, "sello.wav", 0.55)
R.sfx(k["l4"] + 0.3, "pop-3.wav", 0.4)
for i in range(6):
    R.sfx(k["entrenan"] + i * 0.28, "gota.wav", 0.35)
R.sfx(k["bailan"] - 0.05, "pop-1.wav", 0.4)
R.sfx(k["parados"] - 0.05, "pop-4.wav", 0.4)
R.sfx(k["comes"] - 0.15, "pop-2.wav", 0.45)
R.sfx(k["comes"] + 0.3, "monedas.wav", 0.3)
R.sfx(k["gimnasio"] - 0.1, "golpe.wav", 0.4)
R.sfx(k["l6"] - 0.1, "barrido-largo.wav", 0.15)
R.sfx(k["llover"] - 0.1, "trueno-corto.wav", 0.3)
R.sfx(k["llover"] - 0.3, "lluvia-corta.wav", 0.5)
R.sfx(k["sol"] - 0.2, "oro.wav", 0.4)
R.sfx(k["l7"] + 0.05, "sirena.wav", 0.35)
R.sfx(k["sabe"] - 0.1, "bip.wav", 0.35)
R.sfx(k["identifica"] - 0.05, "captura.wav", 0.55)
R.sfx(k["quitarte"] - 0.05, "barrido-3.wav", 0.35)
R.sfx(k["basta"] - 0.1, "sello.wav", 0.6)
for word in ("ropa", "cara", "coche"):
    R.sfx(k[word] - 0.1, "tic-1.wav", 0.45)
R.sfx(k["l9"] + 0.1, "pop-1.wav", 0.45)
R.sfx(k["viento"] - 0.2, "viento-barrido.wav", 0.3)
for t0 in (k["l10"] + 0.55, k["calle"] + 0.2):
    R.sfx(t0, "pop-3.wav", 0.4)
R.sfx(k["lejos"] - 0.3, "barrido-largo.wav", 0.3)
R.sfx(k["l11"] - 0.3, "pop-1.wav", 0.5)
R.sfx(k["antes"] - 0.05, "barrido-1.wav", 0.35)
R.sfx(k["recuerda"] - 0.3, "barrido-largo.wav", 0.35)

CAPS = [
    "En GTA 6, si te metes con un peatón, te puede tirar la bebida encima.",
    "Cada persona de la calle tiene su carácter: unas se defienden, y otras huyen.",
    "Y ese es solo el primero de siete.",
    "Dos: Rockstar creó unas 600.000 animaciones. Más de diez veces que GTA 5.",
    "Tres: Jason y Lucía sudan más cuando entrenan o bailan que cuando están parados.",
    "Cuatro: lo que comes cambia su peso, y el gimnasio, sus músculos.",
    "Cinco: puede llover en una zona del mapa y hacer sol en otra.",
    "Seis: la policía no sabe quién eres hasta que te identifica.",
    "Y quitarte la gorra no basta: recuerda tu ropa, tu cara y tu coche.",
    "Y el último, el más loco: el viento.",
    "Lleva trozos de las conversaciones de la calle más o menos lejos.",
    "¿Cuál te parece más real? Y antes de meterte con alguien, recuerda que...",
]
HL = {"bebida", "carácter", "defienden", "huyen", "siete", "600.000", "diez", "sudan", "peso", "músculos", "llover", "sol",
      "identifica", "gorra", "basta", "ropa", "cara", "coche", "viento", "lejos", "real?", "dos", "tres", "cuatro", "cinco", "seis"}

R.write(R.mundo(body, sets_js, keys_js, render_js, overlay_js, K), R.subs(CAPS, HL, sync="words"))
