function openModal(imgSrc) {
    document.getElementById('modalImg').src = imgSrc;
    document.getElementById('imageModal').style.display = "flex";
}

function closeModal() {
    document.getElementById('imageModal').style.display = "none";
}