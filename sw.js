// ═══════════════════════════════════════════════════════════════════════
// Nómina Auditor — modo sin conexión (service worker)
// ═══════════════════════════════════════════════════════════════════════
// Solo guarda el CÓDIGO de la app (index.html, librerías y fuentes).
// Tus nóminas y tu API key siguen en el almacenamiento del navegador:
// nunca pasan por aquí ni se suben a ningún sitio.
//
// Estrategia:
//  - La app (index.html): primero la red. Con conexión siempre llega la última
//    versión publicada; sin conexión (o si la red tarda más de 4 s) se abre la
//    copia guardada. No hace falta tocar nada de este archivo para publicar
//    cambios del index.html.
//  - Librerías (cdnjs) y fuentes (Google Fonts): primero la copia guardada;
//    sus URLs llevan versión, así que no cambian.
//  - Las llamadas a Gemini (POST) y cualquier otra cosa: directas a la red.
//
// Cambia CACHE_VERSION solo si cambias este archivo o la lista de librerías.
// Las cachés se filtran por el prefijo "nomina-auditor-" porque todas las webs
// de asesorian.github.io comparten origen y no hay que tocar las de otras apps.
// ═══════════════════════════════════════════════════════════════════════

const CACHE_PREFIX = 'nomina-auditor-';
const CACHE_VERSION = CACHE_PREFIX + 'sw1';
const APP_SHELL = './';
const NETWORK_TIMEOUT_MS = 4000;
const CDN_ASSETS = [
  'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js',
  'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap'
];
const CACHE_FIRST_HOSTS = ['cdnjs.cloudflare.com', 'fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_VERSION);
    await cache.add(new Request(APP_SHELL, { cache: 'reload' }));
    // Si alguna librería no se puede descargar ahora, no bloquea: se guardará al usarla.
    await Promise.allSettled(CDN_ASSETS.map(u => cache.add(u)));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      .filter(k => k.startsWith(CACHE_PREFIX) && k !== CACHE_VERSION)
      .map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return; // Gemini y cualquier envío: siempre a la red, sin tocar

  const url = new URL(req.url);

  if (req.mode === 'navigate' && url.origin === self.location.origin) {
    const network = fetch(req).then(async res => {
      if (res.ok) {
        const cache = await caches.open(CACHE_VERSION);
        await cache.put(APP_SHELL, res.clone());
      }
      return res;
    });
    event.waitUntil(network.then(() => {}, () => {}));
    event.respondWith(networkFirst(network));
    return;
  }

  if (CACHE_FIRST_HOSTS.includes(url.hostname)) {
    event.respondWith(cacheFirst(event));
  }
});

async function networkFirst(network) {
  const cached = await caches.match(APP_SHELL, { cacheName: CACHE_VERSION });
  if (!cached) return network; // primera vez: no hay copia, se espera a la red
  const timeout = new Promise(resolve => setTimeout(resolve, NETWORK_TIMEOUT_MS, null));
  try {
    const res = await Promise.race([network, timeout]);
    return res && res.ok ? res : cached;
  } catch {
    return cached; // sin conexión
  }
}

async function cacheFirst(event) {
  const cache = await caches.open(CACHE_VERSION);
  const hit = await cache.match(event.request);
  if (hit) return hit;
  const res = await fetch(event.request);
  if (res.ok || res.type === 'opaque') event.waitUntil(cache.put(event.request, res.clone()));
  return res;
}
