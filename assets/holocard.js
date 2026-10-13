/* 全息闪卡查看器 · 改编自 EverettFish/holo-card-studio（MIT）web-holographic 查看器
   原理：四层纹理（主体/背景/线稿/文字）视差 + 镭射光谱 + Voronoi 星光，正面/金边/背面三材质。
   本馆适配：不依赖 Blender 卡模与四层原图——全部纹理在运行时从单张展品图与人物数据生成，
   支持翻面、自动旋转与 PNG 下载。 */
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

let renderer = null, composer = null, root = null, uniforms = null;
let raf = 0, container = null, auto = false, flipped = false;
let targetX = 0.02, targetY = -0.1, targetZoom = 1, rotX = targetX, rotY = targetY;
let dragging = false, last = { x: 0, y: 0 }, lastTime = 0, elapsed = 0;
let currentCh = null, currentNo = "";

const vertex = `varying vec2 vUv;
void main(){vUv=vec2(uv.x,1.0-uv.y);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`;
const shared = `precision highp float;
varying vec2 vUv;
uniform float uTime,uFoil,uScale,uDepth,uBgDepth,uSafeScale;
uniform vec2 uSafeOffset;
uniform vec3 uView;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
vec3 spectrum(float t){t=fract(t);vec3 pink=vec3(1.,.32,.62),yellow=vec3(1.,.85,.32),blue=vec3(.22,.62,1.);if(t<.35)return mix(pink,yellow,t/.35);if(t<.7)return mix(yellow,blue,(t-.35)/.35);return mix(blue,vec3(1.),(t-.7)/.3);}
vec3 overlay(vec3 b,vec3 f){return mix(2.*b*f,1.-2.*(1.-b)*(1.-f),step(vec3(.5),b));}
float inside(vec2 p){return step(0.,p.x)*step(0.,p.y)*step(p.x,1.)*step(p.y,1.);}
vec2 parallax(vec2 p,float s,float d){return (p-.5)*s+.5+uView.xy/max(abs(uView.z),.35)*d*.14;}
float wave(vec2 p){vec2 a=p+uView.xy*2.4;return .5+.5*sin((a.x*.848-a.y*.530)*6.283*.55+7.*noise(a*1.5));}
float star(vec2 p){vec2 q=p*105.,id=floor(q),f=fract(q);float first=9.,second=9.;for(int y=-1;y<=1;y++){for(int x=-1;x<=1;x++){vec2 g=vec2(float(x),float(y));vec2 o=vec2(hash(id+g),hash(id+g+43.3));float d=length(g+o-f);if(d<first){second=first;first=d;}else second=min(second,d);}}float edge=1.-smoothstep(.01,.035,second-first);float sparse=step(.90,hash(id+8.8));float twinkle=pow(.5+.5*sin(uTime*1.8+hash(id)*30.+uView.x*27.+uView.y*21.),6.);return edge*sparse*twinkle;}
`;
const fragment = shared + `
uniform sampler2D tSubject,tBackground,tText,tLine;
void main(){
 vec2 uv=vUv;
 vec2 su=parallax(uv,uScale,uDepth)*uSafeScale+uSafeOffset;
 vec2 bu=parallax(uv,1.,uBgDepth);
 vec4 sub=texture2D(tSubject,clamp(su,0.,1.));sub.a*=inside(su);
 vec3 bg=texture2D(tBackground,clamp(bu,0.,1.)).rgb;
 float w=wave(uv); vec3 foil=spectrum(w*.8+noise(uv*5.)*.12);
 vec3 subject=mix(sub.rgb,overlay(sub.rgb,foil),uFoil*.28);
 bg=mix(bg,overlay(bg,foil),uFoil*.36);
 vec3 col=mix(bg,subject,sub.a);
 float sweep=pow(max(0.,sin((uv.x*.83+uv.y*.35+uView.x*1.8+uView.y*.9)*6.283)),12.);
 col+=foil*sweep*uFoil*.28;
 float line=1.-smoothstep(.06,.25,texture2D(tLine,clamp(su,0.,1.)).r);
 col+=vec3(1.,.94,.78)*line*inside(su)*sub.a*sweep*uFoil*.22;
 col+=vec3(.66,.86,1.)*star(bu)*uFoil*.65*(1.-sub.a*.7);
 vec4 text=texture2D(tText,uv);col=mix(col,text.rgb,text.a);
 gl_FragColor=vec4(pow(max(col,vec3(0.)),vec3(2.2)),1.);
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
}`;
const edgeFragment = shared + `void main(){vec3 col=mix(vec3(.55,.34,.1),spectrum(wave(vUv)),.65+uFoil*.2);gl_FragColor=vec4(col*.8+.14,1.);
#include <tonemapping_fragment>
#include <colorspace_fragment>
}`;
const backFragment = shared + `uniform sampler2D tBack;
void main(){vec4 art=texture2D(tBack,vec2(1.-vUv.x,vUv.y));vec2 p=vUv-.5;float filigree=.5+.5*sin(length(p*vec2(1.,1.5))*100.+noise(p*15.)*4.);vec3 col=mix(vec3(.025,.042,.064),vec3(.085,.092,.11),filigree*.35);float border=step(.465,max(abs(p.x),abs(p.y)));col=mix(col,spectrum(wave(vUv))*.55,border);col+=spectrum(wave(vUv))*uFoil*.08;col=mix(col,art.rgb,art.a);gl_FragColor=vec4(pow(col,vec3(2.2)),1.);
#include <tonemapping_fragment>
#include <colorspace_fragment>
}`;

/* ---------- 运行时纹理工厂 ---------- */
const LW = 1448, LH = 2048;
function cv(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
function rr(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
function drawCover(ctx, img, W, H) {
  /* 大倍率放大走渐进式：逐级倍增 + high 平滑，显著减少糊化 */
  let src = img, sw = src.width, sh = src.height;
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  while (sw * 2 <= W) {
    const step = cv(sw * 2, sh * 2), sx = step.getContext("2d");
    sx.imageSmoothingEnabled = true; sx.imageSmoothingQuality = "high";
    sx.drawImage(src, 0, 0, sw * 2, sh * 2);
    src = step; sw *= 2; sh *= 2;
  }
  const ir = sw / sh, cr = W / H;
  let dw, dh;
  if (ir > cr) { dh = H; dw = H * ir; } else { dw = W; dh = W / ir; }
  ctx.drawImage(src, (W - dw) / 2, (H - dh) / 2, dw, dh);
}
function loadImg(src) {
  return new Promise((res, rej) => {
    const im = new Image();
    im.crossOrigin = "anonymous";
    im.onload = () => res(im);
    im.onerror = rej;
    im.src = src;
  });
}
function bgTexture(img) {
  const c = cv(LW, LH), x = c.getContext("2d");
  const small = cv(LW / 8, LH / 8), s = small.getContext("2d");
  drawCover(s, img, small.width, small.height);
  x.imageSmoothingEnabled = true;
  x.drawImage(small, 0, 0, LW, LH);           /* 放大即得廉价模糊 */
  x.fillStyle = "rgba(10,10,16,.34)";
  x.fillRect(0, 0, LW, LH);
  return c;
}
function subjectTexture(img) {
  const c = cv(LW, LH), x = c.getContext("2d");
  drawCover(x, img, LW, LH);
  const m = cv(LW, LH), mx = m.getContext("2d");
  try { mx.filter = "blur(30px)"; } catch (e) { /* 老浏览器退化为硬边圆角 */ }
  mx.fillStyle = "#fff";
  rr(mx, LW * 0.05, LH * 0.04, LW * 0.9, LH * 0.92, 90);
  mx.fill();
  x.globalCompositeOperation = "destination-in";
  x.drawImage(m, 0, 0);
  return c;
}
function lineTexture(img) {
  const w = 384, h = Math.round(w * img.height / img.width);
  const small = cv(w, h), s = small.getContext("2d");
  drawCover(s, img, w, h);
  const src = s.getImageData(0, 0, w, h).data;
  const lum = new Float32Array(w * h);
  for (let i = 0; i < w * h; i++)
    lum[i] = 0.299 * src[i * 4] + 0.587 * src[i * 4 + 1] + 0.114 * src[i * 4 + 2];
  const mid = cv(w, h), ox = mid.getContext("2d");
  const od = ox.createImageData(w, h);
  for (let y = 1; y < h - 1; y++)
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const gx = lum[i - w + 1] + 2 * lum[i + 1] + lum[i + w + 1] - lum[i - w - 1] - 2 * lum[i - 1] - lum[i + w - 1];
      const gy = lum[i + w - 1] + 2 * lum[i + w] + lum[i + w + 1] - lum[i - w - 1] - 2 * lum[i - w] - lum[i - w + 1];
      const g = Math.min(255, Math.sqrt(gx * gx + gy * gy));
      const v = g > 52 ? Math.max(0, 255 - g * 1.4) : 0;   /* 边缘白线 */
      od.data[i * 4] = od.data[i * 4 + 1] = od.data[i * 4 + 2] = 255 - v;
      od.data[i * 4 + 3] = 255;
    }
  ox.putImageData(od, 0, 0);
  /* 反相：线稿层需要「白线黑底」；先放大到全尺寸再反相 */
  const inv = cv(LW, LH), ix = inv.getContext("2d");
  ix.filter = "invert(1) blur(1.2px)";
  ix.drawImage(mid, 0, 0, LW, LH);
  return inv;
}
function textTexture(ch, no) {
  const c = cv(LW, LH), x = c.getContext("2d");
  x.textBaseline = "alphabetic";
  x.fillStyle = "rgba(255,244,214,.92)";
  x.font = "600 30px 'Trebuchet MS', sans-serif";
  x.fillText("A N I M E   C H A R A C T E R   M U S E U M", 86, 118);
  x.fillStyle = "#c9a86a";
  x.fillRect(86, 140, 340, 3);
  x.fillStyle = "rgba(255,255,255,.96)";
  x.shadowColor = "rgba(0,0,0,.55)"; x.shadowBlur = 18;
  x.font = "800 118px 'PingFang SC','Microsoft YaHei',sans-serif";
  x.fillText(ch.nameZh, 80, LH - 300);
  x.shadowBlur = 8;
  x.fillStyle = "#e8d9ae";
  x.font = "600 40px 'Trebuchet MS', sans-serif";
  x.fillText((ch.nameEn || "").toUpperCase(), 86, LH - 238);
  x.fillStyle = "rgba(255,244,214,.88)";
  x.font = "500 38px 'PingFang SC','Microsoft YaHei',sans-serif";
  x.fillText(ch.animeZh + " · " + ch.year, 86, LH - 178);
  x.font = "700 44px 'Trebuchet MS', sans-serif";
  x.fillText(no, 86, LH - 96);
  x.textAlign = "right";
  x.font = "500 30px 'PingFang SC','Microsoft YaHei',sans-serif";
  x.fillText("经典动漫人物博物馆", LW - 86, LH - 96);
  return c;
}
function backTexture(ch, no) {
  const c = cv(LW, LH), x = c.getContext("2d");
  x.clearRect(0, 0, LW, LH);
  x.fillStyle = "rgba(255,255,255,.94)";
  x.fillRect(0, 0, LW, LH);
  x.fillStyle = "#0a0a0a";
  x.textAlign = "left";
  x.font = "700 26px 'Trebuchet MS', sans-serif";
  x.fillText("ANIME CHARACTER MUSEUM", 86, 118);
  x.font = "800 92px 'PingFang SC','Microsoft YaHei',sans-serif";
  x.fillText(ch.nameZh, 86, 640);
  x.fillStyle = "#696969";
  x.font = "500 34px 'PingFang SC','Microsoft YaHei',sans-serif";
  x.fillText(ch.animeZh + " · " + ch.year, 86, 720);
  x.font = "600 21px 'Trebuchet MS', sans-serif";
  x.fillText("EDITION " + no + " / 214", 86, LH - 150);
  x.fillText("经典动漫人物博物馆 · SINCE 1980", 86, LH - 110);
  return c;
}

/* ---------- 三维场景 ---------- */
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-5, 5, 7.5, -7.5, 0.1, 100);
camera.position.set(0, 0, 20); camera.lookAt(0, 0, 0);

function ensureInit() {
  if (renderer) return true;
  container = document.getElementById("figure-holo");
  if (!container) return false;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true, powerPreference: "high-performance" });
  } catch (e) { return false; }
  renderer.setClearColor(0xffffff, 1);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;
  container.appendChild(renderer.domElement);
  composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(720, 1000), 0.18, 0.35, 1.0));
  composer.addPass(new OutputPass());
  bindControls();
  new ResizeObserver(resize).observe(container);
  resize();
  return true;
}
function resize() {
  const w = container && container.clientWidth, h = container && container.clientHeight;
  if (!w || !h || !renderer) return;
  const halfH = 7.5 / targetZoom;
  camera.left = -halfH * (w / h); camera.right = halfH * (w / h);
  camera.top = halfH; camera.bottom = -halfH;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  composer.setSize(w, h);
}
function bindControls() {
  container.tabIndex = 0;
  container.addEventListener("pointerdown", (e) => {
    if (e.button !== 0) return;
    dragging = true; auto = false;
    last = { x: e.clientX, y: e.clientY };
    container.setPointerCapture(e.pointerId);
  });
  container.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    const base = flipped ? Math.PI : 0;
    targetY = THREE.MathUtils.clamp(targetY + (e.clientX - last.x) * 0.006, base - 0.65, base + 0.65);
    targetX = THREE.MathUtils.clamp(targetX + (e.clientY - last.y) * 0.005, -0.43, 0.43);
    last = { x: e.clientX, y: e.clientY };
  });
  const up = () => { dragging = false; };
  container.addEventListener("pointerup", up);
  container.addEventListener("pointercancel", up);
  container.addEventListener("wheel", (e) => {
    e.preventDefault();
    targetZoom = THREE.MathUtils.clamp(targetZoom - e.deltaY * 0.001, 0.8, 1.2);
    resize();
  }, { passive: false });
  /* 鼠标移入：暂停自动展示，把控制权交给用户；移出：恢复自动旋转 */
  container.addEventListener("pointerenter", () => {
    auto = false;
    if (flipped) { flipped = false; targetY = rotY % (Math.PI * 2); }
  });
  container.addEventListener("pointerleave", () => {
    dragging = false;
    auto = true;
    flipped = false;
  });
}
function roundedShape(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}
function buildCard() {
  if (root) { scene.remove(root); }
  root = new THREE.Group();
  const W = 10, H = 14.1, R = 0.55, D = 0.42;
  const frontMat = new THREE.ShaderMaterial({ uniforms, vertexShader: vertex, fragmentShader: fragment });
  const backMat = new THREE.ShaderMaterial({ uniforms, vertexShader: vertex, fragmentShader: backFragment });
  const goldMat = new THREE.MeshBasicMaterial({ color: 0xbfa26b });
  const shape = roundedShape(W, H, R);
  const frontGeo = new THREE.ShapeGeometry(shape, 24);
  const backGeo = new THREE.ShapeGeometry(shape, 24);
  /* ShapeGeometry 的 UV 是原始坐标，需归一化到 0..1 供着色器采样 */
  for (const g of [frontGeo, backGeo]) {
    const uv = g.attributes.uv;
    for (let i = 0; i < uv.count; i++)
      uv.setXY(i, (uv.getX(i) + W / 2) / W, (H / 2 - uv.getY(i)) / H);
    uv.needsUpdate = true;
  }
  const front = new THREE.Mesh(frontGeo, frontMat);
  front.position.z = D / 2 + 0.01;
  const back = new THREE.Mesh(backGeo, backMat);
  back.position.z = -(D / 2 + 0.01);
  back.rotation.y = Math.PI;
  const core = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: D, bevelEnabled: false, curveSegments: 24 }), goldMat);
  core.position.z = -D / 2;
  root.add(front, back, core);
  scene.add(root);
}
function tex(c) { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.NoColorSpace; t.anisotropy = 4; return t; }
function animate(now) {
  raf = requestAnimationFrame(animate);
  const dt = Math.min((now - lastTime) / 1000, 0.1) || 0;
  lastTime = now;
  if (!document.hidden) elapsed += dt;
  if (auto) {
    targetY = Math.sin(elapsed * 0.65) * 0.38;
    targetX = Math.sin(elapsed * 0.85) * 0.12;
  }
  const ease = 1 - Math.exp(-dt * 8);
  rotX += (targetX - rotX) * ease;
  rotY += (targetY - rotY) * ease;
  if (root) { root.rotation.set(rotX, rotY, 0); root.updateMatrixWorld(true); }
  uniforms.uView.value.copy(camera.position)
    .applyMatrix4(new THREE.Matrix4().copy(root ? root.matrixWorld : new THREE.Matrix4()).invert())
    .normalize();
  uniforms.uTime.value = elapsed;
  composer.render();
}

async function open(imgUrl, ch, no) {
  currentCh = ch; currentNo = no;
  if (!ensureInit()) return false;
  cancelAnimationFrame(raf);
  container.hidden = false;
  requestAnimationFrame(resize);
  /* 传入的可能是展示缩略图路径——纹理必须用原尺寸图保证导出清晰度 */
  const fullUrl = String(imgUrl).replace(/^exhibits\/thumb\//, "exhibits/").replace(/\.webp$/, ".jpg");
  const img = await loadImg(fullUrl);
  uniforms = {
    tSubject: { value: tex(subjectTexture(img)) },
    tBackground: { value: tex(bgTexture(img)) },
    tText: { value: tex(textTexture(ch, no)) },
    tLine: { value: tex(lineTexture(img)) },
    tBack: { value: tex(backTexture(ch, no)) },
    uTime: { value: 0 },
    uView: { value: new THREE.Vector3(0, 0, 1) },
    uFoil: { value: 0.65 },
    uScale: { value: 0.94 },
    uDepth: { value: 0.42 },
    uBgDepth: { value: -0.25 },
    uSafeScale: { value: 1.02 },
    uSafeOffset: { value: new THREE.Vector2(0, 0) },
  };
  buildCard();
  auto = true;                    /* 打开即自动旋转展示 */
  flipped = false;
  targetX = 0.02; targetY = -0.1; targetZoom = 1;
  cancelAnimationFrame(raf);
  lastTime = 0;
  raf = requestAnimationFrame(animate);
  return true;
}
function close() {
  cancelAnimationFrame(raf); raf = 0;
  if (root) { scene.remove(root); root = null; }
}
function download() {
  try {
    /* 超采样导出：临时把渲染分辨率放大 ~2.2 倍，文字与镭射纹理都会锐利得多 */
    const w = container.clientWidth, h = container.clientHeight;
    const scale = Math.min(8, Math.max(2.5, 2100 / w));
    const oldRatio = renderer.getPixelRatio();
    renderer.setPixelRatio(1);
    renderer.setSize(Math.round(w * scale), Math.round(h * scale), false);
    composer.setSize(Math.round(w * scale), Math.round(h * scale));
    composer.render();
    const a = document.createElement("a");
    a.download = (currentCh ? currentCh.nameZh : "card") + "-" + currentNo + "-holocard.png";
    a.href = renderer.domElement.toDataURL("image/png");
    a.click();
    renderer.setPixelRatio(oldRatio);
    resize();
  } catch (e) { console.error(e); }
}
window.HoloCard = {
  open,
  close,
  download,
  flip: () => { flipped = !flipped; auto = false; targetY = flipped ? Math.PI : 0; targetX = 0; },
  autoToggle: () => { auto = !auto; return auto; },
};
