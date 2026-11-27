"""Reel 06 — 7 controles de GTA 6 que el juego casi no te cuenta. A pink car drives along the Leonida promenade at sunset;
each control shows its PS5 buttons in a HUD row and acts on the car (auto drive, indicators, radio, call, hood slide,
Focus, cheats). The last line runs back into the hook so the reel loops."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "serie"))
from serie import Reel, GOLD, PINK

R = Reel(Path(__file__).parent)
w = R.wt
K = {
    "solo": w(0, "solo"),
    "l1": R.ls(1), "destino": w(1, "destino"), "abajo": w(1, "abajo"), "options": w(1, "options", ["opcion", "option", "opsion", "obsion"]),
    "l2": R.ls(2), "circulo2": w(2, "circulo"), "conduce": w(2, "conduce"),
    "l3": R.ls(3), "siete": w(3, "siete", ["7"]),
    "l4": R.ls(4), "toca4": w(4, "toca"), "interm": w(4, "intermitentes", ["intermit"]),
    "l5": R.ls(5), "veces": w(5, "veces"), "apagas": w(5, "apagas"),
    "l6": R.ls(6), "llamada": w(6, "llamada"), "circulo6": w(6, "circulo"), "rechazas": w(6, "rechazas", ["rechaz"]),
    "l7": R.ls(7), "corre": w(7, "corre"), "equis": w(7, "equis", ["x"]), "deslizas": w(7, "deslizas", ["desliz"]),
    "l8": R.ls(8), "joy": w(8, "joysticks", ["joy", "yoy", "yois", "jois"]), "focus": w(8, "focus", ["foc", "fok"]),
    "l9": R.ls(9), "pistas": w(9, "pistas"), "debiles": w(9, "debiles"),
    "l10": R.ls(10), "trucos": w(10, "trucos"), "sesenta": w(10, "sesenta", ["60"]),
    "l11": R.ls(11), "desbloq": w(11, "desbloquean", ["desbloq"]), "historia": w(11, "historia"),
    "l12": R.ls(12), "conocias": w(12, "conocias", ["conoci"]), "pereza": w(12, "pereza"),
    "end": R.total,
}

# ------------------------------------------------------------------ controller glyphs (inline SVG, our palette)
SYM = {
    "tri": '<polygon points="50,24 76,70 24,70" fill="none" stroke="#2EE6D6" stroke-width="8" stroke-linejoin="round"/>',
    "cir": '<circle cx="50" cy="50" r="24" fill="none" stroke="#FF3D8B" stroke-width="8"/>',
    "x":   '<path d="M30 30 L70 70 M70 30 L30 70" stroke="#6FA8FF" stroke-width="8" stroke-linecap="round"/>',
    "sq":  '<rect x="28" y="28" width="44" height="44" rx="4" fill="none" stroke="#D08BFF" stroke-width="8"/>',
}
def btn(sym):
    return f'<svg class="b" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#1B0B3A" stroke="{GOLD}" stroke-width="6"/>{SYM[sym]}</svg>'
def dpad(*on):
    arms = {"up": "M38 10h24v28H38z", "down": "M38 62h24v28H38z", "left": "M10 38h28v24H10z", "right": "M62 38h28v24H62z"}
    p = "".join(f'<path d="{d}" fill="{PINK if k in on else "#4A2A78"}" stroke="{GOLD}" stroke-width="3"/>' for k, d in arms.items())
    return f'<svg class="b" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#1B0B3A" stroke="{GOLD}" stroke-width="5"/>{p}<rect x="38" y="38" width="24" height="24" fill="#4A2A78"/></svg>'
def pill(t):
    return f'<span class="pill">{t}</span>'
def item(label, inner):
    return f'<div class="it"><div class="lab">{label}</div>{inner}</div>'
PLUS = '<div class="plus">+</div>'
ARROW = {"up": "M50 18 L80 58 H62 V84 H38 V58 H20 Z"}
def arrow(rot):
    return f'<svg class="ar" viewBox="0 0 100 100"><path d="{ARROW["up"]}" fill="{GOLD}" transform="rotate({rot} 50 50)"/></svg>'

HUD = {
    "h1a": item("MANTÉN", dpad("down")),
    "h1b": PLUS + item("PULSA", pill("OPTIONS")),
    "h2": item("MANTÉN", btn("cir")),
    "h4": item("TOCA", dpad("left", "right")),
    "h5": item("×2", dpad("left")),
    "h6": item("TOCA", btn("cir")),
    "h7": item("PULSA", btn("x")),
    "h8": item("A LA VEZ", '<div style="display:flex;align-items:center">' + pill("L3") + '<span class="plus2">+</span>' + pill("R3") + '</div>'),
    "h10": item("CÓDIGO EN EL MÓVIL", '<div class="code">' + "".join(arrow(r) for r in (0, 90, 180, 270)) + "</div>"),
}

body = f"""
<style>
  .hud {{ position:absolute; left:0; top:540px; width:1080px; display:flex; justify-content:center; align-items:flex-end; gap:22px; opacity:0; }}
  .it {{ display:flex; flex-direction:column; align-items:center; }}
  .lab {{ font-family:'Inter',sans-serif; font-weight:800; font-size:30px; letter-spacing:0.08em; color:#fff; background:#2A0B4A; padding:4px 14px; border-radius:10px; margin-bottom:10px; }}
  .b {{ width:118px; height:118px; display:block; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  .pill {{ display:inline-block; font-family:'Montserrat',sans-serif; font-weight:900; font-size:40px; color:{GOLD}; background:#1B0B3A; border:5px solid {GOLD};
          border-radius:20px; padding:22px 26px 18px; filter: drop-shadow(0 8px 14px rgba(0,0,0,0.5)); }}
  .plus, .plus2 {{ font-family:'Montserrat',sans-serif; font-weight:900; font-size:64px; color:#fff; text-shadow:0 4px 0 #2A0B4A; align-self:center; margin-top:40px; }}
  .plus2 {{ margin:0 14px; display:inline-block; vertical-align:middle; }}
  .code {{ display:flex; gap:8px; background:#1B0B3A; border:5px solid {GOLD}; border-radius:22px; padding:12px 18px; }}
  .ar {{ width:84px; height:84px; opacity:0; }}
  #cnt {{ position:absolute; left:64px; top:556px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:54px; color:#2A0B4A; background:{GOLD};
         padding:10px 20px 4px; border-radius:16px; transform:rotate(-6deg); opacity:0; box-shadow:0 8px 0 #2A0B4A; }}
  .bar {{ position:absolute; left:0; width:1080px; height:150px; background:#07020F; }}
  #bar-t {{ top:-150px; }} #bar-b {{ bottom:-150px; }}
  #focus {{ position:absolute; inset:0; opacity:0; background: radial-gradient(ellipse 70% 55% at 50% 55%, rgba(46,230,214,0.10) 0%, rgba(20,60,120,0.55) 100%);
           mix-blend-mode: hard-light; }}
  #phone {{ position:absolute; left:290px; top:760px; width:500px; height:250px; border-radius:40px; background:linear-gradient(180deg,#3A1A66,#1B0B3A);
           border:5px solid {GOLD}; opacity:0; box-shadow:0 20px 40px rgba(0,0,0,0.5); text-align:center; }}
  #phone .t1 {{ margin-top:30px; font-family:'Inter',sans-serif; font-weight:800; font-size:30px; letter-spacing:0.1em; color:#C9B8FF; }}
  #phone .t2 {{ margin-top:6px; font-family:'Montserrat',sans-serif; font-weight:900; font-size:52px; color:#fff; }}
  #phone .row {{ display:flex; justify-content:center; gap:120px; margin-top:22px; }}
  #phone .dot {{ width:70px; height:70px; border-radius:50%; }}
  #ph-rej {{ position:absolute; inset:0; border-radius:36px; background:#FF3B3B; display:flex; align-items:center; justify-content:center; opacity:0;
            font-family:'Montserrat',sans-serif; font-weight:900; font-size:64px; color:#fff; }}
</style>
<div id="focus"></div>
<div class="bar" id="bar-t"></div><div class="bar" id="bar-b"></div>
<div class="big" id="bg-title" style="top:600px;font-size:150px;opacity:1"><span class="grad">GTA 6</span><br><span class="plate" style="font-size:50px">7 CONTROLES QUE NO TE CUENTA</span></div>
<div id="cnt">1/7</div>
{''.join(f'<div class="hud" id="{k}">{v}</div>' for k, v in HUD.items() if k != "h1b")}
<div class="tag" id="tg-dest" style="font-size:60px"><span class="grad">DESTINO</span></div>
<div class="tag" id="tg-auto" style="font-size:64px"><span class="grad">CONDUCE SOLO</span><small>modo cine</small></div>
<div class="tag" id="tg-radio" style="font-size:66px"><span class="grad">RADIO</span><small id="tg-radio-s">sonando</small></div>
<div class="tag" id="tg-weak" style="font-size:60px"><span class="grad">PUNTOS DÉBILES</span></div>
<div id="phone"><div class="t1">LLAMADA ENTRANTE</div><div class="t2">Número oculto</div>
  <div class="row"><div class="dot" style="background:#FF3B3B"></div><div class="dot" style="background:#2EE6A0"></div></div><div id="ph-rej">RECHAZADA</div></div>
<div class="big" id="bg-6" style="top:900px;font-size:84px"><span class="plate">Y QUEDAN 6</span></div>
<div class="big" id="bg-60" style="top:860px;font-size:150px"><span class="grad">+60</span><br><span class="plate" style="font-size:64px">TRUCOS</span></div>
<div class="big" id="bg-hist" style="top:1000px;font-size:60px"><span class="stamp">AL TERMINAR LA HISTORIA</span></div>
<div class="big" id="bg-cta" style="top:840px;font-size:100px">¿CUÁL NO<br><span class="grad">CONOCÍAS?</span></div>
"""
# the OPTIONS half of control 1 joins the d-pad in the same row
body = body.replace(f'<div class="hud" id="h1a">{HUD["h1a"]}</div>',
                    f'<div class="hud" id="h1a">{HUD["h1a"]}<div id="h1b" style="display:flex;align-items:flex-end;gap:22px;opacity:0">{HUD["h1b"]}</div></div>')

sets_js = r"""
const ZR = 10, CS = 1.6;                                    // beach road line (sea side of the promenade), car scale
// ---- beach road: dark asphalt with a dashed gold centre line, palms on the sea side
const roadTex = canvasTex(512, 64, (g, W, H) => { g.fillStyle = "#2A1E3A"; g.fillRect(0, 0, W, H);
  g.fillStyle = "#FFC94A"; for (let x = 0; x < W; x += 128) g.fillRect(x, H / 2 - 3, 70, 6);
  g.fillStyle = "#E8C8D8"; g.fillRect(0, 2, W, 3); g.fillRect(0, H - 5, W, 3); }, true);
roadTex.repeat.set(1400 / 24, 1);
const road = new THREE.Mesh(new THREE.PlaneGeometry(1400, 14), new THREE.MeshStandardMaterial({ map: roadTex, roughness: 0.85 }));
road.rotation.x = -Math.PI / 2; road.position.set(0, 0.06, ZR); scene.add(road);
const RS = seeded(606);
for (let i = 0; i < 22; i++) palm(-330 + i * 34 + RS() * 8, ZR + 13 + RS() * 6, 1.3 + RS() * 0.5, (RS() - 0.5) * 1.4);
// ---- car (faces +x)
const car = new THREE.Group(); scene.add(car);
const paint = new THREE.MeshStandardMaterial({ color: 0xFF3D8B, roughness: 0.35, metalness: 0.3 });
const glass = new THREE.MeshStandardMaterial({ color: 0x2A1A4A, roughness: 0.1, metalness: 0.6 });
const add = (geo, mat, x, y, z) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); car.add(m); return m; };
add(new THREE.BoxGeometry(4.6, 0.9, 2.0), paint, 0, 0.75, 0);
add(new THREE.BoxGeometry(2.4, 0.75, 1.8), glass, -0.35, 1.575, 0);
add(new THREE.BoxGeometry(2.2, 0.12, 1.84), paint, -0.35, 1.98, 0);
const wheelM = new THREE.MeshStandardMaterial({ color: 0x15101F, roughness: 0.8 });
const WHEELS = [];
for (const [x, z] of [[1.45, 1.0], [1.45, -1.0], [-1.45, 1.0], [-1.45, -1.0]]) {
  const wh = add(new THREE.CylinderGeometry(0.4, 0.4, 0.34, 18), wheelM, x, 0.4, z); wh.rotation.x = Math.PI / 2; WHEELS.push(wh); }
const headM = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xFFF2C0, emissiveIntensity: 1.2 });
const tailM = new THREE.MeshStandardMaterial({ color: 0xff2040, emissive: 0xff2040, emissiveIntensity: 0.9 });
for (const z of [0.65, -0.65]) { add(new THREE.BoxGeometry(0.08, 0.2, 0.42), headM, 2.31, 0.9, z); add(new THREE.BoxGeometry(0.08, 0.2, 0.42), tailM, -2.31, 0.9, z); }
const indM = new THREE.MeshStandardMaterial({ color: 0xFFB020, emissive: 0xFFA000, emissiveIntensity: 0 });
for (const [x, z] of [[2.25, 0.92], [2.25, -0.92], [-2.25, 0.92], [-2.25, -0.92]]) add(new THREE.BoxGeometry(0.2, 0.16, 0.2), indM, x, 1.0, z);
car.scale.setScalar(CS);
// weak points shown in Focus: red rings around the wheels and the fuel cap
const weakM = new THREE.MeshBasicMaterial({ color: 0xFF3B3B, transparent: true, opacity: 0, depthTest: false });
const WEAK = [[1.45, 0.4, -1.2], [-1.45, 0.4, -1.2], [-1.6, 1.0, -1.02]].map(([x, y, z], i) => {
  const r = new THREE.Mesh(new THREE.TorusGeometry(i === 2 ? 0.28 : 0.6, 0.07, 8, 28), weakM.clone()); r.position.set(x, y, z); r.renderOrder = 5; car.add(r); return r; });
// ---- driving: constant speed, frozen while the hood-slide happens (pure function of t)
const V = 7;
function stopW(t) { const a = K.l7 - 0.4, b = K.l8 - 0.2; if (t < a - 0.8 || t > b + 0.8) return 0;
  if (t < a) return (t - (a - 0.8)) / 0.8; if (t > b) return 1 - (t - b) / 0.8; return 1; }
function carX(t) { let x = -140, dt = 1 / 60; for (let s = 0; s < t; s += dt) x += V * (1 - stopW(s)) * Math.min(dt, t - s); return x; }
// ---- the destination marker
const wp = new THREE.Group(); scene.add(wp);
const wpM = new THREE.MeshStandardMaterial({ color: 0xFF3D8B, emissive: 0xFF3D8B, emissiveIntensity: 0.6 });
const cone = new THREE.Mesh(new THREE.ConeGeometry(1.6, 4, 4), wpM); cone.rotation.x = Math.PI; cone.position.y = 6; wp.add(cone);
const wring = new THREE.Mesh(new THREE.RingGeometry(2.4, 3.2, 40), new THREE.MeshBasicMaterial({ color: 0xFFC94A, side: THREE.DoubleSide })); wring.rotation.x = -Math.PI / 2; wring.position.y = 0.15; wp.add(wring);
// ---- the runner (hood slide)
const man = new THREE.Group(); scene.add(man);
const shirt = new THREE.MeshStandardMaterial({ color: 0x2EE6D6, roughness: 0.6 }), pants = new THREE.MeshStandardMaterial({ color: 0x2A1A4A }), skin = new THREE.MeshStandardMaterial({ color: 0xC98B6B });
const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.2, 0.9, 10), pants); leg.position.y = 0.45; man.add(leg);
const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.24, 0.75, 10), shirt); torso.position.y = 1.27; man.add(torso);
const head = new THREE.Mesh(new THREE.SphereGeometry(0.22, 14, 10), skin); head.position.y = 1.85; man.add(head);
const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.1, 14), new THREE.MeshStandardMaterial({ color: 0xFFC94A })); cap.position.y = 2.03; man.add(cap);
man.scale.setScalar(CS); man.visible = false;
"""

keys_js = r"""
// camera keys as offsets from the car: [time, eye offset, look offset]
const keys = [
  [0, [22, 6, -20], [0, 2.2, 0]],
  [K.l1 - 0.2, [14, 4.5, -14], [0, 2.2, 0]],
  [K.l1 + 0.7, [-14, 24, -34], [26, 0, 4]],
  [K.l2 - 0.1, [-12, 22, -32], [30, 0, 4]],
  [K.l2 + 0.6, [-17, 4.2, -8], [8, 2.4, 0]],
  [K.l3 - 0.05, [-15, 4.6, -9], [8, 2.4, 0]],
  [K.l3, [0, 30, 150], [0, 46, -260]],
  [K.l4 - 0.05, [0, 32, 158], [0, 48, -260]],
  [K.l4, [-14, 4.4, -10], [1, 1.8, 0]],
  [K.l4 + 0.6, [-13, 4, -9], [1, 1.8, 0]],
  [K.l5 - 0.1, [-12, 4, -10], [1, 1.8, 0]],
  [K.l5 + 0.5, [3, 4.5, -14], [0, 2.6, 0]],
  [K.l6 - 0.1, [1, 4.5, -14], [0, 2.6, 0]],
  [K.l6 + 0.6, [10, 8, -24], [0, 4, 6]],
  [K.l7 - 0.1, [8, 8, -24], [0, 4, 6]],
  [K.l7 + 0.6, [15, 5, -12], [2, 1.8, 1]],
  [K.l8 - 0.1, [14, 5.2, -13], [2, 1.8, 1]],
  [K.l8 + 0.6, [-10, 7, -17], [0, 1.8, 0]],
  [K.l10 - 0.05, [10, 6.5, -17], [0, 1.8, 0]],
  [K.l10, [-20, 34, 160], [0, 50, -260]],
  [K.l12 - 0.05, [20, 32, 156], [0, 48, -260]],
  [K.l12, [-6, 16, -30], [4, 1.5, 4]],
  [K.pereza - 0.6, [20, 6, -19], [0, 2.2, 0]],
  [DUR, [22, 6, -20], [0, 2.2, 0]],
];
"""

render_js = r"""
  const pinL = (id, x, y, z, o) => { pin(id, x, y, z, o); const el = tags[id]; el.style.top = Math.max(parseFloat(el.style.top), 900).toFixed(1) + "px"; };
  const cx = carX(t);
  car.position.set(cx, 0, ZR);
  { const [p, l] = camAt(t); cam.position.set(cx + p[0], p[1], ZR + p[2]); cam.lookAt(cx + l[0], l[1], ZR + l[2]); cam.updateMatrixWorld(true); }
  const roll = cx / (0.4 * CS); WHEELS.forEach((wh) => { wh.rotation.y = -roll; });
  // destination marker ahead of the car
  const WPX = carX(K.l1) + 46; wp.position.set(WPX, 0, ZR); wp.visible = t > K.destino - 0.3 && t < K.l2 + 0.2;
  const wpu = eo((t - K.destino + 0.2) / 0.4); wp.scale.setScalar(Math.max(0.01, wpu)); cone.position.y = 6 + Math.sin(t * 4) * 0.6; cone.rotation.y = t * 1.5;
  pinL("tg-dest", WPX, 9, ZR, win(t, K.destino, K.l2 - 0.1));
  pinL("tg-auto", cx, 5, ZR, win(t, K.conduce - 0.1, K.l3 + 0.1));
  // indicators blink from "toca" to the end of line 4
  const blinkOn = t > K.toca4 && t < K.l5 && Math.floor((t - K.toca4) * 2.6) % 2 === 0;
  indM.emissiveIntensity = blinkOn ? 2.2 : 0;
  pinL("tg-radio", cx - 0.5, 5.2, ZR, win(t, K.l5 + 0.3, K.l6 - 0.05));
  document.getElementById("tg-radio-s").textContent = t < K.apagas ? "sonando" : "apagada";
  // hood slide: run in from the sand, slide over the hood, land on the far side
  const hx = cx + 1.5 * CS, t0 = K.corre - 0.1, t1 = K.deslizas - 0.15, t2 = t1 + 0.55, t3 = K.l8 - 0.1;
  man.visible = t > t0 && t < t3;
  if (man.visible) {
    let z, y = 0, lean = 0;
    if (t < t1) { const u = (t - t0) / (t1 - t0); z = -18 + 15.2 * u; man.position.y = Math.abs(Math.sin(u * 18)) * 0.25; lean = -0.15; }
    else if (t < t2) { const u = (t - t1) / (t2 - t1); z = -2.8 + 5.6 * u; y = 1.95 * Math.sin(Math.PI * Math.min(1, u * 1.15)); lean = -1.1 * Math.sin(Math.PI * u); }
    else { const u = Math.min(1, (t - t2) / 0.5); z = 2.8 + 4 * eo(u); }
    man.position.set(hx, y, ZR + z); man.rotation.set(-lean, 0, 0);
  }
  // Focus: weak points pulse in red
  const fo = win(t, K.focus, K.l10, 0.3); const pulse = 1 + 0.18 * Math.sin(t * 9);
  WEAK.forEach((r, i) => { r.material.opacity = 0.95 * win(t, K.debiles - 0.2 + i * 0.12, K.l10, 0.2); r.scale.setScalar(pulse); r.lookAt(cam.position); });
  pinL("tg-weak", cx, 6, ZR, win(t, K.debiles, K.l10 - 0.05));
  document.getElementById("focus").style.opacity = fo.toFixed(3);
  renderer.toneMappingExposure = 1.05 - 0.25 * fo;
"""

def show(sel, t, end, kind="pop"):
    a = (f'tl.fromTo("{sel}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {t});' if kind == "pop" else
         f'tl.fromTo("{sel}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {t});')
    return a + f'\ntl.to("{sel}", {{ opacity: 0, duration: 0.18 }}, {end});'

k = K
ov = [
    'tl.fromTo("#bg-title", { opacity: 1, scale: 1.0 }, { opacity: 1, scale: 1.04, duration: ' + str(k["l1"]) + ', ease: "none" }, 0);',
    f'tl.to("#bg-title", {{ opacity: 0, duration: 0.2 }}, {k["l1"] - 0.15});',
    show("#h1a", k["abajo"] - 0.1, k["l2"] - 0.05),
    f'tl.fromTo("#h1b", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.2)" }}, {k["options"] - 0.1});',
    f'tl.to("#bar-t", {{ y: 150, duration: 0.4, ease: "power2.out" }}, {k["options"]});',
    f'tl.to("#bar-b", {{ y: -150, duration: 0.4, ease: "power2.out" }}, {k["options"]});',
    show("#h2", k["circulo2"] - 0.1, k["l3"] - 0.05),
    f'tl.to("#bar-t", {{ y: 0, duration: 0.35, ease: "power2.in" }}, {k["l3"] - 0.1});',
    f'tl.to("#bar-b", {{ y: 0, duration: 0.35, ease: "power2.in" }}, {k["l3"] - 0.1});',
    show("#bg-6", k["siete"] - 0.15, k["l4"] - 0.1, "up"),
    show("#h4", k["toca4"] - 0.1, k["l5"] - 0.05),
    show("#h5", k["veces"] - 0.15, k["l6"] - 0.05),
    f'tl.fromTo("#phone", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, {k["llamada"] - 0.2});',
    f'tl.to("#phone", {{ x: 8, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }}, {k["llamada"] + 0.1});',
    f'tl.to("#ph-rej", {{ opacity: 1, duration: 0.12 }}, {k["rechazas"] - 0.05});',
    f'tl.to(["#phone .t1", "#phone .t2", "#phone .row"], {{ opacity: 0, duration: 0.12 }}, {k["rechazas"] - 0.05});',
    f'tl.to("#phone", {{ opacity: 0, y: 80, duration: 0.3, ease: "power2.in" }}, {k["l7"] - 0.35});',
    show("#h6", k["circulo6"] - 0.1, k["l7"] - 0.05),
    show("#h7", k["equis"] - 0.1, k["l8"] - 0.05),
    show("#h8", k["joy"] - 0.15, k["l10"] - 0.05),
    show("#h10", k["l10"] + 0.1, k["l11"] + 0.4),
    *[f'tl.fromTo("#h10 .ar:nth-child({i + 1})", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.15, ease: "back.out(2)" }}, {round(k["l10"] + 0.3 + i * 0.22, 3)});' for i in range(4)],
    show("#bg-60", k["sesenta"] - 0.15, k["l11"] - 0.05),
    f'tl.fromTo("#bg-hist", {{ opacity: 0, scale: 1.8, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.18, ease: "power4.out" }}, {k["historia"] - 0.1});',
    f'tl.to("#bg-hist", {{ opacity: 0, duration: 0.2 }}, {k["l12"] - 0.1});',
    f'tl.fromTo("#bg-cta", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {k["l12"]});',
    f'tl.to("#bg-cta", {{ opacity: 0, duration: 0.2 }}, {k["pereza"] - 0.5});',
    f'tl.fromTo("#bg-title", {{ opacity: 0, scale: 1.1 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, {k["pereza"] - 0.3});',
]
# the counter: 1/7 … 7/7, swapped with a little pop at each control
CNT = [(k["l1"], "1/7"), (k["l4"], "2/7"), (k["l5"], "3/7"), (k["l6"], "4/7"), (k["l7"], "5/7"), (k["l8"], "6/7"), (k["l10"], "7/7")]
ov.append(f'tl.fromTo("#cnt", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {k["l1"]});')
for t, txt in CNT[1:]:
    ov.append(f'tl.fromTo("#cnt", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, {t});')
ov.append(f'tl.to("#cnt", {{ opacity: 0, duration: 0.2 }}, {k["l12"] - 0.1});')
overlay_js = "\n".join(ov)
# the counter text is set from render(t), so it is right on any seeked frame
render_js = ("  const CNT = " + str([[t, c] for t, c in CNT]) + ";\n"
             "  { let c = CNT[0][1]; for (const [a, b] of CNT) if (t >= a) c = b; const el = document.getElementById(\"cnt\"); if (el.textContent !== c) el.textContent = c; }\n"
             + render_js)

# ------------------------------------------------------------------ sound
R.sfx(0.05, "subida-1.wav", 0.35)
R.sfx(k["solo"], "pop-1.wav", 0.4)
R.sfx(k["destino"] - 0.2, "pop-2.wav", 0.4)
R.sfx(k["abajo"] - 0.1, "tic.wav", 0.5)
R.sfx(k["options"] - 0.1, "tic.wav", 0.5)
R.sfx(k["options"], "barrido-largo.wav", 0.35)
R.sfx(k["circulo2"] - 0.1, "tic.wav", 0.5)
R.sfx(k["siete"] - 0.15, "pop-1.wav", 0.45)
for key in ("l4", "l5", "l6", "l7", "l8", "l10"):
    R.sfx(k[key] + 0.02, "barrido-1.wav" if key in ("l4", "l6", "l8") else "barrido-2.wav", 0.4)
R.sfx(k["toca4"] - 0.1, "tic.wav", 0.5)
for i in range(4):
    R.sfx(k["toca4"] + i / 1.3, "tic-2.wav", 0.35)
R.sfx(k["veces"] - 0.15, "tic.wav", 0.5)
R.sfx(k["apagas"], "glitch.wav", 0.45)
R.sfx(k["llamada"] - 0.15, "bip.wav", 0.4)
R.sfx(k["llamada"] + 0.45, "bip.wav", 0.4)
R.sfx(k["circulo6"] - 0.1, "tic.wav", 0.5)
R.sfx(k["rechazas"] - 0.05, "pop-2.wav", 0.45)
R.sfx(k["equis"] - 0.1, "tic.wav", 0.5)
R.sfx(k["deslizas"] - 0.15, "barrido-3.wav", 0.45)
R.sfx(k["deslizas"] + 0.4, "golpe.wav", 0.35)
R.sfx(k["joy"] - 0.15, "tic.wav", 0.5)
R.sfx(k["focus"] - 0.05, "subida-2.wav", 0.4)
R.sfx(k["debiles"] - 0.2, "pop-3.wav", 0.4)
for i in range(4):
    R.sfx(k["l10"] + 0.3 + i * 0.22, "tic-1.wav", 0.4)
R.sfx(k["sesenta"] - 0.15, "impacto.wav", 0.45)
R.sfx(k["historia"] - 0.1, "sello.wav", 0.6)
R.sfx(k["l12"], "pop-1.wav", 0.5)
R.sfx(k["pereza"] - 0.3, "barrido-largo.wav", 0.35)

CAPS = [
    "En GTA 6, el coche se conduce solo, y el juego casi no te lo cuenta.",
    "Marca un destino en el mapa, mantén abajo en la cruceta y pulsa Options.",
    "Mantén círculo, y el coche conduce por ti.",
    "Y ese es solo el primero de siete.",
    "Dos: toca izquierda o derecha en la cruceta, y pones los intermitentes.",
    "Tres: toca dos veces izquierda, y apagas la radio al instante.",
    "Cuatro: si te entra una llamada, toca círculo y la rechazas sin sacar el móvil.",
    "Cinco: corre hacia un coche, pulsa equis, y te deslizas por encima del capó.",
    "Seis: aprieta los dos joysticks a la vez, y activas el modo Focus.",
    "Te marca pistas, y hasta los puntos débiles de los vehículos.",
    "Y el último: sí hay trucos. Más de sesenta.",
    "Pero solo se desbloquean cuando terminas la historia.",
    "¿Cuál no conocías? Y si un día te da pereza conducir, recuerda que...",
]
HL = {"solo,", "destino", "options.", "círculo,", "siete.", "intermitentes.", "radio", "rechazas", "capó.", "focus.", "débiles", "trucos.",
      "sesenta.", "historia.", "conocías?", "círculo", "equis,", "dos:", "tres:", "cuatro:", "cinco:", "seis:"}

R.write(R.mundo(body, sets_js, keys_js, render_js, overlay_js, K), R.subs(CAPS, HL))
