document.addEventListener('DOMContentLoaded', function() {
    const offerTypeSelect = document.getElementById('offer-type');
    const adultInput = document.getElementById('adult_nb');
    const childInput = document.getElementById('child_nb');
    const totalPriceDisplay = document.getElementById('total_price_display');
    const totalAdultPriceDisplay = document.getElementById('total_adult_price_display');
    const totalChildPriceDisplay = document.getElementById('total_child_price_display');
    const totalPriceDiv = document.getElementById('total_price');

    function updatePrices() {
        const selectedOption = offerTypeSelect.options[offerTypeSelect.selectedIndex];
        const discountAdult = parseFloat(selectedOption.getAttribute('data-discount-adult') || 0);
        const discountChild = parseFloat(selectedOption.getAttribute('data-discount-child') || 0);
        const standardPrice = parseFloat(document.getElementById('eventData').getAttribute('data-standard-price'));
        const adultQuantity = parseInt(adultInput.value);
        const childQuantity = parseInt(childInput.value);

        const newAdultPrice = calculateDiscountedPrice(standardPrice, discountAdult);
        const newChildPrice = calculateDiscountedPrice(standardPrice, discountChild);

        const totalAdultPrice = newAdultPrice * adultQuantity;
        const totalChildPrice = newChildPrice * childQuantity;
        const totalPrice = totalAdultPrice + totalChildPrice;

        totalAdultPriceDisplay.textContent = totalAdultPrice.toFixed(2) + ' €';
        totalChildPriceDisplay.textContent = totalChildPrice.toFixed(2) + ' €';
        totalPriceDisplay.textContent = totalPrice.toFixed(2) + ' €';

        // Vérifier si le tarif est différent de 0 ou de None
        if (totalPrice !== 0 && !isNaN(totalPrice)) {
            // Afficher la div si le tarif est différent de 0 ou de None
            totalPriceDiv.style.display = 'block';
        } else {
            // Masquer la div si le tarif est égal à 0 ou à None
            totalPriceDiv.style.display = 'none';
        }
    }

    function calculateDiscountedPrice(price, discount) {
        return price * (1 - (discount / 100));
    }

    adultInput.addEventListener('input', updatePrices);
    childInput.addEventListener('input', updatePrices);
    offerTypeSelect.addEventListener('change', updatePrices);
    updatePrices(); // Initial setup on page load
});
