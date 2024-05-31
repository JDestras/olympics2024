

function updateCartUI() {
    const cart = JSON.parse(localStorage.getItem('shoppingCart')) || [];
    const cartElement = document.getElementById('cart_items');
    cartElement.innerHTML = ''; // Nettoyer l'ancien contenu

        cart.forEach((item, index) => {
            cartElement.innerHTML += `<div>Article ${index + 1}: Adultes: ${item.adultNumber}, Enfants: ${item.childNumber}, Total: ${item.totalPrice} €</div>`;
        });
    }


    

