// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function () {
    const themeToggleButton = document.getElementById('theme-toggle');
    const bodyElement = document.body;

    if (localStorage.getItem('theme') === 'dark') {
        bodyElement.classList.add('dark-mode');
        themeToggleButton.innerHTML = '<i class="fas fa-sun"></i>';
    }

    themeToggleButton.addEventListener('click', function () {
        bodyElement.classList.toggle('dark-mode');
        if (bodyElement.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
            themeToggleButton.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            localStorage.removeItem('theme');
            themeToggleButton.innerHTML = '<i class="fas fa-moon"></i>';
        }
    });

    // Header fade effect on scroll (fade off when scrolling down, appear when scrolling up)
    const header = document.querySelector('header');
    let lastScrollY = window.scrollY;  // Track the last scroll position

    function handleHeaderFade() {
        const currentScrollY = window.scrollY;

        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // Scrolling down and past 100px, hide the header
            header.classList.add('hidden');
        } else if (currentScrollY < lastScrollY) {
            // Scrolling up, show the header
            header.classList.remove('hidden');
        }

        lastScrollY = currentScrollY;
    }

    window.addEventListener('scroll', handleHeaderFade);
    handleHeaderFade(); // Call initially to check the scroll position
});