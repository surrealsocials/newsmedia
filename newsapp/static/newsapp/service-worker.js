// service-worker.js

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('my-cache')
    .then(cache => {
      return cache.addAll([
        '/',
        '/static/css/style.css',
        '/static/js/main.js'
        // Add more URLs of your static assets
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
    .then(response => {
      return response || fetch(event.request);
    })
  );
});
