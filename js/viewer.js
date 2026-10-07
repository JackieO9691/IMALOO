// The reusable environment viewer. It reads one world's data and renders a
// location as layered depth: photo, time-of-day light, the toy (with cast and
// contact shadows, perspective scale and matched lighting), foreground occluders
// cut from the same photo, living effects, and tappable places to go, things to
// do and hidden things to find.

import { Effects } from './effects.js';
import { Sound } from './sound.js';
import { ICONS } from './icons.js';

const TIMES = {
  morning: { filter: 'brightness(1.02) saturate(1.04) sepia(.1)', overlay: 'linear-gradient(180deg, rgba(255,196,170,.18), rgba(255,240,220,0) 60%)' },
  day: { filter: 'none', overlay: 'none' },
  sunset: { filter: 'brightness(.94) saturate(1.18) sepia(.22) hue-rotate(-8deg)', overlay: 'linear-gradient(180deg, rgba(255,140,60,.28), rgba(255,170,90,.08) 55%, rgba(80,40,90,.12))' },
  night: { filter: 'brightness(.42) saturate(.62) hue-rotate(12deg) contrast(1.05)', overlay: 'linear-gradient(180deg, rgba(20,30,80,.45), rgba(10,20,60,.25))' }
};
const WEATHER = {
  sunny: { filter: '', fog: 0 },
  cloudy: { filter: 'saturate(.82) brightness(.93) contrast(.95)', fog: 0 },
  rain: { filter: 'saturate(.75) brightness(.86) contrast(.95)', fog: 0.12 },
  fog: { filter: 'saturate(.8) brightness(1.02) contrast(.85)', fog: 0.38 },
  snow: { filter: 'saturate(.8) brightness(1.06)', fog: 0.1 }
};
const MARK_SURFACES = new Set(['sand', 'dirt', 'snow']);

export class WorldViewer {
  constructor(stage, { onEvent = () => {}, speak = () => {} } = {}) {
    this.stage = stage; this.onEvent = onEvent; this.speak = speak;
    stage.classList.add('world-stage');
    stage.innerHTML = `
      <div class="ws-placeholder"></div>
      <img class="ws-bg" alt="" decoding="async">
      <div class="ws-tint"></div>
      <div class="ws-lights"></div>
      <div class="ws-marks"></div>
      <div class="ws-toy" hidden>
        <img class="ws-cast" alt="" aria-hidden="true">
        <div class="ws-contact"></div>
        <img class="ws-toyimg" alt="" onerror="this.style.visibility='hidden'" onload="this.style.visibility=''">
      </div>
      <svg class="ws-fg" viewBox="0 0 1 1" preserveAspectRatio="none" aria-hidden="true"><defs></defs></svg>
      <canvas class="ws-fx" aria-hidden="true"></canvas>
      <div class="ws-fog"></div>
      <div class="ws-hot"></div>
      <div class="ws-bubble" role="status" hidden></div>
      <div class="ws-loading" hidden><span></span></div>`;
    const q = s => stage.querySelector(s);
    this.el = { ph: q('.ws-placeholder'), bg: q('.ws-bg'), tint: q('.ws-tint'), lights: q('.ws-lights'), marks: q('.ws-marks'), toy: q('.ws-toy'), cast: q('.ws-cast'), contact: q('.ws-contact'), toyImg: q('.ws-toyimg'), fg: q('.ws-fg'), fx: q('.ws-fx'), fog: q('.ws-fog'), hot: q('.ws-hot'), bubble: q('.ws-bubble'), loading: q('.ws-loading') };
    this.fx = new Effects(this.el.fx);
    this.pos = { x: 0.5, y: 0.85 }; this.facing = 1; this.busy = false;
    this.time = 'day'; this.weather = 'sunny';
    this.found = new Set(); this.lightsOn = new Set();
    this.ro = new ResizeObserver(() => { this.fx.resize(); this.placeToy(); });
    this.ro.observe(stage);
    stage.addEventListener('click', e => this.onStageTap(e));
  }

  /* ---------- loading ---------- */
  async open(world, toy, { time, weather, location } = {}) {
    this.world = world; this.toy = toy;
    this.time = time || 'day'; this.weather = weather || 'sunny';
    this.el.toyImg.src = toy.src; this.el.cast.src = toy.src;
    this.el.toyImg.alt = toy.name;
    this.fx.start();
    await this.go(location || world.start, { arrive: null });
  }

  loc(id) { return this.world.locations.find(l => l.id === id); }

  async go(id, { arrive } = {}) {
    const L = this.loc(id); if (!L) return;
    const first = !this.L;
    this.stage.classList.add('ws-travel');
    if (!first) await wait(420);
    this.L = L;
    this.el.ph.style.background = `linear-gradient(180deg, ${L.tone[1]}, ${L.tone[0]})`;
    await this.loadImage(L);
    this.buildForeground(L); this.buildLights(L); this.buildHotspots(L);
    this.el.marks.innerHTML = '';
    this.applyLight();
    this.fx.setScene(L.ambient, { time: this.time, weather: this.weather });
    Sound.play(L.sound, { time: this.time, weather: this.weather });
    // Arrive from the side the child came from, then walk in.
    const s = { x: L.spawn[0], y: L.spawn[1] };
    const from = arrive ? { x: arrive.x < 0.5 ? 0.98 : 0.02, y: 0.95 } : null;
    this.pos = from ? { x: from.x, y: Math.max(s.y, from.y) } : { ...s };
    this.el.toy.hidden = false; this.placeToy();
    this.stage.classList.remove('ws-travel');
    this.preloadNeighbours(L);
    this.onEvent({ type: 'enter', world: this.world.id, location: L.id, name: L.name, pos: { ...s } });
    if (from) await this.walkTo(s.x, s.y);
  }

  loadImage(L) {
    const bg = this.el.bg;
    this.el.loading.hidden = false;
    return new Promise(resolve => {
      let done = false;
      const finish = ok => { if (done) return; done = true; this.el.loading.hidden = true; this.stage.classList.toggle('ws-noimage', !ok); resolve(); };
      // Progressive: small image first, swap in the large one when ready.
      const small = new Image(); small.decoding = 'async';
      small.onload = () => { bg.src = small.src; finish(true); };
      small.onerror = () => { bg.removeAttribute('src'); finish(false); };
      small.src = L.imageSm || L.image;
      const big = new Image(); big.decoding = 'async';
      big.onload = () => { if (this.L === L) { bg.src = big.src; this.refreshForegroundHref(big.src); } finish(true); };
      big.src = L.image;
      setTimeout(() => finish(!!bg.getAttribute('src')), 6000);
    });
  }

  preloadNeighbours(L) {
    (L.nav || []).forEach(n => { const T = this.loc(n.to); if (T) { const i = new Image(); i.src = T.imageSm || T.image; } });
  }

  /* ---------- layers ---------- */
  buildForeground(L) {
    // Occluders: polygons of the photo itself, redrawn above the toy, so the toy
    // can stand behind a rock or a log. Each shows only when the toy is behind it.
    const svg = this.el.fg, defs = svg.querySelector('defs');
    svg.querySelectorAll('g').forEach(g => g.remove()); defs.innerHTML = '';
    (L.foreground || []).forEach((f, i) => {
      const cp = document.createElementNS('http://www.w3.org/2000/svg', 'clipPath');
      cp.id = `occ-${i}`; cp.setAttribute('clipPathUnits', 'userSpaceOnUse');
      const poly = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      poly.setAttribute('points', f.polygon.map(p => p.join(',')).join(' '));
      cp.appendChild(poly); defs.appendChild(cp);
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('clip-path', `url(#occ-${i})`); g.dataset.baseY = f.baseY ?? Math.max(...f.polygon.map(p => p[1]));
      const im = document.createElementNS('http://www.w3.org/2000/svg', 'image');
      im.setAttribute('x', 0); im.setAttribute('y', 0); im.setAttribute('width', 1); im.setAttribute('height', 1);
      im.setAttribute('preserveAspectRatio', 'none'); im.setAttribute('href', this.el.bg.src || '');
      g.appendChild(im); svg.appendChild(g);
    });
  }
  refreshForegroundHref(src) { this.el.fg.querySelectorAll('image').forEach(i => i.setAttribute('href', src)); }

  buildLights(L) {
    const box = this.el.lights; box.innerHTML = '';
    (L.lights || []).forEach(([x, y], i) => {
      const s = document.createElement('i'); s.style.left = x * 100 + '%'; s.style.top = y * 100 + '%'; s.style.animationDelay = (i * 0.37) + 's';
      box.appendChild(s);
    });
    box.classList.toggle('on', this.lightsOn.has(L.id));
  }

  buildHotspots(L) {
    const hot = this.el.hot; hot.innerHTML = '';
    (L.nav || []).forEach(n => {
      const T = this.loc(n.to); if (!T) return;
      const b = btn('ws-hs ws-nav', n.x, n.y, `Go to ${T.name}`);
      b.innerHTML = `<span class="ws-thumb" style="background-image:url('${T.imageSm || T.image}'), linear-gradient(180deg, ${T.tone[1]}, ${T.tone[0]})"></span><span class="ws-steps">${ICONS.steps}</span>`;
      b.addEventListener('click', e => { e.stopPropagation(); this.travel(n); });
      hot.appendChild(b);
    });
    (L.interactions || []).forEach(a => {
      const b = btn('ws-hs ws-act', a.x, a.y, a.story.replace('{name}', this.toy.name));
      b.innerHTML = `<span class="ws-ring"></span><span class="ws-ico">${ICONS[a.kind] || ICONS.sparkle}</span>`;
      b.addEventListener('click', e => { e.stopPropagation(); this.interact(a); });
      hot.appendChild(b);
    });
    (L.discoveries || []).forEach(d => {
      const key = `${L.id}:${d.id}`;
      const b = btn('ws-hs ws-find', d.x, d.y, 'Something hidden');
      b.hidden = true; b.dataset.key = key;
      b.innerHTML = `<span class="ws-glint"></span><span class="ws-item">${ICONS[d.item] || ICONS.sparkle}</span>`;
      b.addEventListener('click', e => { e.stopPropagation(); this.collect(d, b); });
      if (this.found.has(key)) b.remove(); else hot.appendChild(b);
    });
  }

  /* ---------- light, time, weather ---------- */
  setTime(t) { this.time = t; this.applyLight(); this.refreshScene(); }
  setWeather(w) { this.weather = w; this.applyLight(); this.refreshScene(); }
  refreshScene() {
    if (!this.L) return;
    this.fx.setScene(this.L.ambient, { time: this.time, weather: this.weather });
    Sound.play(this.L.sound, { time: this.time, weather: this.weather });
  }
  applyLight() {
    const T = TIMES[this.time] || TIMES.day, Wt = WEATHER[this.weather] || WEATHER.sunny, L = this.L;
    const f = [T.filter, Wt.filter].filter(x => x && x !== 'none').join(' ') || 'none';
    this.el.bg.style.filter = f; this.el.fg.style.filter = f;
    this.el.tint.style.background = T.overlay;
    this.el.fog.style.opacity = Wt.fog;
    // The toy takes the scene's light: same grade, plus the place's warmth.
    const warm = L ? L.lighting.warmth || 0 : 0;
    this.el.toyImg.style.filter = `${f === 'none' ? '' : f} sepia(${warm.toFixed(2)}) contrast(1.02)`.trim();
    const sh = L ? L.lighting.shadow : 0.45;
    const dim = this.time === 'night' ? 0.35 : this.weather === 'cloudy' || this.weather === 'rain' || this.weather === 'fog' ? 0.45 : 1;
    this.stage.style.setProperty('--shadow', (sh * dim).toFixed(2));
    this.stage.style.setProperty('--contact', (0.55 * (dim < 1 ? 0.8 : 1)).toFixed(2));
    this.stage.dataset.time = this.time;
    this.placeToy();
  }

  /* ---------- the toy ---------- */
  scaleAt(y) {
    const g = this.L.ground, k = (y - g.horizon) / (1 - g.horizon);
    return g.nearScale * Math.min(1.15, Math.max(0.18, k));
  }
  placeToy() {
    if (!this.L) return;
    const { x, y } = this.pos, H = this.stage.clientHeight || 1;
    const h = this.scaleAt(y) * H;
    const t = this.el.toy;
    t.style.left = x * 100 + '%'; t.style.top = y * 100 + '%';
    t.style.height = h + 'px'; t.style.zIndex = 5;
    t.style.setProperty('--face', this.facing);
    const from = this.L.lighting.from || 0, back = this.L.lighting.backlit;
    this.el.cast.style.transform = back ? `scaleY(-0.32) skewX(${-from}deg)` : `scaleY(0.34) skewX(${from}deg)`;
    // Foreground pieces cover the toy only when the toy stands behind them.
    this.el.fg.querySelectorAll('g').forEach(g => { g.style.display = y < +g.dataset.baseY ? '' : 'none'; });
    this.revealNearby();
  }

  walkTo(tx, ty) {
    const L = this.L; if (!L) return Promise.resolve();
    [tx, ty] = clampToArea(L.walk, tx, ty);
    const sx = this.pos.x, sy = this.pos.y, dist = Math.hypot(tx - sx, (ty - sy) * 1.6);
    if (dist < 0.005) return Promise.resolve();
    this.facing = tx < sx ? -1 : 1;
    const dur = Math.max(450, dist * 2600);
    const marks = MARK_SURFACES.has(L.surface);
    let lastMark = 0;
    this.el.toy.classList.add('walking');
    return new Promise(res => {
      const t0 = performance.now();
      const step = now => {
        const k = Math.min(1, (now - t0) / dur), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        this.pos = { x: sx + (tx - sx) * e, y: sy + (ty - sy) * e };
        this.placeToy();
        if (marks && k - lastMark > 0.08) { lastMark = k; this.leaveMark(); }
        if (k < 1) requestAnimationFrame(step); else { this.el.toy.classList.remove('walking'); res(); }
      };
      requestAnimationFrame(step);
    });
  }

  leaveMark() {
    const m = document.createElement('i'), s = this.scaleAt(this.pos.y);
    m.style.left = this.pos.x * 100 + '%'; m.style.top = this.pos.y * 100 + '%';
    m.style.width = s * 9 + '%'; m.style.height = s * 3 + '%';
    this.el.marks.appendChild(m);
    setTimeout(() => m.remove(), 9000);
  }

  async perform(kind) {
    const t = this.el.toy, cls = `do-${kind}`;
    t.classList.remove(cls); void t.offsetWidth; t.classList.add(cls);
    await wait(kind === 'hop' ? 1500 : 1100);
    t.classList.remove(cls);
  }

  /* ---------- play ---------- */
  onStageTap(e) {
    if (this.busy || !this.L) return;
    const r = this.stage.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
    if (y < this.L.ground.horizon) return;
    this.walkTo(x, y);
  }

  async travel(n) {
    if (this.busy) return; this.busy = true;
    await this.walkTo(n.x, n.y);
    await this.go(n.to, { arrive: n });
    this.busy = false;
  }

  async interact(a) {
    if (this.busy) return; this.busy = true;
    // Stand just in front of the thing, on the side the toy is coming from.
    const side = this.pos.x < a.x ? -1 : 1;
    await this.walkTo(a.x + side * 0.06, Math.max(a.y + 0.03, this.L.ground.horizon + 0.08));
    this.facing = side > 0 ? -1 : 1; this.placeToy();
    if (a.kind === 'lights') {
      const on = !this.lightsOn.has(this.L.id);
      on ? this.lightsOn.add(this.L.id) : this.lightsOn.delete(this.L.id);
      this.el.lights.classList.toggle('on', on);
    }
    const p = this.perform(a.kind);
    if (a.fx) setTimeout(() => this.fx.burst(a.fx, a.x, a.y), 250);
    const text = a.story.replace(/\{name\}/g, this.toy.name);
    this.say(text);
    this.onEvent({ type: 'interact', world: this.world.id, location: this.L.id, id: a.id, kind: a.kind, text, pos: { ...this.pos } });
    await p; this.busy = false;
  }

  revealNearby() {
    if (!this.L) return;
    this.el.hot.querySelectorAll('.ws-find[hidden]').forEach(b => {
      const d = (this.L.discoveries || []).find(x => `${this.L.id}:${x.id}` === b.dataset.key); if (!d) return;
      if (Math.hypot(d.x - this.pos.x, (d.y - this.pos.y) * 1.6) < (d.near || 0.16)) {
        b.hidden = false; b.classList.add('ws-pop'); this.fx.burst('sparkle', d.x, d.y); Sound.pop('near');
      }
    });
  }

  async collect(d, b) {
    if (this.busy) return; this.busy = true;
    await this.walkTo(d.x + (this.pos.x < d.x ? -0.05 : 0.05), Math.max(d.y + 0.02, this.L.ground.horizon + 0.08));
    const key = `${this.L.id}:${d.id}`; this.found.add(key);
    const r = b.getBoundingClientRect();
    b.classList.add('ws-collected'); setTimeout(() => b.remove(), 700);
    Sound.pop('find'); this.fx.burst('sparkle', d.x, d.y);
    const text = d.story.replace(/\{name\}/g, this.toy.name);
    this.say(text);
    this.onEvent({ type: 'discover', world: this.world.id, location: this.L.id, id: d.id, item: d.item, text, rect: r, pos: { ...this.pos } });
    await this.perform('wonder'); this.busy = false;
  }

  say(text) {
    const b = this.el.bubble; b.textContent = text; b.hidden = false;
    b.classList.remove('show'); void b.offsetWidth; b.classList.add('show');
    clearTimeout(this.bt); this.bt = setTimeout(() => { b.hidden = true; }, 5200);
    this.speak(text);
  }

  /* ---------- story playback support ---------- */
  async showMoment(m) {
    if (!this.L || this.L.id !== m.location) await this.go(m.location);
    this.pos = { ...m.pos }; this.placeToy();
    if (m.kind) this.perform(m.kind);
    this.say(m.text);
  }

  close() { this.fx.stop(); Sound.stop(); this.L = null; this.el.toy.hidden = true; }
}

/* ---------- helpers ---------- */
function btn(cls, x, y, label) {
  const b = document.createElement('button'); b.type = 'button'; b.className = cls;
  b.style.left = x * 100 + '%'; b.style.top = y * 100 + '%'; b.setAttribute('aria-label', label);
  return b;
}
const wait = ms => new Promise(r => setTimeout(r, ms));

function inside(poly, x, y) {
  let c = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c;
  }
  return c;
}
// Keep the toy on walkable ground: if a tap lands outside, use the nearest point on the edge.
export function clampToArea(poly, x, y) {
  if (!poly || inside(poly, x, y)) return [x, y];
  let best = [x, y], bd = Infinity;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [ax, ay] = poly[j], [bx, by] = poly[i], dx = bx - ax, dy = by - ay;
    const t = Math.max(0, Math.min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy || 1)));
    const px = ax + t * dx, py = ay + t * dy, d = (px - x) ** 2 + (py - y) ** 2;
    if (d < bd) { bd = d; best = [px, py]; }
  }
  // Nudge slightly inward toward the area's centre.
  const cx = poly.reduce((s, p) => s + p[0], 0) / poly.length, cy = poly.reduce((s, p) => s + p[1], 0) / poly.length;
  return [best[0] + (cx - best[0]) * 0.03, best[1] + (cy - best[1]) * 0.03];
}
