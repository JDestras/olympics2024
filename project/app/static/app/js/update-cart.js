function updateQuantity(action, index, price) {
    let quantityInput = document.getElementById('quantity-' + index);
    let currentQuantity = parseInt(quantityInput.value);

    if (action === 'increment') {
        if (getTotalNumberOfItems() < 10) {
            currentQuantity += 1;
        } else {
            alert('Le nombre total d\'offres ne peut pas dépasser 10.');
            return; // Ne rien faire si la limite est atteinte
        }
    } else if (action === 'decrement' && currentQuantity > 1) {
        currentQuantity -= 1;
    }

    quantityInput.value = currentQuantity;
    document.getElementById('subtotal-' + index).textContent = (price * currentQuantity).toFixed(2) + ' €';
    localStorage.setItem('quantity-' + index, currentQuantity); // Enregistrer dans LocalStorage
    updateCartTotals();
}

window.onload = () => {
    document.querySelectorAll('.quantity').forEach((input, index) => {
        let storedQuantity = localStorage.getItem('quantity-' + index);
        if (storedQuantity) {
            input.value = storedQuantity;
            let priceElement = document.getElementById('subtotal-' + index);
            if (priceElement) {
                let price = parseFloat(priceElement.textContent.replace('€', '').trim()) / input.value;
                document.getElementById('subtotal-' + index).textContent = (price * storedQuantity).toFixed(2) + ' €';
            }
        }
    });
    updateCartTotals();
};

function getTotalNumberOfItems() {
    let quantities = document.querySelectorAll('.quantity');
    let totalItems = 0;
    quantities.forEach(quantity => {
        totalItems += parseInt(quantity.value);
    });
    return totalItems;
}

function updateCartTotals() {
    var cartItems = document.querySelectorAll('.cart-article');
    var totalItems = 0;
    var totalPrice = 0;

    cartItems.forEach(function(item, index) {
        var quantity = parseInt(document.getElementById('quantity-' + index).value);
        var priceElement = document.getElementById('subtotal-' + index);
        if (priceElement) {
            var price = parseFloat(priceElement.textContent.replace('€', '').trim());
            totalItems += quantity;
            totalPrice += price;
        }
    });

    document.getElementById('items-number').textContent = totalItems;
    document.getElementById('total-price').textContent = totalPrice.toFixed(2) + '€';
}
