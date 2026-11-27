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
  const sx = Math.min(Math.max((v3.x * 0.5 + 0.5) * 1080, 200), 880), sy = Math.min(Math.max((-v3.y * 0.5 + 0.5) * 1920, 690), 1230);
  el.style.left = sx.toFixed(1) + "px"; el.style.top = sy.toFixed(1) + "px"; el.style.opacity = (v3.z < 1 ? op : 0).toFixed(3); }
const win = (t, a, b, f) => clamp01(Math.min((t - a) / (f || 0.25), (b - t) / (f || 0.25)));

