// Toys: the built-in lifelike toys plus toys a child photographs.
// A photographed toy has its background removed on the device (nothing is uploaded),
// so it can stand inside a world instead of looking like a square sticker.

export const BUILT_IN = [
  { id: 'teddy', name: 'Teddy', src: 'toys/teddy.png', kind: 'builtin' },
  { id: 'pony', name: 'Pony', src: 'toys/pony.png', kind: 'builtin' },
  { id: 'doll', name: 'Dolly', src: 'toys/doll.png', kind: 'builtin' }
];

const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
};

export function loadMyToys() { return store.get('imaloo.toys.v2', []); }
export function saveMyToys(list) { return store.set('imaloo.toys.v2', list); }

/**
 * Remove a plain background from a toy photo.
 * Samples the border colour, flood-fills similar pixels from the edges,
 * feathers the edge and crops to the toy. Works best on a plain floor or wall.
 */
export async function cutOutToy(file, max = 640) {
  const img = await loadFile(file);
  const scale = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
  const w = Math.round(img.naturalWidth * scale), h = Math.round(img.naturalHeight * scale);
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  const c = cv.getContext('2d', { willReadFrequently: true });
  c.drawImage(img, 0, 0, w, h);
  const id = c.getImageData(0, 0, w, h), d = id.data;

  // Border colour statistics.
  const samples = [];
  for (let x = 0; x < w; x += 4) { samples.push(px(d, w, x, 0), px(d, w, x, h - 1)); }
  for (let y = 0; y < h; y += 4) { samples.push(px(d, w, 0, y), px(d, w, w - 1, y)); }
  const tol = 46;
  const isBg = i => {
    const r = d[i], g = d[i + 1], b = d[i + 2];
    for (let k = 0; k < samples.length; k += 3) {
      const s = samples[k];
      if (Math.abs(r - s[0]) + Math.abs(g - s[1]) + Math.abs(b - s[2]) < tol) return true;
    }
    return false;
  };

  const mask = new Uint8Array(w * h); // 1 = background
  const stack = [];
  for (let x = 0; x < w; x++) { stack.push(x, x + (h - 1) * w); }
  for (let y = 0; y < h; y++) { stack.push(y * w, w - 1 + y * w); }
  while (stack.length) {
    const p = stack.pop();
    if (mask[p]) continue;
    if (!isBg(p * 4)) continue;
    mask[p] = 1;
    const x = p % w, y = (p / w) | 0;
    if (x > 0) stack.push(p - 1); if (x < w - 1) stack.push(p + 1);
    if (y > 0) stack.push(p - w); if (y < h - 1) stack.push(p + w);
  }

  // If almost nothing was removed (busy background), fall back to a soft oval.
  let removed = 0; for (let i = 0; i < mask.length; i++) removed += mask[i];
  const frac = removed / mask.length;
  let minX = w, minY = h, maxX = 0, maxY = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const p = x + y * w;
    let a;
    if (frac < 0.12) {
      const dx = (x - w / 2) / (w * 0.46), dy = (y - h / 2) / (h * 0.48), r = Math.sqrt(dx * dx + dy * dy);
      a = r < 0.85 ? 255 : r > 1 ? 0 : Math.round(255 * (1 - (r - 0.85) / 0.15));
    } else {
      let n = 0; // feather: count background neighbours
      for (let oy = -1; oy <= 1; oy++) for (let ox = -1; ox <= 1; ox++) {
        const xx = x + ox, yy = y + oy;
        if (xx < 0 || yy < 0 || xx >= w || yy >= h || mask[xx + yy * w]) n++;
      }
      a = mask[p] ? 0 : Math.round(255 * (1 - n / 12));
    }
    d[p * 4 + 3] = a;
    if (a > 40) { if (x < minX) minX = x; if (x > maxX) maxX = x; if (y < minY) minY = y; if (y > maxY) maxY = y; }
  }
  c.putImageData(id, 0, 0);
  if (maxX <= minX || maxY <= minY) { minX = 0; minY = 0; maxX = w - 1; maxY = h - 1; }
  const out = document.createElement('canvas');
  out.width = maxX - minX + 1; out.height = maxY - minY + 1;
  out.getContext('2d').drawImage(cv, minX, minY, out.width, out.height, 0, 0, out.width, out.height);
  return { src: out.toDataURL('image/png'), clean: frac >= 0.12 };
}

function px(d, w, x, y) { const i = (x + y * w) * 4; return [d[i], d[i + 1], d[i + 2]]; }
function loadFile(file) {
  return new Promise((res, rej) => {
    const url = URL.createObjectURL(file), im = new Image();
    im.onload = () => { URL.revokeObjectURL(url); res(im); };
    im.onerror = () => { URL.revokeObjectURL(url); rej(new Error('That picture could not be opened.')); };
    im.src = url;
  });
}
