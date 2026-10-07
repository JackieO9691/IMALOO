// Living-environment layer: subtle ambient motion, weather and short bursts,
// drawn on one canvas over the photo. Everything is driven by world data
// ("ambient" entries with a type and a normalised area), so new worlds need no code.

const TAU = Math.PI * 2;
const rand = (a, b) => a + Math.random() * (b - a);

export class Effects {
  constructor(canvas) {
    this.cv = canvas;
    this.c = canvas.getContext('2d');
    this.parts = [];
    this.bursts = [];
    this.weather = 'sunny';
    this.time = 'day';
    this.t = 0;
    this.raf = 0;
    this.reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.resize();
  }

  resize() {
    const r = this.cv.getBoundingClientRect();
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    this.w = Math.max(1, r.width); this.h = Math.max(1, r.height);
    this.cv.width = Math.round(this.w * dpr); this.cv.height = Math.round(this.h * dpr);
    this.c.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  setScene(ambient = [], { time = 'day', weather = 'sunny' } = {}) {
    this.time = time; this.weather = weather;
    this.parts = [];
    const night = time === 'night';
    ambient.forEach(a => {
      let type = a.type;
      // Daytime creatures rest at night; fireflies and stars take over.
      if (night && (type === 'butterflies' || type === 'bees' || type === 'birds')) return;
      if (weather === 'rain' && (type === 'butterflies' || type === 'bees' || type === 'dust')) return;
      if (night && type === 'dust') type = 'fireflies';
      const n = this.reduced ? Math.ceil((a.n || 10) / 3) : (a.n || 10);
      for (let i = 0; i < n; i++) this.parts.push(this.spawn(type, a));
    });
    if (night) {
      for (let i = 0; i < 40; i++) this.parts.push(this.spawn('stars', { area: [0, 0, 1, 0.35] }));
      for (let i = 0; i < 10; i++) this.parts.push(this.spawn('fireflies', { area: [0, 0.4, 1, 0.5] }));
    }
    if (weather === 'rain') for (let i = 0; i < (this.reduced ? 60 : 160); i++) this.parts.push(this.spawn('rain', { area: [0, 0, 1, 1] }));
    if (weather === 'snow') for (let i = 0; i < 90; i++) this.parts.push(this.spawn('snow', { area: [0, 0, 1, 1] }));
  }

  spawn(type, a) {
    const [ax, ay, aw, ah] = a.area || [0, 0, 1, 1];
    const p = { type, ax, ay, aw, ah, x: ax + Math.random() * aw, y: ay + Math.random() * ah, ph: Math.random() * TAU, s: rand(0.6, 1.4), fall: a.fall, warm: a.warm };
    if (type === 'birds') { p.x = -0.1 - Math.random() * 0.6; p.v = rand(0.012, 0.022); }
    if (type === 'leaves') { p.v = rand(0.01, 0.025); p.rot = Math.random() * TAU; p.col = ['#7a8f3a', '#a8862f', '#5f7a2e'][Math.floor(Math.random() * 3)]; }
    if (type === 'butterflies') p.col = ['#f2a33a', '#f7f1e3', '#7fb2e5'][Math.floor(Math.random() * 3)];
    if (type === 'rain') { p.v = rand(0.9, 1.4); }
    if (type === 'snow') { p.v = rand(0.03, 0.07); }
    if (type === 'waves') { p.v = rand(0.15, 0.3); }
    return p;
  }

  burst(kind, x, y) {
    const n = kind === 'sparkle' ? 18 : 22;
    for (let i = 0; i < n; i++) {
      const ang = kind === 'splash' ? rand(-Math.PI * 0.9, -Math.PI * 0.1) : rand(0, TAU);
      const sp = kind === 'splash' ? rand(0.25, 0.55) : rand(0.08, 0.25);
      this.bursts.push({ kind, x, y, vx: Math.cos(ang) * sp * 0.6, vy: Math.sin(ang) * sp, life: 1, s: rand(0.6, 1.3) });
    }
  }

  start() {
    cancelAnimationFrame(this.raf);
    let last = performance.now();
    const loop = now => {
      const dt = Math.min(0.05, (now - last) / 1000); last = now;
      this.t += dt; this.draw(dt);
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }
  stop() { cancelAnimationFrame(this.raf); }

  draw(dt) {
    const c = this.c, W = this.w, H = this.h, T = this.t;
    c.clearRect(0, 0, W, H);
    for (const p of this.parts) {
      const X = p.x * W, Y = p.y * H;
      switch (p.type) {
        case 'dust': {
          p.x += Math.sin(T * 0.3 + p.ph) * 0.00008; p.y -= 0.004 * dt;
          if (p.y < p.ay) p.y = p.ay + p.ah;
          c.fillStyle = `rgba(255,246,220,${0.15 + 0.25 * Math.abs(Math.sin(T * 0.8 + p.ph))})`;
          c.beginPath(); c.arc(X, Y, 1.2 * p.s, 0, TAU); c.fill(); break;
        }
        case 'fireflies': {
          p.x += Math.sin(T * 0.5 + p.ph) * 0.0004; p.y += Math.cos(T * 0.4 + p.ph) * 0.0003;
          const a = Math.max(0, Math.sin(T * 1.6 + p.ph));
          const g = c.createRadialGradient(X, Y, 0, X, Y, 9 * p.s);
          g.addColorStop(0, `rgba(255,236,140,${0.9 * a})`); g.addColorStop(1, 'rgba(255,236,140,0)');
          c.fillStyle = g; c.beginPath(); c.arc(X, Y, 9 * p.s, 0, TAU); c.fill(); break;
        }
        case 'stars': {
          c.fillStyle = `rgba(255,255,255,${0.25 + 0.5 * Math.abs(Math.sin(T * 0.7 + p.ph))})`;
          c.fillRect(X, Y, 1.4 * p.s, 1.4 * p.s); break;
        }
        case 'leaves': {
          p.y += p.v * dt; p.x += Math.sin(T * 0.9 + p.ph) * 0.0006; p.rot += dt * 1.2;
          if (p.y > p.ay + p.ah + 0.1) { p.y = p.ay - 0.05; p.x = p.ax + Math.random() * p.aw; }
          c.save(); c.translate(X, Y); c.rotate(p.rot); c.scale(1, Math.abs(Math.sin(T * 2 + p.ph)) * 0.7 + 0.3);
          c.fillStyle = p.col; c.globalAlpha = 0.75;
          c.beginPath(); c.ellipse(0, 0, 5 * p.s, 2.4 * p.s, 0, 0, TAU); c.fill(); c.restore(); break;
        }
        case 'butterflies': case 'bees': {
          const bx = (p.ax + p.aw * (0.5 + 0.45 * Math.sin(T * 0.13 + p.ph))) * W;
          const by = (p.ay + p.ah * (0.5 + 0.4 * Math.sin(T * 0.31 + p.ph * 2))) * H;
          const f = Math.abs(Math.sin(T * (p.type === 'bees' ? 40 : 9) + p.ph));
          c.save(); c.translate(bx, by);
          if (p.type === 'bees') {
            c.fillStyle = 'rgba(60,40,10,.8)'; c.beginPath(); c.ellipse(0, 0, 2.6, 1.8, 0, 0, TAU); c.fill();
            c.fillStyle = `rgba(255,255,255,${0.4 * f})`; c.beginPath(); c.ellipse(0, -2, 2.5, 1.4, 0, 0, TAU); c.fill();
          } else {
            c.fillStyle = p.col; c.globalAlpha = 0.85;
            const s = 4 * p.s;
            c.beginPath(); c.ellipse(-s * 0.7 * f, 0, s * f, s * 0.8, -0.3, 0, TAU); c.fill();
            c.beginPath(); c.ellipse(s * 0.7 * f, 0, s * f, s * 0.8, 0.3, 0, TAU); c.fill();
            c.globalAlpha = 1; c.fillStyle = '#2b2118'; c.fillRect(-0.6, -s * 0.6, 1.2, s * 1.2);
          }
          c.restore(); break;
        }
        case 'birds': {
          p.x += p.v * dt;
          if (p.x > 1.15) { p.x = -0.15 - Math.random() * 0.8; p.y = p.ay + Math.random() * p.ah; }
          const f = Math.sin(T * 7 + p.ph) * 3 * p.s;
          c.strokeStyle = 'rgba(40,40,45,.55)'; c.lineWidth = 1.3;
          c.beginPath(); c.moveTo(X - 6 * p.s, Y - f); c.quadraticCurveTo(X - 2, Y - 2, X, Y); c.quadraticCurveTo(X + 2, Y - 2, X + 6 * p.s, Y - f); c.stroke(); break;
        }
        case 'water': {
          // Sparkling highlights on moving water; "fall" streams them downward.
          if (p.fall) { p.y += 0.25 * dt; if (p.y > p.ay + p.ah) p.y = p.ay; }
          else p.x += 0.006 * dt * Math.sin(p.ph);
          const a = Math.max(0, Math.sin(T * 3 + p.ph * 3));
          c.fillStyle = p.warm ? `rgba(255,214,150,${0.55 * a})` : `rgba(255,255,255,${0.45 * a})`;
          if (p.fall) c.fillRect(X, Y, 1.2, 7 * p.s); else c.fillRect(X - 4 * p.s, Y, 8 * p.s, 1.2);
          break;
        }
        case 'mist': {
          const g = c.createRadialGradient(X, Y, 0, X, Y, 60 * p.s);
          g.addColorStop(0, `rgba(255,255,255,${0.06 + 0.04 * Math.sin(T * 0.5 + p.ph)})`); g.addColorStop(1, 'rgba(255,255,255,0)');
          c.fillStyle = g; c.beginPath(); c.arc(X + Math.sin(T * 0.2 + p.ph) * 10, Y, 60 * p.s, 0, TAU); c.fill(); break;
        }
        case 'waves': {
          // A soft foam line that rolls up the sand and back.
          const k = 0.5 + 0.5 * Math.sin(T * 0.6 + p.ph);
          const wy = (p.ay + p.ah * k) * H;
          c.strokeStyle = `rgba(255,255,255,${0.12 + 0.18 * (1 - k)})`; c.lineWidth = 2;
          c.beginPath();
          for (let x = 0; x <= W; x += 24) c.lineTo(x, wy + Math.sin(x * 0.02 + T + p.ph) * 3);
          c.stroke(); break;
        }
        case 'sand': {
          p.x += 0.01 * dt; if (p.x > p.ax + p.aw) p.x = p.ax;
          c.fillStyle = `rgba(255,240,210,${0.25 * Math.abs(Math.sin(T + p.ph))})`; c.fillRect(X, Y, 1.5, 1.5); break;
        }
        case 'bubbles': {
          p.y -= 0.05 * dt; if (p.y < p.ay) p.y = p.ay + p.ah;
          c.strokeStyle = 'rgba(255,255,255,.5)'; c.beginPath(); c.arc(X + Math.sin(T * 2 + p.ph) * 3, Y, 3 * p.s, 0, TAU); c.stroke(); break;
        }
        case 'rain': {
          p.y += p.v * dt; p.x -= 0.05 * dt; if (p.y > 1) { p.y = -0.05; p.x = Math.random() * 1.1; }
          c.strokeStyle = 'rgba(210,225,240,.35)'; c.lineWidth = 1;
          c.beginPath(); c.moveTo(X, Y); c.lineTo(X - 2, Y + 12 * p.s); c.stroke(); break;
        }
        case 'snow': {
          p.y += p.v * dt; p.x += Math.sin(T + p.ph) * 0.0004; if (p.y > 1) { p.y = -0.02; p.x = Math.random(); }
          c.fillStyle = 'rgba(255,255,255,.85)'; c.beginPath(); c.arc(X, Y, 2 * p.s, 0, TAU); c.fill(); break;
        }
      }
    }
    // Short bursts from interactions: water droplets and sparkles.
    this.bursts = this.bursts.filter(b => b.life > 0);
    for (const b of this.bursts) {
      b.life -= dt * 1.4; b.x += b.vx * dt; b.y += b.vy * dt;
      if (b.kind === 'splash' || b.kind === 'sand') b.vy += 1.2 * dt;
      const X = b.x * W, Y = b.y * H;
      if (b.kind === 'splash') { c.fillStyle = `rgba(225,240,255,${b.life})`; c.beginPath(); c.arc(X, Y, 2.2 * b.s, 0, TAU); c.fill(); }
      else if (b.kind === 'sand') { c.fillStyle = `rgba(214,184,130,${b.life})`; c.fillRect(X, Y, 2.5 * b.s, 2.5 * b.s); }
      else { c.fillStyle = `rgba(255,236,160,${b.life})`; c.beginPath(); c.arc(X, Y, 1.8 * b.s, 0, TAU); c.fill(); }
    }
  }
}
