document.addEventListener('DOMContentLoaded', function() {
    updateCartUI();
});

function addToCart() {
    const eventID = document.getElementById('active_event').getAttribute('data-event-id');
    const offerID = document.getElementById('offer-type').value;
    const adultNumber = parseInt(document.getElementById('adult_ticket').value);
    const childNumber = parseInt(document.getElementById('child_ticket').value);
    const totalPrice = document.getElementById('total_price_display').textContent;

    const cartItem = {
        eventID,
        offerID,
        adultNumber,
        childNumber,
        totalPrice
    };

    addCartItemToStorage(cartItem);
    updateCartUI();
    return false; // Pour éviter la soumission réelle du formulaire
}

function addCartItemToStorage(item) {
    let cart = localStorage.getItem('shoppingCart') || '[]'; // Default to empty array in JSON if null
    cart = JSON.parse(cart);
    cart.push(item);
    localStorage.setItem('shoppingCart', JSON.stringify(cart));
}

function updateCartUI() {
    const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
    const cartElement = document.getElementById('cart_items');
    cartElement.innerHTML = ''; // Clear previous content

    cart.forEach((item, index) => {
        cartElement.innerHTML += `<div>Article ${index + 1}: Adultes: ${item.adultNumber}, Enfants: ${item.childNumber}, Total: ${item.totalPrice} €</div>`;
    });
}


