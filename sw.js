// Offline cache for IMALOO. Photos, toys and world data are cache-first (they rarely
// change and are the heavy part); the app shell is network-first so updates show up.
const CACHE = 'imaloo-v2';
const SHELL = ['./', 'index.html', 'css/app.css', 'js/app.js', 'js/viewer.js', 'js/effects.js', 'js/sound.js', 'js/toys.js', 'js/icons.js', 'data/worlds.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).catch(() => {}));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  const heavy = /\/(worlds|toys)\//.test(url.pathname) || /\/data\/worlds\//.test(url.pathname);
  if (heavy) {
    e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return res;
    })));
  } else {
    e.respondWith(fetch(e.request).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return res;
    }).catch(() => caches.match(e.request)));
  }
});
