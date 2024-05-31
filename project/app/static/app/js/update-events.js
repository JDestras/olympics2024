document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('filter-form');
    form.addEventListener('change', function(event) {
        event.preventDefault();
        // Création de l'URL avec les paramètres
        const url = new URL(form.action);
        const params = new URLSearchParams(new FormData(form)).toString();
        url.search = params; // Ajoute les paramètres à l'URL

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Pour que Django sache qu'il s'agit d'une requête AJAX
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('event-list').innerHTML = data.html;
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données:', error);
        });
    });
});





