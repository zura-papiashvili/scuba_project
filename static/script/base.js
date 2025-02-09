document.addEventListener('DOMContentLoaded', function () {
    const themeToggleButton = document.getElementById('theme-toggle');
    const bodyElement = document.body;
    const header = document.querySelector('header');
    const bgImageSection = document.querySelector('.bgimg-1'); // Ensure the background section is selected

    // Preload dark mode background to prevent flickering
    const darkBg = new Image();
    darkBg.src = '/static/landing/images/cover-dark.webp';

    function applyTheme(theme) {
        if (theme === 'dark') {
            bodyElement.classList.add('dark-mode');
            themeToggleButton.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            bodyElement.classList.remove('dark-mode');
            themeToggleButton.innerHTML = '<i class="fas fa-moon"></i>';
        }
    }

    // Apply saved theme on load
    const savedTheme = localStorage.getItem('theme');
    applyTheme(savedTheme);

    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', function () {
            const isDark = bodyElement.classList.toggle('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            applyTheme(isDark ? 'dark' : 'light');
        });
    }

    // Header fade effect on scroll (fade off when scrolling down, appear when scrolling up)
    let lastScrollY = window.scrollY;
    function handleHeaderFade() {
        const currentScrollY = window.scrollY;
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            header.classList.add('hidden');
        } else if (currentScrollY < lastScrollY) {
            header.classList.remove('hidden');
        }
        lastScrollY = currentScrollY;
    }

    let scrollTimeout;
    window.addEventListener('scroll', function () {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(handleHeaderFade, 100); // Debounce for performance
    });

    handleHeaderFade();
});
