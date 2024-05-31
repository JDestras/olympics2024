document.addEventListener('DOMContentLoaded', function() {
    const offerTypeSelect = document.getElementById('offer-type');
    const adultInput = document.getElementById('adult_nb');
    const childInput = document.getElementById('child_nb');
    const adultTicket = document.getElementById('adult_ticket');
    const childTicket = document.getElementById('child_ticket');
    const adultDivInput = document.getElementById('adult_nb_input');
    const childDivInput = document.getElementById('child_nb_input');

    function updateFieldsBasedOnOffer() {
        const selectedOption = offerTypeSelect.options[offerTypeSelect.selectedIndex];
        const maxAdults = parseInt(selectedOption.getAttribute('data-max-adults'), 10);
        const minAdults = parseInt(selectedOption.getAttribute('data-min-adults'), 10);
        const maxChildren = parseInt(selectedOption.getAttribute('data-max-children'), 10);
        const minChildren = parseInt(selectedOption.getAttribute('data-min-children'), 10);
        const isChildOffer = selectedOption.getAttribute('data-is-child-offer') === 'True';
    
        // Reset input values to minimums
        adultInput.min = minAdults;
        adultInput.max = maxAdults;
        adultInput.value = minAdults;
        adultTicket.value = minAdults;
    
        childInput.min = minChildren;
        childInput.max = maxChildren;
    
        // Set childTicket value based on the actual value in childInput
        childTicket.value = childInput.value;
    
        // Adjust visibility of inputs
        adultDivInput.style.display = (maxAdults === minAdults) ? 'none' : 'block';
        
        // Masquer la div contenant le champ enfant si l'offre ne dispose pas de billets enfants
        childDivInput.style.display = isChildOffer ? 'block' : 'none';
    }
    

    offerTypeSelect.addEventListener('change', updateFieldsBasedOnOffer);
    childInput.addEventListener('input', function() {
        childTicket.value = childInput.value;
    });

    updateFieldsBasedOnOffer(); // Initial setup on page load
});
