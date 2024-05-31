document.querySelector('.back-to-previous').addEventListener('click', function(event) {
    event.preventDefault(); // Empêche le lien de suivre son href
    history.back(); // Revient à la page précédente
  });