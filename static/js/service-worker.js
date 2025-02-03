const CACHE_NAME = "django-offline-cache-v1";
const urlsToCache = [
    "/",
    "/offline/",  // Your offline fallback page
    "/static/css/styles.css",  // Add important CSS
    "/static/js/main.js",  // Add essential JS
];

// Install service worker and cache files
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

// Serve cached content when offline
self.addEventListener("fetch", (event) => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
