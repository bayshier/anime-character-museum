/* 3D 展台查看器 · Three.js 实时生成亚克力立牌（二阶段 2a）
   约定：若 models/<id>.glb 存在（二阶段 2b AI 图生 3D 产物），将优先加载 GLB。 */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

let renderer = null, scene = null, camera = null, controls = null;
let group = null, raf = 0, container = null, texLoader = null;

function ensureInit() {
  if (renderer) return true;
  container = document.getElementById("archive-3d");
  if (!container || !window.WebGLRenderingContext) return false;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
  } catch (e) {
    return false;
  }
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(38, 1, 0.1, 60);
  camera.position.set(0, 0.6, 3.4);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.enablePan = false;
  controls.minDistance = 1.8;
  controls.maxDistance = 7;
  controls.target.set(0, -0.1, 0);

  scene.add(new THREE.AmbientLight(0xffffff, 1.1));
  const key = new THREE.DirectionalLight(0xfff2d9, 1.6);
  key.position.set(2, 3, 4);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xcbeeea, 0.7);
  fill.position.set(-3, 1, -2);
  scene.add(fill);

  texLoader = new THREE.TextureLoader();
  texLoader.crossOrigin = "anonymous";
  texLoader.onError = () => { /* 贴图失败：由调用方回退平面 */ };

  const resize = () => {
    if (!container || container.hidden) return;
    const w = container.clientWidth || 300, h = container.clientHeight || 420;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(container);
  resize();
  return true;
}

function roundedRectShape(w, h, r) {
  const s = new THREE.Shape();
  const x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y);
  s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r);
  s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h);
  s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r);
  s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}

function disposeGroup() {
  if (!group) return;
  group.traverse((o) => {
    if (o.geometry) o.geometry.dispose();
    if (o.material) {
      (Array.isArray(o.material) ? o.material : [o.material]).forEach((mt) => {
        if (mt.map) mt.map.dispose();
        mt.dispose();
      });
    }
  });
  scene.remove(group);
  group = null;
}

function buildStandee(texture, imgAspect) {
  disposeGroup();
  group = new THREE.Group();

  const w = 1.5;
  const h = Math.min(2.6, Math.max(1.5, w * imgAspect));
  const shape = roundedRectShape(w, h, Math.min(0.12, w * 0.09));
  const geo = new THREE.ExtrudeGeometry(shape, {
    depth: 0.05, bevelEnabled: true, bevelThickness: 0.012,
    bevelSize: 0.012, bevelSegments: 2, curveSegments: 24,
  });
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 4;
  /* ExtrudeGeometry 的 UV 等于顶点坐标：把贴图矩阵从形状空间映射回 0..1 */
  texture.wrapS = THREE.ClampToEdgeWrapping;
  texture.wrapT = THREE.ClampToEdgeWrapping;
  texture.repeat.set(1 / w, 1 / h);
  texture.offset.set(0.5, 0.5);

  const front = new THREE.MeshBasicMaterial({ map: texture });
  const side = new THREE.MeshBasicMaterial({ color: 0xefe3c8 });
  const standee = new THREE.Mesh(geo, [front, side]);
  group.add(standee);

  /* 底座：黄铜椭圆台 + 连接块 */
  const baseMat = new THREE.MeshStandardMaterial({ color: 0xc9a86a, roughness: 0.35, metalness: 0.55 });
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.68, 0.09, 40), baseMat);
  base.scale.z = 0.42;
  base.position.y = -h / 2 - 0.045;
  group.add(base);

  const linkMat = new THREE.MeshStandardMaterial({ color: 0xb5975c, roughness: 0.4, metalness: 0.5 });
  const link = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.1, 0.07), linkMat);
  link.position.y = -h / 2 + 0.02;
  link.position.z = -0.01;
  group.add(link);

  scene.add(group);
}

function animate() {
  raf = requestAnimationFrame(animate);
  if (group) group.rotation.y += 0.0035;   /* 缓慢自动旋转 */
  controls.update();
  renderer.render(scene, camera);
}

async function tryLoadGlb(url) {
  /* 二阶段 2b：GLB 存在即优先（GLTFLoader 由调用方按需 import，此处先探测文件） */
  try {
    const head = await fetch(url, { method: "HEAD" });
    return head.ok;
  } catch (e) {
    return false;
  }
}

async function open(imgUrl, exhibitId) {
  if (!ensureInit()) return false;
  cancelAnimationFrame(raf);
  container.hidden = false;
  requestAnimationFrame(() => {
    container.dispatchEvent(new Event("viewer-resize"));
  });

  const glbUrl = `models/${exhibitId}.glb`;
  const hasGlb = await tryLoadGlb(glbUrl);
  if (hasGlb) {
    /* 2b 产物优先：动态引入 GLTFLoader 加载真 3D 模型 */
    const { GLTFLoader } = await import("three/addons/loaders/GLTFLoader.js");
    const loader = new GLTFLoader();
    loader.load(glbUrl, (gltf) => {
      disposeGroup();
      group = gltf.scene;
      const box = new THREE.Box3().setFromObject(group);
      const size = box.getSize(new THREE.Vector3());
      const scale = 2.2 / Math.max(size.x, size.y, size.z);
      group.scale.setScalar(scale);
      group.position.y = -0.2;
      scene.add(group);
      animate();
    });
    return true;
  }

  /* 2a：实时生成亚克力立牌 */
  texLoader.load(imgUrl, (tex) => {
    const img = tex.image;
    buildStandee(tex, img.height / img.width);
    cancelAnimationFrame(raf);
    animate();
  }, undefined, () => { /* 贴图加载失败：清空让调用方回退 */ disposeGroup(); container.hidden = true; });
  return true;
}

function close() {
  cancelAnimationFrame(raf);
  raf = 0;
  disposeGroup();
}

window.Viewer3D = { open, close };
