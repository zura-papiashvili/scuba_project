// Add parallax effect on scroll
window.addEventListener('scroll', function () {
    const parallax = document.querySelector('.parallax');
    const scrollPosition = window.scrollY;  // Get the scroll position

    // Adjust the background position based on scroll position
    parallax.style.transition = 'background-position 0.3s ease-out';
    parallax.style.backgroundPosition = 'center ' + (scrollPosition * 0.5) + 'px';  // 0.8 is the speed factor
});


document.addEventListener("DOMContentLoaded", function () {
    const img = document.getElementById("draggable-image");

    let offsetX, offsetY, isDragging = false;

    img.addEventListener("mousedown", (e) => {
        isDragging = true;
        offsetX = e.clientX - img.offsetLeft;
        offsetY = e.clientY - img.offsetTop;
        img.style.cursor = "grabbing";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isDragging) return;
        img.style.left = `${e.clientX - offsetX}px`;
        img.style.top = `${e.clientY - offsetY}px`;
    });

    document.addEventListener("mouseup", () => {
        isDragging = false;
        img.style.cursor = "grab";
    });
    // Redirect on double click
    img.addEventListener("dblclick", () => {
        const redirectUrl = img.getAttribute("data-url");
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
    });
});