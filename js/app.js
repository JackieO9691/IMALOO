// IMALOO app shell: Home → Choose My Toy → Choose A World → Enter → Explore,
// Discover, Interact → Create Story. Worlds come from data/worlds.json, so a new
// world is a new JSON file plus its photos; no code changes.

import { WorldViewer } from './viewer.js';
import { Sound } from './sound.js';
import { ICONS } from './icons.js';
import { BUILT_IN, loadMyToys, saveMyToys, cutOutToy } from './toys.js';

const $ = id => document.getElementById(id);
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
};
const prefs = { voice: store.get('imaloo.voice', true), sound: store.get('imaloo.sound', true) };
Sound.enabled = prefs.sound;

const state = { registry: null, worlds: {}, toy: null, myToys: loadMyToys(), world: null, journal: [], time: 'day', weather: 'sunny', pendingPhoto: null };
const SCREENS = ['home', 'toys', 'naming', 'explorer', 'world', 'grown'];

function show(id) {
  SCREENS.forEach(s => { $(s).hidden = s !== id; });
  document.body.dataset.screen = id;
  if (id !== 'world') { viewer.close(); hush(); }
  if (id === 'toys') drawToys();
  if (id === 'explorer') drawExplorer();
  window.scrollTo(0, 0);
}

function speak(text) {
  try { speechSynthesis.cancel(); if (!prefs.voice || !text) return; const u = new SpeechSynthesisUtterance(text); u.rate = 0.95; u.pitch = 1.1; speechSynthesis.speak(u); } catch (e) {}
}
function hush() { try { speechSynthesis.cancel(); } catch (e) {} }
function toast(msg) { const t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status'); t.textContent = msg; document.body.appendChild(t); setTimeout(() => t.remove(), 2400); }

/* ---------- data ---------- */
async function loadRegistry() {
  const r = await fetch('data/worlds.json'); state.registry = await r.json();
}
async function loadWorld(entry) {
  if (state.worlds[entry.id]) return state.worlds[entry.id];
  const r = await fetch(entry.data); const w = await r.json();
  state.worlds[entry.id] = w; return w;
}

/* ---------- toys ---------- */
const allToys = () => BUILT_IN.concat(state.myToys);
function drawToys() {
  const g = $('toyGrid'); g.innerHTML = '';
  const cam = document.createElement('label'); cam.className = 'card toy-card camera'; cam.htmlFor = 'photoIn'; cam.tabIndex = 0;
  cam.innerHTML = `<span class="cam-ico"><svg viewBox="0 0 64 64" aria-hidden="true"><rect x="6" y="16" width="52" height="38" rx="10" fill="currentColor"/><rect x="22" y="9" width="20" height="10" rx="4" fill="currentColor"/><circle cx="32" cy="35" r="12" fill="var(--sun)"/><circle cx="32" cy="35" r="6" fill="currentColor"/></svg></span><b>My toy</b>`;
  cam.setAttribute('aria-label', 'Take a photo of my toy');
  cam.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); $('photoIn').click(); } });
  g.appendChild(cam);
  allToys().forEach(t => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'card toy-card';
    b.setAttribute('aria-pressed', state.toy && state.toy.id === t.id ? 'true' : 'false');
    const img = document.createElement('img'); img.alt = ''; img.src = t.src; img.loading = 'lazy';
    img.onerror = () => { b.classList.add('missing'); };
    const name = document.createElement('b'); name.textContent = t.name;
    b.append(img, name);
    b.addEventListener('click', () => { state.toy = t; show('explorer'); });
    if (t.kind === 'photo') {
      const rm = document.createElement('button'); rm.type = 'button'; rm.className = 'remove'; rm.textContent = '×';
      rm.setAttribute('aria-label', `Remove ${t.name}`);
      rm.addEventListener('click', e => { e.stopPropagation(); state.myToys = state.myToys.filter(x => x.id !== t.id); saveMyToys(state.myToys); drawToys(); });
      b.appendChild(rm);
    }
    g.appendChild(b);
  });
}

$('photoIn').addEventListener('change', async e => {
  const file = e.target.files && e.target.files[0]; e.target.value = '';
  if (!file) return;
  $('nameBusy').hidden = false; show('naming'); $('nameImg').removeAttribute('src');
  try {
    const out = await cutOutToy(file);
    state.pendingPhoto = out.src; $('nameImg').src = out.src;
    $('cutHint').hidden = out.clean;
  } catch (err) { toast(err.message); show('toys'); return; }
  finally { $('nameBusy').hidden = true; }
  $('nameIn').value = '';
  const chips = $('nameChips'); chips.innerHTML = '';
  ['Teddy', 'Bunny', 'Dolly', 'Pony', 'Dino', 'Kitty', 'Puppy', 'Unicorn'].forEach(n => {
    const c = document.createElement('button'); c.type = 'button'; c.className = 'chip'; c.textContent = n; c.setAttribute('aria-pressed', 'false');
    c.addEventListener('click', () => { $('nameIn').value = n; chips.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x === c ? 'true' : 'false')); });
    chips.appendChild(c);
  });
});
$('nameDone').addEventListener('click', () => {
  if (!state.pendingPhoto) return;
  const t = { id: 'p' + Date.now(), name: (($('nameIn').value || '').trim() || 'My Toy').slice(0, 14), src: state.pendingPhoto, kind: 'photo' };
  state.myToys.push(t);
  if (!saveMyToys(state.myToys)) toast('This toy will stay until you close the app');
  state.toy = t; show('explorer');
});
$('nameCancel').addEventListener('click', () => show('toys'));

/* ---------- World Explorer ---------- */
function drawExplorer() {
  const g = $('worldGrid'); g.innerHTML = '';
  $('explorerToy').src = state.toy ? state.toy.src : '';
  state.registry.worlds.forEach((w, i) => {
    const ready = !!w.data;
    const b = document.createElement('button'); b.type = 'button'; b.className = 'card world-card' + (ready ? '' : ' soon');
    b.style.setProperty('--t0', w.tone[0]); b.style.setProperty('--t1', w.tone[1]);
    b.setAttribute('aria-label', ready ? w.name : `${w.name}, coming soon`);
    const img = document.createElement('img'); img.alt = ''; img.loading = i < 6 ? 'eager' : 'lazy'; img.decoding = 'async'; img.src = w.thumb;
    img.onerror = () => img.remove();
    const label = document.createElement('b'); label.textContent = w.name;
    b.append(img, label);
    if (!ready) { const s = document.createElement('span'); s.className = 'soon-badge'; s.innerHTML = `${ICONS.sparkle}<span>Soon</span>`; b.appendChild(s); }
    b.addEventListener('click', () => ready ? enterWorld(w) : (speak(`${w.name} is coming soon!`), toast(`${w.name} is coming soon`)));
    g.appendChild(b);
  });
}

/* ---------- inside a world ---------- */
const viewer = new WorldViewer($('stage'), { onEvent: onWorldEvent, speak });

async function enterWorld(entry) {
  if (!state.toy) { show('toys'); return; }
  const w = await loadWorld(entry);
  state.world = w; state.journal = [];
  state.time = 'day'; state.weather = 'sunny';
  show('world');
  drawHud();
  await viewer.open(w, state.toy, { time: state.time, weather: state.weather });
}

function onWorldEvent(ev) {
  if (ev.type === 'enter') {
    if (!state.journal.some(j => j.type === 'enter' && j.location === ev.location)) state.journal.push({ ...ev, text: `${state.toy.name} went to the ${ev.name}.` });
    const L = viewer.L;
    if (L && L.defaultTime && state.time === 'day') { /* keep child's choice; default only hints */ }
    drawPlaces();
  } else {
    state.journal.push(ev);
  }
  if (ev.type === 'discover') { flyToBag(ev); drawBag(); }
}

function drawHud() {
  drawPlaces(); drawBag();
  $('timeBtn').innerHTML = TIME_ICONS[state.time];
  $('weatherBtn').innerHTML = WEATHER_ICONS[state.weather];
}
function drawPlaces() {
  const box = $('places'); box.innerHTML = '';
  const w = state.world; if (!w) return;
  const seen = new Set(state.journal.filter(j => j.type === 'enter').map(j => j.location));
  w.locations.forEach(L => {
    const d = document.createElement('i');
    d.className = (viewer.L && viewer.L.id === L.id ? 'here ' : '') + (seen.has(L.id) ? 'seen' : '');
    d.title = L.name; box.appendChild(d);
  });
}
function totalFinds() { return state.world.locations.reduce((n, L) => n + (L.discoveries || []).length, 0); }
function drawBag() {
  const found = state.journal.filter(j => j.type === 'discover');
  $('bagCount').textContent = `${found.length}/${totalFinds()}`;
  const list = $('bagList'); list.innerHTML = '';
  if (!found.length) { list.innerHTML = '<p class="bag-empty">Explore to find hidden treasures!</p>'; return; }
  found.forEach(f => { const s = document.createElement('span'); s.className = 'bag-item'; s.innerHTML = ICONS[f.item] || ICONS.sparkle; s.title = f.text; list.appendChild(s); });
}
function flyToBag(ev) {
  const to = $('bagBtn').getBoundingClientRect(), r = ev.rect;
  const f = document.createElement('span'); f.className = 'flyer'; f.innerHTML = ICONS[ev.item] || ICONS.sparkle;
  f.style.left = r.left + 'px'; f.style.top = r.top + 'px';
  document.body.appendChild(f);
  requestAnimationFrame(() => { f.style.transform = `translate(${to.left - r.left}px, ${to.top - r.top}px) scale(.6)`; f.style.opacity = '0.2'; });
  setTimeout(() => { f.remove(); $('bagBtn').classList.add('bump'); setTimeout(() => $('bagBtn').classList.remove('bump'), 400); }, 800);
}

const TIME_ORDER = ['morning', 'day', 'sunset', 'night'];
const WEATHER_ORDER = ['sunny', 'cloudy', 'rain', 'fog'];
const TIME_ICONS = {
  morning: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M4 22h24" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M9 22a7 7 0 0114 0" fill="#ffc46b"/></svg>',
  day: '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="6" fill="#ffd24a"/><g stroke="#ffd24a" stroke-width="2.4" stroke-linecap="round"><path d="M16 3v4M16 25v4M3 16h4M25 16h4M7 7l3 3M22 22l3 3M25 7l-3 3M7 25l3-3"/></g></svg>',
  sunset: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M8 21a8 8 0 0116 0" fill="#ff8a4a"/><path d="M4 21h24M8 26h16" stroke="#ffb07a" stroke-width="2.4" stroke-linecap="round"/></svg>',
  night: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M21 5a11 11 0 1 0 6 18A9 9 0 0 1 21 5z" fill="#f2ecc8"/><circle cx="9" cy="8" r="1.2" fill="#fff"/></svg>'
};
const WEATHER_ICONS = {
  sunny: '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="13" cy="13" r="6" fill="#ffd24a"/><path d="M13 3v2.5M3 13h2.5M6 6l1.8 1.8M20 6l-1.8 1.8" stroke="#ffd24a" stroke-width="2.2" stroke-linecap="round"/><path d="M15 27a4.5 4.5 0 010-9 6 6 0 0111.5 1.6A3.7 3.7 0 0126 27z" fill="#fff" opacity=".9"/></svg>',
  cloudy: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M9 24a6 6 0 010-12 8 8 0 0115 2 5 5 0 010 10z" fill="#e9eef3"/></svg>',
  rain: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M9 19a6 6 0 010-12 8 8 0 0115 2 5 5 0 010 10z" fill="#d5dde6"/><path d="M11 23l-2 5M17 23l-2 5M23 23l-2 5" stroke="#8fc3f0" stroke-width="2.4" stroke-linecap="round"/></svg>',
  fog: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 11h22M3 16h26M6 21h20M9 26h14" stroke="#e9eef3" stroke-width="2.6" stroke-linecap="round"/></svg>'
};

$('timeBtn').addEventListener('click', () => {
  const opts = state.world.timeOfDay || TIME_ORDER;
  state.time = opts[(opts.indexOf(state.time) + 1) % opts.length];
  viewer.setTime(state.time); $('timeBtn').innerHTML = TIME_ICONS[state.time];
});
$('weatherBtn').addEventListener('click', () => {
  const opts = (state.world.weather || WEATHER_ORDER).filter(w => WEATHER_ICONS[w]);
  state.weather = opts[(opts.indexOf(state.weather) + 1) % opts.length];
  viewer.setWeather(state.weather); $('weatherBtn').innerHTML = WEATHER_ICONS[state.weather];
});
$('bagBtn').addEventListener('click', () => { $('bag').hidden = !$('bag').hidden; });
$('bagClose').addEventListener('click', () => { $('bag').hidden = true; });
$('worldBack').addEventListener('click', () => show('explorer'));
$('fullBtn').addEventListener('click', async () => {
  const st = $('worldWrap');
  try { if (document.fullscreenElement) await document.exitFullscreen(); else await st.requestFullscreen(); } catch (e) { toast('Full screen is not available here'); }
});

/* ---------- Create Story: replay the adventure ---------- */
let storyTimer = 0, storyOn = false;
$('storyBtn').addEventListener('click', () => storyOn ? stopStory() : playStory());
async function playStory() {
  const moments = state.journal.filter(j => j.text && j.pos);
  if (moments.length < 2) { const m = `Explore a little more, then we can make ${state.toy.name}'s story!`; toast(m); speak(m); return; }
  storyOn = true; document.body.classList.add('story-mode'); $('storyBtn').setAttribute('aria-pressed', 'true');
  const intro = `${state.toy.name}'s adventure in the ${state.world.name}`;
  $('storyTitle').textContent = intro; $('storyTitle').hidden = false; speak(intro);
  await new Promise(r => { storyTimer = setTimeout(r, 2600); });
  $('storyTitle').hidden = true;
  for (const m of moments) {
    if (!storyOn) return;
    await viewer.showMoment(m);
    await new Promise(r => { storyTimer = setTimeout(r, 4800); });
  }
  if (!storyOn) return;
  $('storyTitle').textContent = 'The End'; $('storyTitle').hidden = false; speak('The End');
  await new Promise(r => { storyTimer = setTimeout(r, 2600); });
  stopStory();
}
function stopStory() {
  storyOn = false; clearTimeout(storyTimer); hush();
  document.body.classList.remove('story-mode'); $('storyTitle').hidden = true; $('storyBtn').setAttribute('aria-pressed', 'false');
}

/* ---------- grown-ups (press and hold) ---------- */
(() => {
  const b = $('grownBtn'); let t0 = 0, raf = 0;
  const stop = () => { cancelAnimationFrame(raf); b.style.setProperty('--held', '0%'); t0 = 0; };
  const tick = () => { const k = (performance.now() - t0) / 1500; b.style.setProperty('--held', Math.min(100, k * 100) + '%'); if (k >= 1) { stop(); show('grown'); } else raf = requestAnimationFrame(tick); };
  b.addEventListener('pointerdown', e => { e.preventDefault(); t0 = performance.now(); raf = requestAnimationFrame(tick); });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => b.addEventListener(ev, stop));
  b.addEventListener('click', () => { if (!t0) toast('Grown-ups: press and hold'); });
  b.addEventListener('keydown', e => { if (e.key === 'Enter' && e.repeat) show('grown'); });
})();
$('optVoice').checked = prefs.voice; $('optSound').checked = prefs.sound;
$('optVoice').addEventListener('change', e => { prefs.voice = e.target.checked; store.set('imaloo.voice', prefs.voice); if (!prefs.voice) hush(); });
$('optSound').addEventListener('change', e => { prefs.sound = e.target.checked; store.set('imaloo.sound', prefs.sound); Sound.enabled = prefs.sound; });
$('clearBtn').addEventListener('click', () => { $('clearConfirm').hidden = false; });
$('clearNo').addEventListener('click', () => { $('clearConfirm').hidden = true; });
$('clearYes').addEventListener('click', () => { state.myToys = []; saveMyToys([]); if (state.toy && state.toy.kind === 'photo') state.toy = null; $('clearConfirm').hidden = true; toast('Deleted'); });
$('grownBack').addEventListener('click', () => show('home'));

/* ---------- navigation ---------- */
$('logo').addEventListener('click', () => show('home'));
$('playBtn').addEventListener('click', () => show('toys'));
$('toysBack').addEventListener('click', () => show('home'));
$('explorerBack').addEventListener('click', () => show('toys'));

/* ---------- start ---------- */
(async () => {
  try { await loadRegistry(); }
  catch (e) { toast('The worlds could not load. Check the connection and try again.'); return; }
  show('home');
  if ('serviceWorker' in navigator && location.protocol === 'https:' && window.top === window) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
})();
