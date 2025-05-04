self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('ochiq-byudjet-v1').then(cache => {
            return cache.addAll([
                '/',
                '/static/css/tailwind.min.css',
                '/static/js/jquery.min.js',
                '/static/js/gsap.min.js',
                '/static/js/chart.min.js',
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});