/* Procedural cartoon characters: built from primitives, posed from a plain state object,
   so every frame is a pure function of time. window.HFChars.make(spec) -> { root, pose(state) } */
(function () {
  const std = (color, rough) =>
    new THREE.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.6 : rough });
  function cap(r, len, mat) {
    const m = new THREE.Mesh(new THREE.CapsuleGeometry(r, len, 8, 20), mat);
    m.castShadow = true;
    m.receiveShadow = true;
    return m;
  }
  function sph(r, mat, sx, sy, sz) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(r, 40, 28), mat);
    m.scale.set(sx || 1, sy || 1, sz || 1);
    m.castShadow = true;
    return m;
  }
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
  /* limb: a pivot at the joint, the segment hangs down -y */
  function limb(r, len, mat) {
    const pivot = new THREE.Group();
    const seg = cap(r, len, mat);
    seg.position.y = -len / 2;
    pivot.add(seg);
    const end = new THREE.Group();
    end.position.y = -len;
    pivot.add(end);
    return { pivot: pivot, end: end };
  }

  function make(spec) {
    const M = {
      skin: std(spec.skin || 0xf0c4a0, 0.55),
      hair: std(spec.hair, 0.7),
      top: std(spec.top, 0.85),
      top2: std(spec.top2 || spec.top, 0.85),
      pants: std(spec.pants, 0.8),
      shoe: std(spec.shoe, 0.5),
      eyeW: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.25 }),
      eyeP: new THREE.MeshStandardMaterial({ color: spec.iris || 0x3a2416, roughness: 0.2 }),
      dark: new THREE.MeshStandardMaterial({ color: 0x3a1a14, roughness: 0.5 }),
      brow: std(spec.brow || spec.hair, 0.7),
      white: std(0xf5f5f2, 0.6),
      glass: new THREE.MeshStandardMaterial({ color: 0x2a2e36, roughness: 0.3, metalness: 0.3 }),
    };
    const root = new THREE.Group();
    const hips = new THREE.Group();
    hips.position.y = 0.92;
    root.add(hips);

    /* torso */
    const torso = new THREE.Group();
    hips.add(torso);
    const body = cap(0.2, 0.36, M.top);
    body.scale.set(1, 1, 0.72);
    body.position.y = 0.26;
    torso.add(body);
    if (spec.outfit === "hoodie") {
      const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.1, 0.02), M.top2);
      pocket.position.set(0, 0.16, 0.145);
      torso.add(pocket);
      const hood = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.045, 12, 28), M.top2);
      hood.rotation.x = Math.PI / 2 - 0.25;
      hood.position.set(0, 0.55, -0.02);
      torso.add(hood);
      for (const x of [-0.035, 0.035]) {
        const s = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.13, 6), M.white);
        s.position.set(x, 0.44, 0.15);
        torso.add(s);
      }
    } else {
      const shirt = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.26, 3), M.white);
      shirt.rotation.set(Math.PI, 0, 0);
      shirt.scale.set(1, 1, 0.25);
      shirt.position.set(0, 0.45, 0.13);
      torso.add(shirt);
      for (const x of [-1, 1]) {
        const lapel = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.22, 0.015), M.top2);
        lapel.position.set(x * 0.06, 0.42, 0.142);
        lapel.rotation.z = x * 0.35;
        torso.add(lapel);
      }
    }
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.055, 0.1, 16), M.skin);
    neck.position.y = 0.6;
    torso.add(neck);

    /* head */
    const head = new THREE.Group();
    head.position.y = 0.78;
    torso.add(head);
    const skull = sph(0.16, M.skin, 1, 1.08, 0.98);
    head.add(skull);
    for (const x of [-1, 1]) {
      const ear = sph(0.032, M.skin, 0.6, 1, 0.8);
      ear.position.set(x * 0.157, -0.005, 0);
      head.add(ear);
    }
    const nose = sph(0.022, M.skin, 0.85, 1, 1);
    nose.position.set(0, -0.02, 0.158);
    head.add(nose);
    /* hair */
    const capGeo = new THREE.SphereGeometry(0.172, 40, 24, 0, Math.PI * 2, 0, Math.PI * 0.42);
    const hairCap = new THREE.Mesh(capGeo, M.hair);
    hairCap.scale.set(1.03, 1.12, 1.05);
    hairCap.position.set(0, 0.012, -0.012);
    hairCap.rotation.x = -0.18;
    hairCap.castShadow = true;
    head.add(hairCap);
    if (spec.hairStyle === "curly") {
      const r = rand(spec.seed || 3);
      for (let i = 0; i < 46; i++) {
        const th = r() * Math.PI * 2;
        const ph = 0.15 + r() * 0.95;
        const rr = 0.165;
        const c = sph(0.035 + r() * 0.015, M.hair);
        c.position.set(
          Math.sin(ph) * Math.cos(th) * rr,
          Math.cos(ph) * rr * 1.12 + 0.02,
          Math.sin(ph) * Math.sin(th) * rr - 0.01,
        );
        if (c.position.z > 0.09 && c.position.y < 0.1) continue;
        head.add(c);
      }
    } else {
      const fringe = sph(0.11, M.hair, 1.25, 0.42, 0.62);
      fringe.position.set(0.03, 0.135, 0.085);
      fringe.rotation.set(0.35, 0, -0.28);
      head.add(fringe);
      const side = sph(0.1, M.hair, 0.5, 0.6, 1.1);
      side.position.set(-0.13, 0.06, -0.02);
      head.add(side);
      const side2 = side.clone();
      side2.position.x = 0.13;
      head.add(side2);
    }
    /* eyes */
    const eyes = [];
    for (const x of [-1, 1]) {
      const g = new THREE.Group();
      g.position.set(x * 0.058, 0.025, 0.13);
      const w = sph(0.03, M.eyeW, 1, 1.1, 0.6);
      g.add(w);
      const p = sph(0.017, M.eyeP, 1, 1.05, 0.5);
      p.position.z = 0.014;
      g.add(p);
      const hl = sph(0.005, M.white);
      hl.position.set(0.006, 0.007, 0.022);
      g.add(hl);
      head.add(g);
      const brow = cap(0.007, 0.045, M.brow);
      brow.rotation.z = Math.PI / 2;
      const bg = new THREE.Group();
      bg.position.set(x * 0.058, 0.082, 0.142);
      bg.add(brow);
      head.add(bg);
      eyes.push({ g: g, p: p, brow: bg, side: x });
    }
    if (spec.glasses) {
      for (const x of [-1, 1]) {
        const ring = new THREE.Mesh(new THREE.TorusGeometry(0.04, 0.007, 8, 4), M.glass);
        ring.rotation.z = Math.PI / 4;
        ring.scale.set(1.25, 0.95, 1);
        ring.position.set(x * 0.06, 0.022, 0.165);
        head.add(ring);
        const temple = new THREE.Mesh(new THREE.BoxGeometry(0.006, 0.006, 0.15), M.glass);
        temple.position.set(x * 0.152, 0.03, 0.09);
        head.add(temple);
      }
      const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.006, 0.006), M.glass);
      bridge.position.set(0, 0.035, 0.168);
      head.add(bridge);
    }
    /* mouth: a smile arc and an open "O" */
    const smile = new THREE.Mesh(new THREE.TorusGeometry(0.042, 0.009, 8, 24, Math.PI), M.dark);
    smile.position.set(0, -0.075, 0.142);
    head.add(smile);
    const open = sph(0.03, M.dark, 1.1, 1, 0.4);
    open.position.set(0, -0.082, 0.14);
    head.add(open);
    const teeth = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.012, 0.01), M.white);
    teeth.position.set(0, -0.066, 0.152);
    head.add(teeth);

    /* arms */
    const arms = [];
    for (const x of [-1, 1]) {
      const up = limb(0.055, 0.24, M.top);
      up.pivot.position.set(x * 0.25, 0.5, 0);
      torso.add(up.pivot);
      const lo = limb(0.05, 0.22, M.top);
      up.end.add(lo.pivot);
      const hand = sph(0.05, M.skin, 0.9, 1, 0.8);
      hand.position.y = -0.03;
      lo.end.add(hand);
      arms.push({ up: up.pivot, lo: lo.pivot, side: x });
    }
    /* legs */
    const legs = [];
    for (const x of [-1, 1]) {
      const th = limb(0.075, 0.34, M.pants);
      th.pivot.position.set(x * 0.1, 0, 0);
      hips.add(th.pivot);
      const sh = limb(0.065, 0.32, M.pants);
      th.end.add(sh.pivot);
      const shoe = sph(0.07, M.shoe, 0.9, 0.6, 1.6);
      shoe.position.set(0, -0.04, 0.06);
      sh.end.add(shoe);
      legs.push({ th: th.pivot, sh: sh.pivot });
    }

    function pose(s) {
      s = s || {};
      const sit = s.sit || 0;
      hips.position.y = 0.92 - sit * 0.4;
      for (const l of legs) {
        l.th.rotation.x = -sit * 1.5 + (s.legSwing || 0);
        l.sh.rotation.x = sit * 1.5;
      }
      torso.rotation.x = (s.lean || 0) * 0.35;
      torso.scale.y = 1 + 0.012 * Math.sin((s.t || 0) * 2.3);
      head.rotation.set((s.headPitch || 0) + (s.nod || 0), s.headYaw || 0, s.headRoll || 0);
      const blink = Math.min(1, Math.max(0, s.blink || 0));
      const surprise = s.surprise || 0;
      for (const e of eyes) {
        e.g.scale.set(
          1 + surprise * 0.15,
          (1 - 0.92 * blink) * (1 + surprise * 0.25) * (1 - 0.35 * (s.squint || 0)),
          1,
        );
        e.p.position.x = (s.lookX || 0) * 0.008;
        e.p.position.y = (s.lookY || 0) * 0.008;
        /* brow: + angry (inner down), - worried (inner up) */
        const b = s.brow || 0;
        e.brow.rotation.z = e.side * b * 0.45;
        e.brow.position.y = 0.082 + surprise * 0.02 - Math.abs(b) * 0.004;
      }
      /* smile: +1 smile, -1 frown */
      const sm = s.smile || 0;
      smile.rotation.z = sm >= 0 ? Math.PI : 0;
      smile.scale.set(1, Math.max(0.15, Math.abs(sm)), 1);
      smile.position.y = sm >= 0 ? -0.066 : -0.098;
      const mo = Math.max(surprise, s.mouthOpen || 0);
      open.visible = mo > 0.05;
      open.scale.set(1.0, 0.25 + mo * 0.9, 0.4);
      smile.visible = mo < 0.4;
      teeth.visible = (s.teeth || 0) > 0.5;
      for (const a of arms) {
        const k = a.side < 0 ? "L" : "R";
        a.up.rotation.set(
          s["arm" + k + "x"] || 0,
          0,
          (s["arm" + k + "z"] || 0) * a.side + a.side * 0.12,
        );
        a.lo.rotation.set(s["fore" + k + "x"] || 0, 0, 0);
      }
    }
    pose({});
    root.traverse((o) => {
      if (o.isMesh) o.castShadow = true;
    });
    return { root: root, pose: pose, head: head };
  }

  /* a natural blink track: seeded times, 0.14 s each */
  function blinkTrack(seed, span) {
    const r = rand(seed);
    const times = [];
    let t = 0.4 + r();
    while (t < span) {
      times.push(t);
      t += 2.2 + r() * 2.4;
    }
    return function (time) {
      for (const b of times) {
        const d = time - b;
        if (d >= 0 && d < 0.14) return 1 - Math.abs(d - 0.07) / 0.07;
      }
      return 0;
    };
  }
  /* smooth blend between expression keys: [[t, {state}], ...] */
  function track(keys) {
    return function (time) {
      if (time <= keys[0][0]) return Object.assign({}, keys[0][1]);
      for (let i = 0; i < keys.length - 1; i++) {
        const a = keys[i];
        const b = keys[i + 1];
        if (time < b[0]) {
          const span = Math.min(0.28, b[0] - a[0]);
          let k = (time - (b[0] - span)) / span;
          k = k < 0 ? 0 : k;
          k = k * k * (3 - 2 * k);
          const out = {};
          const ks = new Set(Object.keys(a[1]).concat(Object.keys(b[1])));
          for (const key of ks)
            out[key] = (a[1][key] || 0) + ((b[1][key] || 0) - (a[1][key] || 0)) * k;
          return out;
        }
      }
      return Object.assign({}, keys[keys.length - 1][1]);
    };
  }
  window.HFChars = {
    make: make,
    blinkTrack: blinkTrack,
    track: track,
    MAGNUS: {
      skin: 0xf2c6a2,
      hair: 0x8b5a32,
      top: 0xa8adb5,
      top2: 0x969ba4,
      pants: 0x2b2f3a,
      shoe: 0x9aa0aa,
      outfit: "hoodie",
      iris: 0x3b5a7a,
    },
    FABI: {
      skin: 0xf0c3a0,
      hair: 0x1d1612,
      top: 0x22305a,
      top2: 0x1a2548,
      pants: 0x262a33,
      shoe: 0x15161a,
      outfit: "blazer",
      hairStyle: "curly",
      glasses: true,
      iris: 0x3a2416,
      seed: 9,
    },
  };
})();
