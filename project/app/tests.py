from django.test import TestCase, RequestFactory, Client
import unittest
from django.urls import reverse
from .models import Offer, Event, Location, Sport
from .views import offers_view, add_to_cart, calculate_discounted_price, cart_view
from .forms import EventFilterForm, OfferForm
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware



class OffersViewTestCase(TestCase):

    def test_invalid_form(self):
        # Création d'une requête GET avec un formulaire invalide
        data = {'city': 'Invalid City', 'sport': 'Invalid Sport'}
        request = RequestFactory().get(reverse('offers_view'), data)
        form = EventFilterForm(data)

        # Appel de la vue offers_view avec la requête et le formulaire invalide
        response = offers_view(request)

        # Vérification du statut de réponse
        self.assertEqual(response.status_code, 200)

        # Vérification du contenu de la page pour une réponse invalide
        self.assertContains(response, 'Offres')
        self.assertNotContains(response, 'Test Offer')
        
class AddToCartViewTestCase(TestCase):
    def test_add_to_cart(self):
        # Créer une requête POST avec les données nécessaires
        data = {
            'event_id': 1,
            'offer_id': 1,
            'adult_ticket': 2,
            'child_ticket': 1,
        }
        request = RequestFactory().post(reverse('add_to_cart'), data)
        
        # Initialiser le middleware de session avec une fonction get_response
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()

        # Appeler la vue add_to_cart avec la requête
        response = add_to_cart(request)

        # Vérifier si la réponse est une redirection
        self.assertTrue(response.status_code, 302)

        # Vérifier si la redirection est effectuée vers cart_view
        self.assertEqual(response.url, reverse('cart_view'))

        # Vérifier si les données ont été ajoutées correctement à la session
        cart = request.session.get('cart')
        self.assertIsNotNone(cart)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]['event'], '1')
        self.assertEqual(cart[0]['offer'], '1')
        self.assertEqual(cart[0]['adults'], '2')
        self.assertEqual(cart[0]['children'], '1')

class CalculateDiscountedPriceTestCase(unittest.TestCase):
    def test_valid_discount(self):
        price = 100
        discount = 20
        discounted_price = calculate_discounted_price(price, discount)
        self.assertEqual(discounted_price, 80)

    def test_discount_greater_than_100(self):
        price = 100
        discount = 150
        with self.assertRaises(ValueError):
            calculate_discounted_price(price, discount)

    def test_negative_discount(self):
        price = 100
        discount = -20
        with self.assertRaises(ValueError):
            calculate_discounted_price(price, discount)

    def test_null_price(self):
        price = None
        discount = 20
        with self.assertRaises(ValueError):
            calculate_discounted_price(price, discount)

    def test_null_discount(self):
        price = 100
        discount = None
        with self.assertRaises(ValueError):
            calculate_discounted_price(price, discount)

    def test_null_price_and_discount(self):
        price = None
        discount = None
        with self.assertRaises(ValueError):
            calculate_discounted_price(price, discount)

if __name__ == '__main__':
    unittest.main()


class CartViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_empty_cart(self):
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Votre panier est vide.')  # Assurez-vous que ce texte est présent dans la réponse

if __name__ == '__main__':
    unittest.main()
    

class RemoveFromCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_remove_item_index(self):
        # Ajoutez des éléments au panier
        self.client.post(reverse('add_to_cart'), {'event_id': 1, 'offer_id': 1, 'adult_ticket': 2, 'child_ticket': 1})
        # Testez la suppression
        response = self.client.post(reverse('remove_from_cart'), {'item_index': 0})
        # Assurez-vous que l'élément a été supprimé du panier et que la redirection vers la vue du panier a été effectuée
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(response.client.session['cart']), 0)

    def test_get_request(self):
        # Effectuez une demande GET à la vue remove_from_cart
        response = self.client.get(reverse('remove_from_cart'))
        
        # Assurez-vous que la redirection vers la vue du panier a été effectuée
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart_view'))