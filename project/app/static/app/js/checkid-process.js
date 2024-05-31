document.addEventListener("DOMContentLoaded", function() {
    var rules = document.querySelector('.process-rule');
    var video = document.getElementById('camera');
    var verifyButton = document.getElementById('verifyButton');
    var verificationResultInput = document.getElementById('verificationResult');
    var threeDots = document.querySelector('.three-dots');
    var checkOk = document.querySelector('.check-ok');

    // Masquer la vidéo au chargement de la page
    video.style.display = 'none';

    // Lorsque l'utilisateur clique sur le bouton "Lancer la vérification"
    verifyButton.addEventListener('click', function() {
        // Afficher la vidéo
        video.style.display = 'block';
        rules.style.display = 'none';

        // Masquer le bouton "Lancer la vérification"
        verifyButton.style.display = 'none';
        // Afficher les points de chargement
        threeDots.style.display = 'flex';

        // Attendre 4 secondes
        setTimeout(function() {
            // Masquer les points de chargement
            threeDots.style.display = 'none';
            
            // Définir verificationResult sur "success"
            verificationResultInput.value = 'success';
            
            // Afficher l'icône de vérification et le lien "Poursuivre"
            checkOk.style.display = 'block';
        }, 4000);
    });      
}); 
