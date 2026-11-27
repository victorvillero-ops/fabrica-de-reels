const { spawn } = require("child_process");
const fs = require("fs"), path = require("path");
const WebSocket = require("D:/openwhispr-dev/node_modules/ws");
const bin = "D:/openwhispr-dev/resources/bin/sherpa-onnx-ws-win32-x64.exe";
const dir = path.join(process.env.USERPROFILE, ".cache/openwhispr/parakeet-models/orukeet-v0.1.0");
const port = 6611;
const child = spawn(bin, [`--tokens=${dir}/tokens.txt`, `--encoder=${dir}/encoder.int8.onnx`, `--decoder=${dir}/decoder.int8.onnx`, `--joiner=${dir}/joiner.int8.onnx`, `--port=${port}`, "--num-threads=4", "--num-work-threads=1"]);
let log = ""; child.stderr.on("data", d => log += d); child.stdout.on("data", d => log += d);
const audio = fs.readFileSync(process.argv[2]);
const t0 = Date.now();
function attempt(n) {
  const ws = new WebSocket(`ws://127.0.0.1:${port}`);
  ws.on("error", () => { if (n > 0) setTimeout(() => attempt(n - 1), 500); else { console.error("no conecta\n" + log); child.kill(); } });
  ws.on("open", () => {
    const t1 = Date.now();
    const m = Buffer.alloc(8 + audio.length); m.writeInt32LE(16000, 0); m.writeInt32LE(audio.length, 4); audio.copy(m, 8);
    ws.send(m);
    ws.on("message", d => { const s = d.toString(); let t; try { t = JSON.parse(s).text } catch { t = s } console.log(`TEXTO: ${t}\nCarga del modelo: ${((t1-t0)/1000).toFixed(1)} s · Transcripción: ${((Date.now()-t1)/1000).toFixed(2)} s`); ws.send("Done"); ws.close(); child.kill(); });
  });
}
setTimeout(() => attempt(60), 1000);
