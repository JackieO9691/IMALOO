// Gentle generated soundscapes (no audio files to download): filtered noise for
// water, wind and waves, plus occasional bird chirps or night crickets.
// Starts only after a tap, as browsers require.

let ctx = null, master = null, nodes = [], timers = [], enabled = true;

function ac() {
  if (!ctx) {
    const C = window.AudioContext || window.webkitAudioContext;
    if (!C) return null;
    ctx = new C(); master = ctx.createGain(); master.gain.value = 0.5; master.connect(ctx.destination);
  }
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}

function noise(c) {
  const buf = c.createBuffer(1, c.sampleRate * 2, c.sampleRate), d = buf.getChannelData(0);
  let last = 0;
  for (let i = 0; i < d.length; i++) { const w = Math.random() * 2 - 1; last = (last + 0.02 * w) / 1.02; d[i] = last * 3.5; }
  const src = c.createBufferSource(); src.buffer = buf; src.loop = true; return src;
}

function bed(c, { freq = 800, q = 0.5, vol = 0.2, lfo = 0, lfoDepth = 0 }) {
  const src = noise(c), f = c.createBiquadFilter(), g = c.createGain();
  f.type = 'lowpass'; f.frequency.value = freq; f.Q.value = q; g.gain.value = vol;
  src.connect(f).connect(g).connect(master); src.start();
  nodes.push(src, g);
  if (lfo) {
    const o = c.createOscillator(), og = c.createGain();
    o.frequency.value = lfo; og.gain.value = lfoDepth; o.connect(og).connect(g.gain); o.start(); nodes.push(o);
  }
}

function chirps(c, every, night) {
  const fire = () => {
    const t = c.currentTime, o = c.createOscillator(), g = c.createGain();
    if (night) { o.type = 'square'; o.frequency.value = 4200; }
    else { o.type = 'sine'; o.frequency.setValueAtTime(2400 + Math.random() * 1500, t); o.frequency.exponentialRampToValueAtTime(3800 + Math.random() * 900, t + 0.08); }
    g.gain.setValueAtTime(0.0001, t);
    const reps = night ? 3 : 2;
    for (let i = 0; i < reps; i++) {
      g.gain.exponentialRampToValueAtTime(night ? 0.012 : 0.03, t + i * 0.12 + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.12 + 0.09);
    }
    o.connect(g).connect(master); o.start(t); o.stop(t + reps * 0.12 + 0.1);
  };
  timers.push(setInterval(() => { if (Math.random() < 0.6) fire(); }, every));
}

const SCAPES = {
  forest: (c, n) => { bed(c, { freq: 500, vol: 0.12, lfo: 0.08, lfoDepth: 0.05 }); chirps(c, n ? 900 : 2600, n); },
  creek: (c, n) => { bed(c, { freq: 2200, q: 0.8, vol: 0.12 }); bed(c, { freq: 600, vol: 0.08 }); chirps(c, n ? 900 : 3400, n); },
  waterfall: (c) => { bed(c, { freq: 3200, vol: 0.18 }); bed(c, { freq: 400, vol: 0.12 }); },
  waves: (c) => { bed(c, { freq: 900, vol: 0.2, lfo: 0.11, lfoDepth: 0.16 }); },
  'waves-far': (c, n) => { bed(c, { freq: 500, vol: 0.12, lfo: 0.09, lfoDepth: 0.08 }); chirps(c, n ? 900 : 4000, n); },
  'waves-calm': (c) => { bed(c, { freq: 600, vol: 0.12, lfo: 0.07, lfoDepth: 0.07 }); },
  backyard: (c, n) => { bed(c, { freq: 400, vol: 0.06 }); chirps(c, n ? 800 : 2200, n); },
  indoors: (c) => { bed(c, { freq: 250, vol: 0.04 }); },
  rain: (c) => { bed(c, { freq: 5000, q: 0.3, vol: 0.12 }); }
};

export const Sound = {
  set enabled(v) { enabled = v; if (!v) this.stop(); },
  get enabled() { return enabled; },
  play(name, { time = 'day', weather = 'sunny' } = {}) {
    this.stop();
    if (!enabled) return;
    const c = ac(); if (!c) return;
    const night = time === 'night';
    (SCAPES[name] || SCAPES.forest)(c, night);
    if (weather === 'rain') SCAPES.rain(c);
  },
  pop(kind = 'find') {
    if (!enabled) return;
    const c = ac(); if (!c) return;
    const t = c.currentTime, notes = kind === 'find' ? [784, 988, 1319] : [523, 659];
    notes.forEach((f, i) => {
      const o = c.createOscillator(), g = c.createGain(); o.type = 'triangle'; o.frequency.value = f;
      g.gain.setValueAtTime(0.0001, t + i * 0.09); g.gain.exponentialRampToValueAtTime(0.08, t + i * 0.09 + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.09 + 0.35);
      o.connect(g).connect(master); o.start(t + i * 0.09); o.stop(t + i * 0.09 + 0.4);
    });
  },
  stop() {
    nodes.forEach(n => { try { n.stop ? n.stop() : n.disconnect(); } catch (e) {} });
    timers.forEach(clearInterval); nodes = []; timers = [];
  }
};
