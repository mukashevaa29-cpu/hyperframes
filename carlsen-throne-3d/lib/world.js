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
  function checkerTex(n, a, b) {
    const t = canvasTex(n * 64, n * 64, (ctx) => {
      for (let i = 0; i < n; i++)
        for (let j = 0; j < n; j++) {
          ctx.fillStyle = (i + j) % 2 ? b : a;
          ctx.fillRect(i * 64, j * 64, 64, 64);
        }
    });
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
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
  function board(n, sq) {
    const g = new THREE.Group();
    const tex = checkerTex(n, COL.cream, COL.green);
    tex.magFilter = THREE.NearestFilter;
    const top = new THREE.Mesh(
      new THREE.PlaneGeometry(n * sq, n * sq),
      new THREE.MeshStandardMaterial({ map: tex, roughness: 0.55 }),
    );
    top.rotation.x = -Math.PI / 2;
    top.receiveShadow = true;
    g.add(top);
    const frame = new THREE.Mesh(
      new THREE.BoxGeometry(n * sq + 0.7, 0.5, n * sq + 0.7),
      new THREE.MeshStandardMaterial({ color: 0x4a2f1b, roughness: 0.6 }),
    );
    frame.position.y = -0.26;
    frame.receiveShadow = true;
    g.add(frame);
    return g;
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
  function faceCam(obj) {
    obj.rotation.y = Math.atan2(cam.position.x - obj.position.x, cam.position.z - obj.position.z);
  }
  function setCam(p, look, fov) {
    cam.position.copy(p);
    cam.fov = fov || 38;
    cam.updateProjectionMatrix();
    cam.lookAt(look);
  }
  const mix = (a, b, k) => a.clone().lerp(b, k);

  /* ---------- sets ---------- */
  const SHOTS = [];
  /* a character cut-out that swaps expression art, blinks and settles with a small pop */
  function puppet(set, prefix, height) {
    const any = set[prefix + "-smug"] || set[Object.keys(set)[0]];
    const aspect = any.image.width / any.image.height;
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(height * aspect, height),
      new THREE.MeshBasicMaterial({
        map: any,
        transparent: true,
        alphaTest: 0.5,
        toneMapped: false,
      }),
    );
    m.geometry.translate(0, height / 2, 0);
    m.userData = { set: set, prefix: prefix, tint: 0 };
    return m;
  }
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

  function buildHall(tex) {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x05080f);
    scene.fog = new THREE.Fog(0x05080f, 14, 46);
    const L = lights(scene, {
      sky: 0x6f8fd8,
      ground: 0x0a0d18,
      hemi: 0.55,
      keyColor: 0xfff0d8,
      key: 2.4,
      keyPos: V(4, 14, 8),
      rimColor: 0x4f8dff,
      rim: 1.6,
      rimPos: V(-6, 6, -10),
      shadow: 16,
    });
    const ftex = checkerTex(8, "#1c2b4d", "#0d1730");
    ftex.repeat.set(10, 10);
    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(160, 160),
      new THREE.MeshStandardMaterial({ map: ftex, roughness: 0.35, metalness: 0.2 }),
    );
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);
    const dais = new THREE.Mesh(
      new THREE.CylinderGeometry(3.2, 3.6, 0.4, 48),
      new THREE.MeshStandardMaterial({ color: 0x1a2440, roughness: 0.4 }),
    );
    dais.position.y = 0.2;
    dais.receiveShadow = true;
    scene.add(dais);
    const types = ["king", "queen", "rook", "bishop", "rook", "queen"];
    for (let i = 0; i < 6; i++) {
      for (const side of [-1, 1]) {
        const p = piece(types[i], side < 0 ? "white" : "black", 3.4);
        p.position.set(side * 6.2, 0, 3 - i * 5.5);
        scene.add(p);
      }
    }
    /* the giant white king stands behind him: the throne he is defending */
    const statue = piece("king", "white", 2.6);
    statue.position.set(0, 0.4, -2.2);
    scene.add(statue);
    const throne = puppet(tex.magnus, "st", 3.7);
    throne.position.set(0, 0.4, 0.4);
    scene.add(throne);
    const cones = [];
    for (const x of [-2.6, 0, 2.6]) {
      const c = new THREE.Mesh(
        new THREE.ConeGeometry(3.4, 18, 48, 1, true),
        new THREE.MeshBasicMaterial({
          color: 0x5aa0ff,
          transparent: true,
          opacity: 0.045,
          blending: THREE.AdditiveBlending,
          depthWrite: false,
          side: THREE.DoubleSide,
        }),
      );
      c.position.set(x, 8, -0.5);
      c.rotation.z = x * -0.05;
      scene.add(c);
      cones.push(c);
    }
    const fgA = toFg(piece("pawn", "white", 1.3));
    const fgB = toFg(piece("rook", "black", 1.3));
    scene.add(fgA, fgB);
    const dustUpdate = dust(scene, 220, { x0: -6, x1: 6, y0: 0.5, y1: 11, z0: -6, z1: 9 }, 7);
    const blue = new THREE.Color(0x5aa0ff);
    const red = new THREE.Color(0xff4040);
    const rimBlue = new THREE.Color(0x4f8dff);
    function mood(k) {
      for (const c of cones) c.material.color.copy(blue).lerp(red, k);
      L.rim.color.copy(rimBlue).lerp(red, k);
      throne.userData.tint = k;
    }
    return { scene: scene, throne: throne, fgA: fgA, fgB: fgB, dust: dustUpdate, mood: mood };
  }

  function build(tex) {
    const hall = buildHall(tex);

    /* 1 · 0.00–1.75 · wide push-in on the throne */
    SHOTS.push({
      t0: 0,
      t1: 1.75,
      scene: hall.scene,
      update(u, t) {
        const k = outCubic(u / 1.75);
        hall.mood(0);
        hall.fgA.position.set(-2.0, 0, 10.4);
        hall.fgB.position.set(2.2, 0, 11.0);
        setCam(mix(V(0, 1.4, 16), V(0, 2.2, 10.5), k), V(0, lerp(2.4, 2.9, k), 0), 40);
        hall.dust(t);
        faceCam(hall.throne);
        animatePuppet(hall.throne, t, [[0, "smug"]], [0.95]);
      },
    });
    /* 2 · 1.75–3.35 · low side angle, the hall turns red on "#2?" */
    SHOTS.push({
      t0: 1.75,
      t1: 3.35,
      scene: hall.scene,
      update(u, t) {
        const k = outCubic(u / 1.6);
        hall.mood(seg(u, 0.05, 0.3));
        hall.fgA.position.set(-4.3, 0, 6.2);
        hall.fgB.position.set(30, 0, 0);
        setCam(mix(V(-1.6, 3.0, 6.4), V(-1.1, 3.3, 5.0), k), V(0.0, 3.55, 0.4), 36);
        hall.dust(t);
        faceCam(hall.throne);
        animatePuppet(
          hall.throne,
          t,
          [
            [0, "smug"],
            [1.82, "worried"],
          ],
          [2.95],
        );
      },
    });

    /* 3 · 3.35–5.45 · calendar flips to December 1 */
    (function () {
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x3a2616);
      scene.fog = new THREE.Fog(0x3a2616, 12, 34);
      lights(scene, {
        sky: 0xffe2b8,
        ground: 0x1a120a,
        hemi: 0.7,
        keyColor: 0xffe6c0,
        key: 2.6,
        keyPos: V(-5, 9, 6),
        rimColor: 0xff9a3c,
        rim: 1.2,
        rimPos: V(6, 4, -6),
        shadow: 8,
      });
      const b = board(8, 1);
      scene.add(b);
      const layout = [
        ["rook", "black", -3.5, -3.5],
        ["queen", "black", -0.5, -3.5],
        ["king", "black", 0.5, -3.5],
        ["bishop", "black", 2.5, -2.5],
        ["pawn", "black", -2.5, -1.5],
        ["pawn", "white", 2.5, 1.5],
        ["pawn", "white", -3.5, 2.5],
        ["rook", "white", 3.5, 3.5],
      ];
      for (const p of layout) {
        const o = piece(p[0], p[1], 0.8);
        o.position.set(p[2], 0, p[3]);
        scene.add(o);
      }
      const fg = toFg(piece("king", "white", 0.8));
      fg.position.set(-1.9, 0, 5.4);
      scene.add(fg);
      const cal = new THREE.Group();
      cal.position.set(0, 0, -0.4);
      scene.add(cal);
      const stand = new THREE.Mesh(
        new THREE.BoxGeometry(2.7, 3.2, 0.25),
        new THREE.MeshStandardMaterial({ color: 0x2a2018, roughness: 0.7 }),
      );
      stand.position.set(0, 1.75, -0.2);
      stand.rotation.x = -0.12;
      stand.castShadow = true;
      cal.add(stand);
      const pages = [];
      const defs = [
        ["DEC", "1", COL.gold, "#16130a"],
        ["NOV", "29", COL.red, "#fff"],
        ["NOV", "22", COL.red, "#fff"],
        ["NOV", "15", COL.red, "#fff"],
      ];
      defs.forEach((d, i) => {
        const t = canvasTex(512, 600, (ctx, w, h) => {
          ctx.fillStyle = "#f6f3ea";
          roundRect(ctx, 0, 0, w, h, 36);
          ctx.fill();
          ctx.save();
          roundRect(ctx, 0, 0, w, h, 36);
          ctx.clip();
          ctx.fillStyle = d[2];
          ctx.fillRect(0, 0, w, 160);
          ctx.restore();
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillStyle = d[3];
          ctx.font = FONT(100);
          ctx.fillText(d[0], w / 2, 88);
          ctx.fillStyle = "#1b1b24";
          ctx.font = FONT(330);
          ctx.fillText(d[1], w / 2, 390);
        });
        const pivot = new THREE.Group();
        pivot.position.set(0, 3.25, 0.02 + i * 0.012);
        const m = new THREE.Mesh(
          new THREE.PlaneGeometry(2.4, 2.81),
          new THREE.MeshBasicMaterial({ map: t, toneMapped: false, side: THREE.DoubleSide }),
        );
        m.position.y = -1.405;
        pivot.add(m);
        pivot.rotation.x = -0.12;
        cal.add(pivot);
        pages.push(pivot);
      });
      SHOTS.push({
        t0: 3.35,
        t1: 5.45,
        scene: scene,
        update(u) {
          const k = outCubic(u / 2.1);
          for (let i = 1; i <= 3; i++) {
            const f = inOut(seg(u, 0.22 + (3 - i) * 0.2, 0.42 + (3 - i) * 0.2));
            pages[i].rotation.x = -0.12 - f * 2.9;
            pages[i].visible = f < 0.98;
          }
          const pop = backOut(seg(u, 0.84, 1.14));
          pages[0].scale.setScalar(1 + 0.06 * pop);
          setCam(mix(V(3.6, 2.4, 11.5), V(1.3, 2.3, 8.8), k), V(0, 1.35, 0), 46);
        },
      });
    })();

    /* 4 · 5.45–6.70 · two kings, five points apart */
    (function () {
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x14284f);
      scene.fog = new THREE.Fog(0x14284f, 10, 30);
      lights(scene, {
        sky: 0x9cc0ff,
        ground: 0x0a1020,
        hemi: 0.7,
        keyColor: 0xffffff,
        key: 2.4,
        keyPos: V(3, 9, 6),
        rimColor: 0xff9a3c,
        rim: 1.6,
        rimPos: V(-6, 3, -5),
        shadow: 7,
      });
      scene.add(board(8, 1));
      const wk = piece("king", "white", 0.85);
      wk.position.set(-0.6, 0, 0.5);
      const bk = piece("king", "black", 0.85);
      scene.add(wk, bk);
      const gap = label("5.4", { color: COL.gold, height: 0.7 });
      gap.position.set(0.0, 2.75, 0.5);
      scene.add(gap);
      const fg = toFg(piece("pawn", "white", 0.85));
      fg.position.set(-1.9, 0, 5.2);
      scene.add(fg);
      SHOTS.push({
        t0: 5.45,
        t1: 6.7,
        scene: scene,
        update(u) {
          const s = outExpo(seg(u, 0.0, 0.45));
          bk.position.set(lerp(3.5, 0.6, s), 0, 0.5);
          gap.scale.setScalar(backOut(seg(u, 0.12, 0.42)));
          gap.visible = u > 0.12;
          const k = outCubic(u / 1.25);
          setCam(mix(V(1.4, 1.0, 9.2), V(0.4, 1.2, 7.4), k), V(0, 0.95, 0.5), 44);
          gap.quaternion.copy(cam.quaternion);
        },
      });
    })();

    /* 5 · 6.70–10.40 · the reign: the king runs past fifteen years */
    (function () {
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x12264d);
      scene.fog = new THREE.Fog(0x12264d, 12, 38);
      const L = lights(scene, {
        sky: 0x86b4ff,
        ground: 0x0a1020,
        hemi: 0.75,
        keyColor: 0xfff2dc,
        key: 2.3,
        keyPos: V(5, 12, 8),
        rimColor: 0x4fb0ff,
        rim: 1.5,
        rimPos: V(-8, 5, -8),
        shadow: 10,
      });
      const tex = checkerTex(8, COL.cream, COL.green);
      tex.magFilter = THREE.NearestFilter;
      tex.repeat.set(7, 0.5);
      const lane = new THREE.Mesh(
        new THREE.PlaneGeometry(56, 4),
        new THREE.MeshStandardMaterial({ map: tex, roughness: 0.55 }),
      );
      lane.rotation.x = -Math.PI / 2;
      lane.position.set(24, 0, 0);
      lane.receiveShadow = true;
      scene.add(lane);
      const under = new THREE.Mesh(
        new THREE.BoxGeometry(56.6, 0.5, 4.6),
        new THREE.MeshStandardMaterial({ color: 0x4a2f1b, roughness: 0.6 }),
      );
      under.position.set(24, -0.26, 0);
      scene.add(under);
      const years = [];
      for (let i = 0; i < 16; i++) {
        const y = label(String(2011 + i), { color: i === 0 ? COL.gold : "#ffffff", height: 0.8 });
        y.position.set(1.5 + i * 3, 3.6, -2.4);
        scene.add(y);
        years.push(y);
        const fallen = piece(["king", "queen", "rook", "bishop"][i % 4], "black", 0.8);
        fallen.rotation.z = Math.PI / 2;
        fallen.rotation.y = 0.5 + i * 1.3;
        fallen.position.set(3.2 + i * 3, 0.33, 1.25 + (i % 2) * 0.35);
        scene.add(fallen);
      }
      const king = piece("king", "white", 0.95);
      scene.add(king);
      const crown = label("#1", { color: "#16130a", bg: COL.gold, height: 0.42 });
      scene.add(crown);
      const fgs = [];
      for (let i = 0; i < 9; i++) {
        const f = toFg(piece(i % 2 ? "pawn" : "bishop", "white", 0.9));
        f.position.set(2 + i * 5.6, 0, 5.6);
        scene.add(f);
        fgs.push(f);
      }
      SHOTS.push({
        t0: 6.7,
        t1: 10.4,
        scene: scene,
        update(u) {
          /* slow by "July 2011", then the years fly on "never gave it back" */
          const x = 1.5 + 1.2 * outCubic(seg(u, 0, 1.9)) + 43.5 * inOut(seg(u, 2.1, 3.7));
          king.position.set(x, 0, 0);
          king.rotation.y = x * 0.5;
          crown.position.set(x, 3.05, 0);
          L.key.position.set(x + 5, 12, 8);
          L.key.target.position.set(x, 0, 0);
          const back = seg(u, 2.1, 3.7);
          setCam(
            V(x + lerp(2.0, 3.4, back), lerp(1.6, 2.2, back), lerp(11.5, 13.5, back)),
            V(x + 0.5, 1.2, -0.6),
            44,
          );
          crown.quaternion.copy(cam.quaternion);
          for (const y of years) y.quaternion.copy(cam.quaternion);
        },
      });
    })();

    /* 6 · 10.40–12.95 · the scoreboard counts the days */
    (function () {
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x05080f);
      scene.fog = new THREE.Fog(0x05080f, 12, 40);
      lights(scene, {
        sky: 0x6f8fd8,
        ground: 0x0a0d18,
        hemi: 0.6,
        keyColor: 0xfff0d8,
        key: 2.2,
        keyPos: V(3, 12, 8),
        rimColor: 0xffc83d,
        rim: 1.4,
        rimPos: V(-6, 8, -6),
        shadow: 9,
      });
      const b = board(8, 1);
      scene.add(b);
      const king = piece("king", "white", 1);
      scene.add(king);
      for (let i = 0; i < 8; i++) {
        const p = piece("pawn", "white", 0.8);
        const a = (i / 8) * Math.PI * 2;
        p.position.set(Math.cos(a) * 2.6, 0, Math.sin(a) * 2.6);
        scene.add(p);
      }
      const sbTex = canvasTex(1024, 512, () => {});
      const sb = new THREE.Mesh(new THREE.BoxGeometry(6.4, 3.2, 0.4), [
        new THREE.MeshStandardMaterial({ color: 0x11141d }),
        new THREE.MeshStandardMaterial({ color: 0x11141d }),
        new THREE.MeshStandardMaterial({ color: 0x11141d }),
        new THREE.MeshStandardMaterial({ color: 0x11141d }),
        new THREE.MeshBasicMaterial({ map: sbTex, toneMapped: false }),
        new THREE.MeshStandardMaterial({ color: 0x11141d }),
      ]);
      sb.position.set(0, 7.4, -1.5);
      sb.rotation.x = 0.22;
      scene.add(sb);
      for (const x of [-3, 3]) {
        const c = new THREE.Mesh(
          new THREE.CylinderGeometry(0.04, 0.04, 8, 8),
          new THREE.MeshStandardMaterial({ color: 0x555b6b }),
        );
        c.position.set(x, 12.2, -1.5);
        scene.add(c);
      }
      const fg = toFg(piece("rook", "black", 1));
      fg.position.set(2.6, 0, 9.5);
      scene.add(fg);
      const dustUpdate = dust(scene, 140, { x0: -6, x1: 6, y0: 0.5, y1: 12, z0: -6, z1: 6 }, 11);
      function drawBoard(n) {
        const ctx = sbTex.userData.ctx;
        ctx.fillStyle = "#0b0e16";
        ctx.fillRect(0, 0, 1024, 512);
        ctx.strokeStyle = "#ffc83d";
        ctx.lineWidth = 14;
        ctx.strokeRect(14, 14, 996, 484);
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "#ffc83d";
        ctx.font = FONT(250);
        ctx.fillText(n.toLocaleString("en-US") + (n >= 5600 ? "+" : ""), 512, 215);
        ctx.fillStyle = "#ffffff";
        ctx.font = FONT(72);
        ctx.fillText("DAYS AT WORLD #1", 512, 410);
        sbTex.needsUpdate = true;
      }
      SHOTS.push({
        t0: 10.4,
        t1: 12.95,
        scene: scene,
        update(u, t) {
          drawBoard(Math.round(5600 * outCubic(seg(u, 0.1, 1.75))));
          const k = outCubic(u / 2.55);
          setCam(mix(V(-2.2, 0.9, 19), V(-0.8, 1.1, 15.5), k), V(0, lerp(4.4, 4.9, k), 0), 46);
          dustUpdate(t);
        },
      });
    })();

    /* 7 · 12.95–16.10 · longer than Kasparov, longer than anyone */
    (function () {
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x12264d);
      scene.fog = new THREE.Fog(0x12264d, 16, 48);
      lights(scene, {
        sky: 0x86b4ff,
        ground: 0x0a1020,
        hemi: 0.8,
        keyColor: 0xfff2dc,
        key: 2.3,
        keyPos: V(5, 14, 9),
        rimColor: 0x4fb0ff,
        rim: 1.4,
        rimPos: V(-8, 6, -8),
        shadow: 12,
      });
      scene.add(board(8, 1));
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
        const h = months * 0.042;
        const t = stripe(a, b);
        t.repeat.set(1, months / 6);
        const m = new THREE.Mesh(
          new THREE.CylinderGeometry(0.85, 0.85, h, 40),
          new THREE.MeshStandardMaterial({ map: t, roughness: 0.4 }),
        );
        m.castShadow = true;
        const g = new THREE.Group();
        g.position.set(x, 0, 0);
        g.add(m);
        const k = piece("king", kingColor, 0.9);
        g.add(k);
        const l1 = label(name, { color: col, height: 0.5 });
        const l2 = label(months + " MO", { color: "#ffffff", height: 0.62 });
        g.add(l1, l2);
        scene.add(g);
        return function (f) {
          const hh = Math.max(0.02, h * f);
          m.scale.y = hh / h;
          m.position.y = hh / 2;
          k.position.y = hh;
          l1.position.set(0, hh + 3.75, 0);
          l2.position.set(0, hh + 3.1, 0);
          l1.quaternion.copy(cam.quaternion);
          l2.quaternion.copy(cam.quaternion);
          l2.material.map.userData.months = months;
          return hh;
        };
      }
      const kas = tower(-1.7, 117, "#8d97ad", "#69728a", "black", "KASPAROV", "#c4ccdd");
      const car = tower(1.7, 183, "#4fb0ff", "#2f86d6", "white", "CARLSEN", COL.blue);
      const fg = toFg(piece("pawn", "black", 0.9));
      fg.position.set(-2.6, 0, 9);
      scene.add(fg);
      SHOTS.push({
        t0: 12.95,
        t1: 16.1,
        scene: scene,
        update(u) {
          const fk = outCubic(seg(u, 0.1, 1.2));
          const fc =
            fk * (117 / 183) * 0 +
            (117 / 183) * outCubic(seg(u, 0.1, 1.2)) +
            (1 - 117 / 183) * inOut(seg(u, 1.7, 2.7));
          const top = Math.max(117 * 0.042 * fk, 183 * 0.042 * fc);
          const camY = 1.6 + top * 0.6;
          setCam(V(lerp(-1.2, 1.2, inOut(u / 3.15)), camY, 21), V(0, camY + 1.4, 0), 44);
          kas(fk);
          car(fc);
        },
      });
    })();
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
  const buildPromise = Promise.all([
    document.fonts.load('900 100px "Nunito"'),
    loadTex("assets/cut/throne.webp"),
    loadTex("assets/cut/rivals.webp"),
    loadTex("assets/cut/shock.webp"),
    loadSet("assets/chars/magnus/", MAGNUS_ART),
  ]).then((r) => {
    build({ throne: r[1], rivals: r[2], shock: r[3], magnus: r[4] });
    ready = true;
    renderAt(lastT);
  });
  window.__hf = window.__hf || {};
  window.__hf.buildReady = window.__hf.buildReady || {};
  window.__hf.buildReady["world3d"] = buildPromise;
  window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
  renderAt(0);
})();
