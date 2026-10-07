// Small picture icons so children can play without reading.
// Actions use white line drawings; found items use simple coloured shapes.
const s = (body, vb = '0 0 32 32') => `<svg viewBox="${vb}" aria-hidden="true" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;
const f = body => `<svg viewBox="0 0 32 32" aria-hidden="true">${body}</svg>`;

export const ICONS = {
  // movement and actions
  steps: s('<ellipse cx="11" cy="20" rx="3.6" ry="5.5"/><ellipse cx="21" cy="11" rx="3.6" ry="5.5"/><path d="M11 28v.5M21 19v.5"/>'),
  jump: s('<path d="M5 25q11-22 22 0"/><path d="M22 20l5 5 1-6"/>'),
  hop: s('<path d="M4 24q5-10 9 0q5-10 9 0q4-8 7-1"/>'),
  splash: s('<path d="M16 6c-5 7-7 10-7 13a7 7 0 0014 0c0-3-2-6-7-13z"/><path d="M5 9l2 3M27 9l-2 3"/>'),
  sit: s('<path d="M7 20h18v5M7 20v5M10 20v-8h12v8"/>'),
  peek: s('<path d="M3 16s5-8 13-8 13 8 13 8-5 8-13 8S3 16 3 16z"/><circle cx="16" cy="16" r="3.5"/>'),
  climb: s('<path d="M10 28V4M22 28V4M10 10h12M10 17h12M10 24h12"/>'),
  wonder: s('<path d="M16 4l2.6 7.4L26 14l-7.4 2.6L16 24l-2.6-7.4L6 14l7.4-2.6z"/>'),
  sparkle: s('<path d="M16 4l2.6 7.4L26 14l-7.4 2.6L16 24l-2.6-7.4L6 14l7.4-2.6z"/>'),
  slide: s('<path d="M5 8q10 2 16 12t6 6"/><path d="M5 27h22"/>'),
  walk: s('<ellipse cx="11" cy="20" rx="3.6" ry="5.5"/><ellipse cx="21" cy="11" rx="3.6" ry="5.5"/>'),
  build: s('<path d="M6 26h20V14h-4v-4h-3v4h-6v-4h-3v4H6z"/><path d="M14 26v-5h4v5"/>'),
  knock: s('<rect x="8" y="4" width="16" height="24" rx="2"/><circle cx="20" cy="16" r="1.2"/>'),
  lights: s('<path d="M3 8q13 10 26 0"/><circle cx="8" cy="12" r="2"/><circle cx="16" cy="14" r="2"/><circle cx="24" cy="12" r="2"/>'),
  wave: s('<path d="M11 18V8a2 2 0 014 0v8M15 15V6a2 2 0 014 0v10M19 15V8a2 2 0 014 0v10q0 9-8 9-5 0-8-6l-3-5a2 2 0 013-2l3 3"/>'),
  dig: s('<path d="M20 4l8 8M24 8L12 20"/><path d="M6 26l6-6 3 3-6 6z"/>'),
  smell: s('<circle cx="16" cy="12" r="4"/><circle cx="16" cy="12" r="9" stroke-dasharray="3 4"/><path d="M16 21v8"/>'),
  build2: '',
  // found things
  footprints: f('<g fill="#6b4a2a"><ellipse cx="10" cy="21" rx="3.5" ry="4.5"/><ellipse cx="22" cy="12" rx="3.5" ry="4.5"/><circle cx="6.5" cy="15" r="1.4"/><circle cx="9" cy="13.5" r="1.4"/><circle cx="12" cy="13.8" r="1.4"/><circle cx="18.5" cy="6" r="1.4"/><circle cx="21" cy="4.5" r="1.4"/><circle cx="24" cy="4.8" r="1.4"/></g>'),
  feather: f('<path d="M24 4C12 8 7 18 8 28c8-3 15-11 16-24z" fill="#b8a07a"/><path d="M8 28L22 8" stroke="#6b5a40" stroke-width="1.4"/>'),
  pebble: f('<ellipse cx="16" cy="18" rx="11" ry="8" fill="#8f9aa3"/><path d="M8 16q8-4 16 2" stroke="#e8edf0" stroke-width="2" fill="none"/>'),
  frog: f('<ellipse cx="16" cy="20" rx="10" ry="7" fill="#5aa04a"/><circle cx="11" cy="12" r="4" fill="#5aa04a"/><circle cx="21" cy="12" r="4" fill="#5aa04a"/><circle cx="11" cy="12" r="1.6" fill="#1d2a14"/><circle cx="21" cy="12" r="1.6" fill="#1d2a14"/>'),
  gumnut: f('<path d="M9 12h14l-2 12a5 5 0 01-10 0z" fill="#7a5a36"/><rect x="8" y="9" width="16" height="4" rx="2" fill="#5a4026"/>'),
  map: f('<path d="M4 8l8-3 8 3 8-3v19l-8 3-8-3-8 3z" fill="#e8d3a2"/><path d="M8 20q5-8 9-2t7-6" stroke="#a5482f" stroke-width="1.6" fill="none" stroke-dasharray="2 2"/><path d="M22 10l3 3m0-3l-3 3" stroke="#a5482f" stroke-width="1.8"/>'),
  cave: f('<path d="M3 27q2-20 13-20t13 20z" fill="#7d776c"/><path d="M10 27q1-11 6-11t6 11z" fill="#2b2622"/>'),
  dragonfly: f('<path d="M16 6v22" stroke="#2d6fa8" stroke-width="2.4"/><g fill="#9cd3f2" opacity=".85"><ellipse cx="9" cy="11" rx="7" ry="2.6"/><ellipse cx="23" cy="11" rx="7" ry="2.6"/><ellipse cx="10" cy="16" rx="6" ry="2.2"/><ellipse cx="22" cy="16" rx="6" ry="2.2"/></g>'),
  shell: f('<path d="M16 4C8 4 4 14 6 24l10 4 10-4c2-10-2-20-10-20z" fill="#f2b9a8"/><path d="M16 5v22M11 7l2 20M21 7l-2 20M7 13l7 14M25 13l-7 14" stroke="#c97f6c" stroke-width="1.2"/>'),
  lizard: f('<path d="M6 22q4-6 10-4t10-6q-2 6-8 8t-12 2z" fill="#9a8a4a"/><circle cx="24" cy="13" r="1" fill="#222"/>'),
  starfish: f('<path d="M16 3l3.5 9.5 10 .5-8 6.5 3 10L16 23.5 7.5 29.5l3-10-8-6.5 10-.5z" fill="#ef8a3a"/>'),
  bottle: f('<rect x="11" y="9" width="10" height="19" rx="4" fill="#9ccfc4" opacity=".9"/><rect x="13.5" y="3" width="5" height="7" rx="1.5" fill="#a87a4a"/><rect x="13" y="14" width="6" height="8" fill="#f5ecd6"/>'),
  anemone: f('<ellipse cx="16" cy="24" rx="10" ry="4" fill="#c24a6a"/><g stroke="#ef7a9a" stroke-width="2.4" stroke-linecap="round"><path d="M8 22q-2-8 0-12M12 21q-1-9 1-14M16 21V6M20 21q1-9-1-14M24 22q2-8 0-12"/></g>'),
  pearl: f('<path d="M4 18q12 14 24 0z" fill="#d9c6b4"/><circle cx="16" cy="15" r="5" fill="#f7f3ee"/><circle cx="14.5" cy="13.5" r="1.5" fill="#fff"/>'),
  ball: f('<circle cx="16" cy="16" r="11" fill="#e8483a"/><path d="M6 12q10 6 20 0M6 20q10-6 20 0" stroke="#ffd34d" stroke-width="2.4" fill="none"/>'),
  ladybird: f('<ellipse cx="16" cy="18" rx="10" ry="9" fill="#d8322a"/><path d="M16 9v18" stroke="#1b1b1b" stroke-width="1.6"/><circle cx="16" cy="9" r="4.5" fill="#1b1b1b"/><g fill="#1b1b1b"><circle cx="11" cy="16" r="2"/><circle cx="21" cy="16" r="2"/><circle cx="12" cy="23" r="1.8"/><circle cx="20" cy="23" r="1.8"/></g>'),
  book: f('<path d="M4 7q6-2 12 1v19q-6-3-12-1z" fill="#3f6fb0"/><path d="M28 7q-6-2-12 1v19q6-3 12-1z" fill="#5a8fd0"/><circle cx="22" cy="14" r="3" fill="#ffe08a"/>'),
  key: f('<circle cx="10" cy="16" r="6" fill="none" stroke="#d6a72c" stroke-width="3"/><path d="M16 16h12M24 16v5M28 16v4" stroke="#d6a72c" stroke-width="3" stroke-linecap="round"/>'),
  snail: f('<path d="M3 24h22q4 0 4-4" stroke="#b3a184" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="14" cy="16" r="8" fill="#c9883e"/><path d="M14 16m-4 0a4 4 0 108 0 3 3 0 10-5 0" stroke="#8a5420" stroke-width="1.6" fill="none"/>'),
  fossil: f('<path d="M5 20q0-10 11-10t11 10" stroke="#e7dcc6" stroke-width="5" stroke-linecap="round" fill="none"/><circle cx="5" cy="21" r="3" fill="#e7dcc6"/><circle cx="27" cy="21" r="3" fill="#e7dcc6"/>')
};
