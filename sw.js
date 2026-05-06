const CACHE = 'namecard-v1';
const ASSETS = [
  './',
  './index.html',
  './css/app.css',
  './js/db.js',
  './js/parser.js',
  './js/app.js',
  './manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // CDN 資源不快取（Tesseract / jsQR 語言包）
  if (e.request.url.includes('cdn.jsdelivr.net') || e.request.url.includes('tessdata')) {
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
