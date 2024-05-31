document.addEventListener('DOMContentLoaded', function() {
    var toggleBtn = document.querySelector('.toggle-btn');
    var openToggle = document.getElementById('open_toggle');
    var closeToggle = document.getElementById('close_toggle');
    var navbar = document.querySelector('.navbar');

    // Ajuster la visibilité initiale selon la largeur de l'écran
    var screenWidth = window.innerWidth;
    if (screenWidth < 768) { // Supposons que 768px est le point de rupture pour le responsive
        closeToggle.style.display = 'none';
        navbar.style.display = 'none';
    } else {
        openToggle.style.display = 'none';
        closeToggle.style.display = 'none'; // Assurez-vous que ce bouton est également caché sur les grands écrans
    }

    toggleBtn.addEventListener('click', function() {
        if (navbar.style.display === 'none') {
            navbar.style.display = 'flex';
            openToggle.style.display = 'none';
            closeToggle.style.display = 'flex';
        } else {
            navbar.style.display = 'none';
            openToggle.style.display = 'flex';
            closeToggle.style.display = 'none';
        }
    });
});