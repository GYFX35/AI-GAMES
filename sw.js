const CACHE_NAME = 'game-portal-cache-v1';
const URLS_TO_CACHE = [
  '/',
  '/index.html',
  '/style.css',
  '/ai_mmo_games.html',
  '/manga_games.html',
  '/casino_games.html',
  '/global_gambles.html',
  '/forums.html',
  '/affiliates.html',
  '/esport_games.html',
  '/instant_games.html',
  '/partnerships.html',
  '/camera_features.html',
  // Add other important pages/assets if any
  // Note: Icon paths from manifest.json should also be cached if they are critical for offline display.
  // e.g., '/icons/icon-192x192.png', '/icons/icon-512x512.png'
  // However, ensure these files exist or the install step will fail.
];

// Install a service worker
self.addEventListener('install', event => {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        // Add all URLs to cache. If any request fails, the service worker installation will fail.
        return cache.addAll(URLS_TO_CACHE.map(url => new Request(url, {cache: 'reload'})));
      })
      .catch(err => {
        console.error('Failed to open cache or add URLs during install:', err);
      })
  );
});

// Cache and return requests
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        // Not found in cache, try to fetch from network
        return fetch(event.request).then(
          networkResponse => {
            // Check if we received a valid response
            if(!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              return networkResponse;
            }

            // IMPORTANT: Clone the response. A response is a stream
            // and because we want the browser to consume the response
            // as well as the cache consuming the response, we need
            // to clone it so we have two streams.
            const responseToCache = networkResponse.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return networkResponse;
          }
        ).catch(error => {
          console.log('Fetch failed; returning offline page instead.', error);
          // Optionally, return a specific offline fallback page if a fetch fails
          // For example, if event.request.mode === 'navigate'
          // return caches.match('/offline.html');
        });
      })
  );
});

// Update a service worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME]; // Keep only the current cache
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
