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

