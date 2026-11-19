/* 3D world for the film: every frame is a pure function of timeline time (hf-seek). */
(function () {
  const W = 1080;
  const H = 1920;
  const bgCanvas = document.getElementById("w3d-bg");
  const fgCanvas = document.getElementById("w3d-fg");
  const rBg = new THREE.WebGLRenderer({
    canvas: bgCanvas,
    antialias: true,
    preserveDrawingBuffer: true,
  });
  const rFg = new THREE.WebGLRenderer({
    canvas: fgCanvas,
    antialias: true,
    alpha: true,
    preserveDrawingBuffer: true,
  });
  for (const r of [rBg, rFg]) {
    r.setSize(W, H, false);
    r.toneMapping = THREE.ACESFilmicToneMapping;
    r.toneMappingExposure = 1.5;
  }
  rBg.shadowMap.enabled = true;
  rBg.shadowMap.type = THREE.PCFSoftShadowMap;
  rFg.setClearColor(0x000000, 0);

  const cam = new THREE.PerspectiveCamera(38, W / H, 0.1, 200);
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const clamp01 = (x) => Math.min(1, Math.max(0, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const seg = (u, a, b) => clamp01((u - a) / (b - a));
  const outCubic = (x) => 1 - Math.pow(1 - clamp01(x), 3);
  const outExpo = (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp01(x)));
  const inOut = (x) => {
    x = clamp01(x);
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  };
  const backOut = (x) => {
    x = clamp01(x);
    const c = 1.9;
    return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2);
  };
  function rand(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const COL = {
    cream: "#eeeed2",
    green: "#769656",
    gold: "#ffc83d",
    red: "#ff5050",
    blue: "#4fb0ff",
    orange: "#ff9a3c",
  };

  /* ---------- pieces ---------- */
  const PROFILE = {
    base: [
      [0, 0],
      [0.4, 0],
      [0.42, 0.06],
      [0.4, 0.12],
      [0.33, 0.16],
      [0.34, 0.24],
      [0.26, 0.3],
    ],
    pawn: [
      [0.14, 0.62],
      [0.12, 0.84],
      [0.22, 0.88],
      [0.22, 0.93],
      [0.1, 0.97],
      [0, 0.97],
    ],
    rook: [
      [0.2, 0.7],
      [0.19, 1.12],
      [0.3, 1.18],
      [0.3, 1.5],
      [0.22, 1.5],
      [0.22, 1.4],
      [0, 1.4],
    ],
    bishop: [
      [0.15, 0.75],
      [0.11, 1.3],
      [0.22, 1.35],
      [0.22, 1.42],
      [0.1, 1.46],
      [0.17, 1.62],
      [0.15, 1.8],
      [0.05, 1.98],
      [0, 2.0],
    ],
    queen: [
      [0.16, 0.85],
      [0.12, 1.6],
      [0.24, 1.66],
      [0.24, 1.74],
      [0.13, 1.78],
      [0.16, 1.95],
      [0.28, 2.2],
      [0.2, 2.2],
      [0.14, 2.12],
      [0, 2.12],
    ],
    king: [
      [0.17, 0.9],
      [0.13, 1.7],
      [0.26, 1.76],
      [0.26, 1.85],
      [0.14, 1.89],
      [0.18, 2.05],
      [0.29, 2.3],
      [0.2, 2.34],
      [0, 2.36],
    ],
  };
  const geoCache = {};
  function pieceGeo(type) {
    if (!geoCache[type]) {
      const pts = PROFILE.base.concat(PROFILE[type]).map((p) => new THREE.Vector2(p[0], p[1]));
      geoCache[type] = new THREE.LatheGeometry(pts, 40);
    }
    return geoCache[type];
  }
  const MAT = {
    white: new THREE.MeshStandardMaterial({ color: 0xf4f1e6, roughness: 0.32, metalness: 0.02 }),
    black: new THREE.MeshStandardMaterial({ color: 0x2a2d36, roughness: 0.28, metalness: 0.05 }),
    gold: new THREE.MeshStandardMaterial({ color: 0xffc83d, roughness: 0.3, metalness: 0.55 }),
  };
  function piece(type, color, scale) {
    const g = new THREE.Group();
    const m = MAT[color];
    const body = new THREE.Mesh(pieceGeo(type), m);
    body.castShadow = true;
    body.receiveShadow = true;
    g.add(body);
    const add = (geo, x, y, z) => {
      const o = new THREE.Mesh(geo, m);
      o.position.set(x, y, z);
      o.castShadow = true;
      g.add(o);
      return o;
    };
    if (type === "pawn") add(new THREE.SphereGeometry(0.21, 24, 16), 0, 1.15, 0);
    if (type === "queen") add(new THREE.SphereGeometry(0.09, 16, 12), 0, 2.22, 0);
    if (type === "bishop") add(new THREE.SphereGeometry(0.06, 12, 8), 0, 2.05, 0);
    if (type === "king") {
      add(new THREE.BoxGeometry(0.09, 0.42, 0.09), 0, 2.56, 0);
      add(new THREE.BoxGeometry(0.3, 0.09, 0.09), 0, 2.6, 0);
    }
    g.scale.setScalar(scale || 1);
    return g;
  }

  /* ---------- textures ---------- */
  function canvasTex(w, h, draw) {
    const c = document.createElement("canvas");
    c.width = w;
    c.height = h;
    const ctx = c.getContext("2d");
    draw(ctx, w, h);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 8;
    t.userData = { canvas: c, ctx: ctx };
    return t;
  }

  const FONT = (px) => "900 " + px + 'px "Nunito", sans-serif';
  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  /* a text label standing in the world; height in world units */
  function label(text, o) {
    o = o || {};
    const px = 180;
    const pad = o.bg ? 50 : 16;
    const probe = document.createElement("canvas").getContext("2d");
    probe.font = FONT(px);
    const tw = Math.ceil(probe.measureText(text).width);
    const w = tw + pad * 2;
    const h = px + pad * 2;
    const t = canvasTex(w, h, (ctx) => {
      if (o.bg) {
        ctx.fillStyle = o.bg;
        roundRect(ctx, 0, 0, w, h, 44);
        ctx.fill();
      }
      ctx.font = FONT(px);
      ctx.textBaseline = "middle";
      ctx.textAlign = "center";
      if (!o.bg) {
        ctx.lineWidth = 22;
        ctx.lineJoin = "round";
        ctx.strokeStyle = "rgba(0,0,0,0.75)";
        ctx.strokeText(text, w / 2, h / 2 + 8);
      }
      ctx.fillStyle = o.color || "#fff";
      ctx.fillText(text, w / 2, h / 2 + 8);
    });
    const height = o.height || 1;
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry((height * w) / h, height),
      new THREE.MeshBasicMaterial({
        map: t,
        transparent: true,
        toneMapped: false,
        fog: false,
        depthWrite: false,
        side: THREE.DoubleSide,
      }),
    );
    m.renderOrder = 5;
    return m;
  }
  function lights(scene, o) {
    const hemi = new THREE.HemisphereLight(o.sky, o.ground, o.hemi);
    const key = new THREE.DirectionalLight(o.keyColor, o.key);
    key.position.copy(o.keyPos);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    const s = o.shadow || 12;
    key.shadow.camera.left = -s;
    key.shadow.camera.right = s;
    key.shadow.camera.top = s;
    key.shadow.camera.bottom = -s;
    key.shadow.camera.far = 80;
    key.shadow.bias = -0.0005;
    key.shadow.radius = 4;
    const rim = new THREE.DirectionalLight(o.rimColor, o.rim);
    rim.position.copy(o.rimPos);
    for (const l of [hemi, key, rim]) {
      l.layers.enableAll();
      scene.add(l);
    }
    scene.add(key.target);
    return { hemi: hemi, key: key, rim: rim };
  }
  function toFg(obj) {
    obj.traverse((o) => o.layers.set(1));
    return obj;
  }
  function dust(scene, count, box, seed) {
    const rnd = rand(seed);
    const base = [];
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) base.push([rnd(), rnd(), rnd(), 0.2 + rnd() * 0.5]);
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const pts = new THREE.Points(
      geo,
      new THREE.PointsMaterial({
        color: 0xcfe4ff,
        size: 0.06,
        transparent: true,
        opacity: 0.55,
        depthWrite: false,
      }),
    );
    scene.add(pts);
    return function (t) {
      for (let i = 0; i < count; i++) {
        const b = base[i];
        pos[i * 3] = box.x0 + b[0] * (box.x1 - box.x0) + Math.sin(t * 0.6 + i) * 0.15;
        pos[i * 3 + 1] = box.y0 + ((b[1] + t * 0.03 * b[3]) % 1) * (box.y1 - box.y0);
        pos[i * 3 + 2] = box.z0 + b[2] * (box.z1 - box.z0);
      }
      geo.attributes.position.needsUpdate = true;
    };
  }

  /* ---------- sets ---------- */
  const SHOTS = [];
  /* a character cut-out that swaps expression art, blinks and settles with a small pop */
  /* face(t): [[time, "expr"], ...]; blinks: times; returns nothing, sets the art for time t */
  function animatePuppet(m, t, face, blinks) {
    let expr = face[0][1];
    let since = 99;
    for (const f of face) {
      if (t >= f[0]) {
        expr = f[1];
        since = t - f[0];
      }
    }
    let blink = false;
    for (const b of blinks) if (t >= b && t < b + 0.11) blink = true;
    const set = m.userData.set;
    const key = m.userData.prefix + "-" + expr;
    const tex = (blink && set[key + "-blink"]) || set[key];
    if (m.material.map !== tex) {
      m.material.map = tex;
      m.material.needsUpdate = true;
    }
    const pop = since < 0.25 ? Math.sin((since / 0.25) * Math.PI) * 0.035 : 0;
    m.scale.set(1 - pop * 0.5, 1 + pop, 1);
    m.rotation.z = Math.sin(t * 1.4) * 0.008;
    const k = m.userData.tint || 0;
    m.material.color.setRGB(1, 1 - 0.18 * k, 1 - 0.18 * k);
  }

  /* ---------- painted plates: every shot is a camera on a painting, with cut-outs and props in front ---------- */
  const PW = 11;
  const PH = 19.6;
  const PZ = -7;
  const PY = 4.9;
  const FULL =
    PH /
    2 /
    Math.tan((40 / 2) * (Math.PI / 180)); /* camera distance that shows the whole plate height */
  function platePt(px, py, z) {
    return V((px / 1116 - 0.5) * PW, PY + (0.5 - py / 2000) * PH, z == null ? PZ : z);
  }
  /* look straight at plate pixel (px, py) at a zoom (1 = whole plate); dx/dy shift the camera for parallax */
  function camPlate(px, py, zoom, dx, dy) {
    const hw = (PH * (1080 / 1920)) / 2 / zoom;
    const hh = PH / 2 / zoom;
    const c = platePt(px, py);
    c.x = Math.min(PW / 2 - hw, Math.max(-PW / 2 + hw, c.x));
    c.y = Math.min(PY + PH / 2 - hh, Math.max(PY - PH / 2 + hh, c.y));
    const d = FULL / zoom;
    cam.position.set(c.x + (dx || 0), c.y + (dy || 0), PZ + d);
    cam.fov = 40;
    cam.updateProjectionMatrix();
    cam.lookAt(c.x + (dx || 0) * 0.15, c.y + (dy || 0) * 0.15, PZ);
  }
  function plateScene(tex, o) {
    o = o || {};
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(o.bg || 0x0a0f1e);
    lights(scene, {
      sky: 0xcfe0ff,
      ground: 0x2a2018,
      hemi: 1.0,
      keyColor: o.key || 0xfff0d8,
      key: 2.2,
      keyPos: V(3, 12, 10),
      rimColor: o.rim || 0x6aa8ff,
      rim: 1.2,
      rimPos: V(-6, 6, -4),
      shadow: 10,
    });
    const back = new THREE.Mesh(
      new THREE.PlaneGeometry(PW, PH),
      new THREE.MeshBasicMaterial({ map: tex, toneMapped: false, fog: false }),
    );
    back.position.set(0, PY, PZ);
    scene.add(back);
    const d =
      o.dust === false
        ? () => {}
        : dust(scene, 140, { x0: -5, x1: 5, y0: -3, y1: 13, z0: -5, z1: 8 }, o.seed || 5);
    return { scene: scene, back: back, dust: d };
  }
  /* a cut-out character; first = the key whose art sets the aspect */
  function cutout(set, prefix, first, height) {
    const t0 = set[prefix + "-" + first];
    const aspect = t0.image.width / t0.image.height;
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(height * aspect, height),
      new THREE.MeshBasicMaterial({
        map: t0,
        transparent: true,
        alphaTest: 0.5,
        toneMapped: false,
        fog: false,
      }),
    );
    m.geometry.translate(0, height / 2, 0);
    m.userData = { set: set, prefix: prefix, tint: 0 };
    return m;
  }
  /* stand a cut-out so that, seen from the whole-plate camera, its feet sit on plate pixel (px, py) and it is hPx tall */
  function standOnPlate(m, px, py, z) {
    const C = V(0, PY, PZ + FULL);
    const P = platePt(px, py);
    const k = (C.z - z) / (C.z - PZ);
    m.position.copy(C.clone().add(P.sub(C).multiplyScalar(k)));
    m.position.z = z;
    return k;
  }
  function makeCutout(set, prefix, first, px, py, hPx, z) {
    const C = V(0, PY, PZ + FULL);
    const k = (C.z - z) / (C.z - PZ);
    const m = cutout(set, prefix, first, (hPx / 2000) * PH * k);
    standOnPlate(m, px, py, z);
    return m;
  }
  function blob(scene, m, w) {
    const tex = canvasTex(256, 128, (ctx, cw, ch) => {
      const g = ctx.createRadialGradient(cw / 2, ch / 2, 4, cw / 2, ch / 2, cw / 2);
      g.addColorStop(0, "rgba(0,0,0,0.5)");
      g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, cw, ch);
    });
    const b = new THREE.Mesh(
      new THREE.PlaneGeometry(w, w * 0.32),
      new THREE.MeshBasicMaterial({
        map: tex,
        transparent: true,
        depthWrite: false,
        toneMapped: false,
        fog: false,
      }),
    );
    b.position.set(m.position.x, m.position.y + 0.02, m.position.z + 0.05);
    scene.add(b);
    return b;
  }
  /* a screen glued onto the plate: draw(ctx, w, h, u) every frame */
  function plateScreen(scene, x0, y0, x1, y1, draw) {
    const tex = canvasTex(
      1024,
      Math.round((1024 * (y1 - y0) * PH) / 2000 / (((x1 - x0) * PW) / 1116)),
      () => {},
    );
    const w = ((x1 - x0) / 1116) * PW;
    const h = ((y1 - y0) / 2000) * PH;
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ map: tex, toneMapped: false, fog: false }),
    );
    m.position.copy(platePt((x0 + x1) / 2, (y0 + y1) / 2, PZ + 0.01));
    scene.add(m);
    return function (u) {
      const c = tex.userData.canvas;
      draw(tex.userData.ctx, c.width, c.height, u);
      tex.needsUpdate = true;
    };
  }
  function screenText(ctx, w, h, lines) {
    ctx.fillStyle = "#0b0f1c";
    ctx.fillRect(0, 0, w, h);
    const g = ctx.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, w * 0.7);
    g.addColorStop(0, "rgba(80,120,255,0.18)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (const l of lines) {
      ctx.globalAlpha = l.a == null ? 1 : l.a;
      ctx.font = FONT(l.size);
      ctx.fillStyle = l.color;
      ctx.fillText(l.text, w / 2 + (l.x || 0), l.y);
    }
    ctx.globalAlpha = 1;
  }
  function tintPlate(p, k, r, g, b) {
    p.back.material.color.setRGB(lerp(1, r, k), lerp(1, g, k), lerp(1, b, k));
  }

  function build(tex) {
    const P = tex.plates;
    const MG = tex.magnus;
    const shot = (t0, t1, scene, update) =>
      SHOTS.push({ t0: t0, t1: t1, scene: scene, update: update });

    /* A/B 0.00–3.35 · throne room: Magnus smug, then the room turns red on "#2?" */
    (function () {
      const s = plateScene(P["throne-room"], { seed: 3 });
      const mag = makeCutout(MG, "st", "smug", 558, 1900, 980, 2.4);
      s.scene.add(mag);
      blob(s.scene, mag, 2.4);
      const fgA = toFg(piece("pawn", "white", 1.1));
      fgA.position.set(-2.6, -1.6, 9);
      const fgB = toFg(piece("rook", "black", 1.1));
      fgB.position.set(2.8, -1.6, 9.5);
      s.scene.add(fgA, fgB);
      shot(0, 1.75, s.scene, (u, t) => {
        camPlate(558, 1180, lerp(1.08, 1.25, outCubic(u / 1.75)), 0, 0);
        animatePuppet(mag, t, [[0, "smug"]], [0.95]);
        tintPlate(s, 0, 1, 1, 1);
        mag.userData.tint = 0;
        s.dust(t);
      });
      shot(1.75, 3.35, s.scene, (u, t) => {
        camPlate(558, 1023, lerp(1.92, 2.05, outCubic(u / 1.6)), -0.3, 0);
        animatePuppet(
          mag,
          t,
          [
            [0, "smug"],
            [1.82, "worried"],
          ],
          [2.95],
        );
        const r = seg(u, 0.05, 0.3);
        tintPlate(s, r, 1, 0.62, 0.62);
        mag.userData.tint = r * 0.6;
        s.dust(t);
      });
    })();

    /* C 3.35–5.45 · the room: push from the wall calendar to the "DEC 1" sign */
    (function () {
      const s = plateScene(P["room"], { seed: 8, rim: 0xffb070 });
      const fg = toFg(piece("king", "white", 0.9));
      fg.position.set(-2.4, -0.4, 8.5);
      s.scene.add(fg);
      shot(3.35, 5.45, s.scene, (u, t) => {
        const k = inOut(u / 2.1);
        camPlate(lerp(330, 498, k), lerp(980, 870, k), lerp(1.55, 2.4, k), lerp(0.4, -0.2, k), 0);
        s.dust(t);
      });
    })();

    /* D 5.45–6.70 and S 48.70–50.80 · the studio screen */
    (function () {
      const s = plateScene(P["studio"], { seed: 12, rim: 0xb070ff });
      let mode = "gap5";
      const draw = plateScreen(s.scene, 188, 563, 958, 1027, (ctx, w, h, u) => {
        if (mode === "gap5") {
          const pop = backOut(seg(u, 0.05, 0.45));
          screenText(ctx, w, h, [
            {
              text: "5.4",
              size: Math.round(260 * Math.max(0.01, pop)),
              color: "#ffc83d",
              y: h * 0.45,
            },
            { text: "POINTS LEFT", size: 60, color: "#ffffff", y: h * 0.82, a: seg(u, 0.35, 0.6) },
          ]);
          return;
        }
        /* live ratings: two bars, the gap lands on "five point four" */
        ctx.fillStyle = "#0b0f1c";
        ctx.fillRect(0, 0, w, h);
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.font = FONT(34);
        ctx.fillStyle = "rgba(255,255,255,0.7)";
        ctx.fillText("LIVE RATINGS · NOV 2026", w / 2, 46);
        const base = h - 40;
        const grow = outExpo(seg(u, 0.1, 0.7));
        const hm = 330 * grow;
        const hf = 330 * (8.6 / 14) * grow;
        const bars = [
          { x: w * 0.3, hgt: hm, col: "#4fb0ff", name: "CARLSEN", val: "2804.0" },
          { x: w * 0.7, hgt: hf, col: "#ff9a3c", name: "CARUANA", val: "2798.6" },
        ];
        for (const b of bars) {
          ctx.fillStyle = b.col;
          roundRect(ctx, b.x - 90, base - b.hgt, 180, b.hgt, 18);
          ctx.fill();
          ctx.font = FONT(44);
          ctx.fillStyle = b.col;
          ctx.fillText(b.val, b.x, base - b.hgt - 34);
          ctx.font = FONT(30);
          ctx.fillStyle = "#ffffff";
          ctx.fillText(b.name, b.x, base - b.hgt - 80);
        }
        const g = seg(u, 0.85, 1.1);
        if (g > 0) {
          ctx.globalAlpha = g;
          ctx.setLineDash([16, 12]);
          ctx.strokeStyle = "#ffc83d";
          ctx.lineWidth = 8;
          ctx.beginPath();
          ctx.moveTo(w * 0.3 + 100, base - hm);
          ctx.lineTo(w * 0.7 + 100, base - hm);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.font = FONT(120);
          ctx.fillStyle = "#ffc83d";
          ctx.fillText("5.4", w / 2, base - hm + 70);
          ctx.globalAlpha = 1;
        }
      });
      shot(5.45, 6.7, s.scene, (u, t) => {
        mode = "gap5";
        draw(u);
        camPlate(572, 1000, lerp(1.6, 1.8, outCubic(u / 1.25)), 0, 0);
        s.dust(t);
      });
      shot(48.7, 50.8, s.scene, (u, t) => {
        mode = "bars";
        draw(u);
        camPlate(572, 1020, lerp(1.5, 1.65, outCubic(u / 2.1)), 0.2, 0);
        s.dust(t);
      });
    })();

    /* E/F 6.70–12.95 · hall of fame: Magnus stands, the years fly down the corridor; then the camera runs on */
    (function () {
      const s = plateScene(P["hall-of-fame"], { seed: 21 });
      const mag = makeCutout(MG, "st", "smug", 800, 1900, 820, 2.6);
      s.scene.add(mag);
      blob(s.scene, mag, 2.2);
      const years = [];
      for (let i = 0; i < 16; i++) {
        const l = label(String(2011 + i), { color: i === 0 ? COL.gold : "#ffffff", height: 0.9 });
        s.scene.add(l);
        years.push(l);
      }
      shot(6.7, 10.4, s.scene, (u, t) => {
        camPlate(590, 1150, lerp(1.25, 1.55, outCubic(u / 3.7)), 0, 0);
        mag.visible = true;
        animatePuppet(mag, t, [[0, "smug"]], [1.5 + 6.7]);
        years.forEach((l, i) => {
          const start = 0.35 + i * 0.2;
          const k = seg(u, start, start + 0.75);
          l.visible = k > 0 && k < 1;
          const side = i % 2 ? 1 : -1;
          l.position.set(
            lerp(-0.6 + 0.5 * side, -2.6 + 0.8 * side, k * k),
            lerp(4.6, 5.4, k),
            lerp(PZ + 1.2, 11, inCubicLocal(k)),
          );
          l.quaternion.copy(cam.quaternion);
        });
        s.dust(t);
      });
      shot(10.4, 12.95, s.scene, (u, t) => {
        const k = inOut(u / 2.55);
        camPlate(590, 1000, lerp(1.6, 2.6, k), 0, 0);
        mag.visible = false;
        for (const l of years) l.visible = false;
        s.dust(t);
      });
    })();

    /* G 12.95–16.10 · two towers in the corridor: Kasparov 117 months, Carlsen 183 */
    (function () {
      const s = plateScene(P["hall-of-fame"], { seed: 22 });
      const stripe = (a, b) => {
        const t = canvasTex(8, 64, (ctx) => {
          ctx.fillStyle = a;
          ctx.fillRect(0, 0, 8, 64);
          ctx.fillStyle = b;
          ctx.fillRect(0, 0, 8, 10);
        });
        t.wrapT = THREE.RepeatWrapping;
        return t;
      };
      function tower(x, months, a, b, kingColor, name, col) {
        const h = months * 0.026;
        const t = stripe(a, b);
        t.repeat.set(1, months / 6);
        const m = new THREE.Mesh(
          new THREE.CylinderGeometry(0.55, 0.55, h, 40),
          new THREE.MeshStandardMaterial({ map: t, roughness: 0.4 }),
        );
        m.castShadow = true;
        const g = new THREE.Group();
        g.position.set(x, -1.2, 1.5);
        g.add(m);
        const k = piece("king", kingColor, 0.6);
        g.add(k);
        const l1 = label(name, { color: col, height: 0.36 });
        const l2 = label(months + " MO", { color: "#ffffff", height: 0.46 });
        g.add(l1, l2);
        s.scene.add(g);
        return function (f) {
          const hh = Math.max(0.02, h * f);
          m.scale.y = hh / h;
          m.position.y = hh / 2;
          k.position.y = hh;
          l1.position.set(0, hh + 2.45, 0);
          l2.position.set(0, hh + 1.95, 0);
          l1.quaternion.copy(cam.quaternion);
          l2.quaternion.copy(cam.quaternion);
        };
      }
      const kas = tower(-0.95, 117, "#8d97ad", "#69728a", "black", "KASPAROV", "#c4ccdd");
      const car = tower(0.95, 183, "#4fb0ff", "#2f86d6", "white", "CARLSEN", COL.blue);
      shot(12.95, 16.1, s.scene, (u, t) => {
        const fk = outCubic(seg(u, 0.1, 1.2));
        const fc = (117 / 183) * fk + (1 - 117 / 183) * inOut(seg(u, 1.7, 2.7));
        kas(fk);
        car(fc);
        camPlate(590, lerp(1350, 1150, inOut(u / 3.15)), 1.15, lerp(-0.3, 0.3, inOut(u / 3.15)), 0);
        s.dust(t);
      });
    })();

    /* plain painted shots: a slow move on the picture */
    function plain(name, t0, t1, from, to, seed) {
      const s = plateScene(P[name], { seed: seed });
      shot(t0, t1, s.scene, (u, t) => {
        const k = inOut(u / (t1 - t0));
        camPlate(lerp(from[0], to[0], k), lerp(from[1], to[1], k), lerp(from[2], to[2], k), 0, 0);
        s.dust(t);
      });
      return s;
    }
    /* H 16.10–19.55 · Caruana: start on him, open out */
    plain("img08-rivals", 16.1, 19.55, [760, 900, 2.0], [700, 1000, 1.45], 31);
    /* I/J 19.55–24.50 · London 2018 */
    plain("london-stage", 19.55, 22.45, [558, 1200, 1.0], [558, 1420, 1.35], 32);
    plain("img02-london2018", 22.45, 24.5, [560, 1050, 1.12], [560, 1020, 1.3], 33);

    /* K/L 24.50–31.40 · game 12: Magnus at the board, then the tiebreak */
    (function () {
      const s = plateScene(P["london-table-blur"], { seed: 41, dust: false });
      const mag = makeCutout(MG, "sit", "focus", 540, 2120, 1350, 3.0);
      s.scene.add(mag);
      shot(24.5, 28.71, s.scene, (u, t) => {
        camPlate(
          558,
          1150,
          lerp(1.06, 1.16, inOut(u / 4.21)),
          lerp(0.2, -0.15, inOut(u / 4.21)),
          0,
        );
        animatePuppet(
          mag,
          t,
          [
            [0, "focus"],
            [27.03, "offer"],
          ],
          [],
        );
      });
      const s2 = plateScene(P["london-stage"], { seed: 42 });
      const win = makeCutout(MG, "st", "win", 700, 2100, 1000, 3.2);
      s2.scene.add(win);
      shot(28.71, 31.4, s2.scene, (u, t) => {
        camPlate(558, 1300, lerp(1.0, 1.15, outCubic(u / 2.69)), 0, 0);
        animatePuppet(win, t, [[0, "win"]], [30.4]);
        s2.dust(t);
      });
    })();

    /* M 31.40–37.50 · Fabi's peak and never #1 */
    plain("img03-podium", 31.4, 34.0, [300, 1100, 1.7], [330, 1150, 1.45], 51);
    plain("podium", 34.0, 35.8, [558, 1400, 1.1], [558, 1450, 1.3], 52);
    plain("img03-podium", 35.8, 37.5, [300, 980, 2.1], [300, 980, 2.3], 53);

    /* N/O/P/Q 37.50–46.10 · Budapest: the hall, the time scramble, the loss, the shock */
    (function () {
      const s = plateScene(P["budapest-hall"], { seed: 61, key: 0xffd9a0 });
      const fg = toFg(piece("king", "black", 1.0));
      fg.position.set(2.2, -1.2, 9.2);
      s.scene.add(fg);
      shot(37.5, 40.0, s.scene, (u, t) => {
        camPlate(558, lerp(1000, 1200, inOut(u / 2.5)), lerp(1.0, 1.25, inOut(u / 2.5)), 0, 0);
        s.dust(t);
      });
      const s2 = plateScene(P["budapest-close-blur"], { seed: 62, dust: false });
      const mag = makeCutout(MG, "sit", "stress", 600, 1960, 1500, 3.0);
      s2.scene.add(mag);
      shot(40.0, 41.4, s2.scene, (u, t) => {
        camPlate(558, 1150, lerp(1.0, 1.12, u / 1.4), Math.sin(t * 40) * 0.02, 0);
        animatePuppet(mag, t, [[0, "stress"]], []);
      });
      plain("budapest-close", 41.4, 43.8, [560, 1560, 2.1], [560, 1540, 2.5], 63);
      const s3 = plateScene(P["budapest-close-blur"], { seed: 64, dust: false });
      const sh = makeCutout(MG, "st", "shock", 600, 2400, 1500, 3.4);
      s3.scene.add(sh);
      shot(43.8, 46.1, s3.scene, (u, t) => {
        const jolt = u > 0.65 && u < 0.95 ? Math.sin(u * 90) * 0.04 : 0;
        camPlate(558, 1200, lerp(1.25, 1.12, outExpo(u / 0.6)), jolt, 0);
        animatePuppet(sh, t, [[0, "shock"]], []);
      });
    })();

    /* R 46.10–48.70 · Fabi: five wins */
    plain("img06-fabi", 46.1, 48.7, [760, 1000, 1.6], [740, 980, 1.85], 71);

    /* T 50.80–53.40 · the "DEC 1" sign */
    (function () {
      const s = plateScene(P["room"], { seed: 81, rim: 0xffb070 });
      shot(50.8, 53.4, s.scene, (u, t) => {
        camPlate(498, 860, lerp(1.6, 3.0, inOut(u / 2.6)), 0, 0);
        s.dust(t);
      });
    })();

    /* U 53.40–57.80 · the empty throne, the crown on the floor */
    plain("throne-fallen", 53.4, 55.7, [558, 1150, 1.0], [558, 1200, 1.25], 91);
    plain("throne-fallen", 55.7, 57.8, [690, 1700, 2.6], [690, 1720, 2.9], 92);
    /* V 57.80–61.60 · the rivals */
    plain("img08-rivals", 57.8, 61.6, [540, 1150, 1.0], [540, 1050, 1.2], 93);
    /* W 61.60–66.40 · end card over the throne room */
    plain("throne-room", 61.6, 66.4, [558, 1150, 1.15], [558, 1150, 1.25], 94);
  }
  function inCubicLocal(x) {
    x = clamp01(x);
    return x * x * x;
  }

  /* ---------- driver ---------- */
  let ready = false;
  let lastT = 0;
  function renderAt(t) {
    lastT = t;
    if (!ready) return;
    let shot = SHOTS[SHOTS.length - 1];
    for (const s of SHOTS) {
      if (t >= s.t0 && t < s.t1) {
        shot = s;
        break;
      }
    }
    shot.update(Math.min(t, shot.t1) - shot.t0, t);
    cam.layers.set(0);
    rBg.render(shot.scene, cam);
    cam.layers.set(1);
    const bgc = shot.scene.background;
    const fog = shot.scene.fog;
    shot.scene.background = null;
    rFg.render(shot.scene, cam);
    shot.scene.background = bgc;
    shot.scene.fog = fog;
  }
  function loadTex(url) {
    return new Promise((resolve, reject) => {
      new THREE.TextureLoader().load(
        url,
        (t) => {
          t.colorSpace = THREE.SRGBColorSpace;
          t.anisotropy = 8;
          resolve(t);
        },
        undefined,
        reject,
      );
    });
  }
  const MAGNUS_ART = [
    "st-smug",
    "st-smug-blink",
    "st-worried",
    "st-worried-blink",
    "st-stern",
    "st-stern-blink",
    "st-think",
    "st-think-blink",
    "st-win",
    "st-win-blink",
    "st-shock",
    "sit-focus",
    "sit-offer",
    "sit-stress",
  ];
  function loadSet(dir, names) {
    return Promise.all(names.map((n) => loadTex(dir + n + ".webp"))).then((ts) => {
      const o = {};
      names.forEach((n, i) => (o[n] = ts[i]));
      return o;
    });
  }
  const PLATES = [
    "throne-room",
    "room",
    "studio",
    "hall-of-fame",
    "img08-rivals",
    "london-stage",
    "london-stage-blur",
    "img02-london2018",
    "london-table-blur",
    "img03-podium",
    "podium",
    "budapest-hall",
    "budapest-close",
    "budapest-close-blur",
    "img06-fabi",
    "throne-fallen",
  ];
  const buildPromise = Promise.all([
    document.fonts.load('900 100px "Nunito"'),
    loadSet("assets/chars/magnus/", MAGNUS_ART),
    Promise.all(PLATES.map((n) => loadTex("assets/bg/" + n + ".jpg"))),
  ]).then((r) => {
    const plates = {};
    PLATES.forEach((n, i) => (plates[n] = r[2][i]));
    build({ magnus: r[1], plates: plates });
    ready = true;
    renderAt(lastT);
  });
  window.__hf = window.__hf || {};
  window.__hf.buildReady = window.__hf.buildReady || {};
  window.__hf.buildReady["world3d"] = buildPromise;
  window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
  renderAt(0);
})();
