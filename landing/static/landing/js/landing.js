// Add parallax effect on scroll
window.addEventListener('scroll', function () {
    const parallax = document.querySelector('.parallax');
    const scrollPosition = window.scrollY;  // Get the scroll position

    // Adjust the background position based on scroll position
    parallax.style.transition = 'background-position 0.3s ease-out';
    parallax.style.backgroundPosition = 'center ' + (scrollPosition * 0.5) + 'px';  // 0.8 is the speed factor
});