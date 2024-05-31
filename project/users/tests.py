from django.test import TestCase, RequestFactory, Client
from users.forms import SignUpForm, SignInForm, PaymentForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.core.mail import outbox
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from .views import sendActivationEmail, activateAccount
from .models import CustomUser, Order
from app.models import Event, Offer, Sport, Location
from .tokens import generateToken
from django.utils import timezone

class SignUpFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'first_name': '',  # Champ requis
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_required_fields(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_email_field(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalidemail',  # Email invalide
            'password1': 'securepassword',
            'password2': 'securepassword'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


def test_save_with_commit(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword'
        }
        form = SignUpForm(data=form_data)
        user = form.save(commit=True)
        self.assertTrue(user.pk)  # Vérifie que l'utilisateur a été enregistré dans la base de données
        

class TestSendActivationEmail(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_send_activation_email(self):
        request = self.factory.get('/customer/details')
        request.user = self.user

        response = sendActivationEmail(request, self.user.id, 'test@example.com')

        self.assertEqual(response.status_code, 200)
               

class TestActivateAccount(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_activate_account(self):
        request = self.factory.get('/customer/details')
        request.user = self.user

        # Ajoutez ces deux lignes pour configurer les messages
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = generateToken.make_token(self.user)

        response = activateAccount(request, uidb64, token)

        self.assertEqual(response.status_code, 200)

class TestSignInForm(TestCase):
    def test_labels(self):
        form = SignInForm()
        self.assertEqual(form.fields['username'].label, 'Username')
        self.assertEqual(form.fields['password'].label, 'Password')
        

class TestPaymentForm(TestCase):
    def test_form_with_valid_data(self):
        form = PaymentForm({
            'account_number': '1234567890123456',
            'cardholder_name': 'John Doe',
            'expiration_date': '12/24',
            'cvc': '123'
        })
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_account_number(self):
        form = PaymentForm({
            'account_number': '1234567890',  # Numéro de compte invalide
            'cardholder_name': 'John Doe',
            'expiration_date': '12/24',
            'cvc': '123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['account_number'], ['Le numéro de compte doit contenir 16 chiffres.'])

   
class TestPaymentView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')  # Utilisez CustomUser ici
        self.sport = Sport.objects.create(name='Test Sport')  # Créez une instance de Sport
        self.event = Event.objects.create(complete_name='Test Event', standard_price=100, sport=self.sport)

    def test_payment_view_with_valid_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/payment/', {  # Remplacez '/payment/' par l'URL correcte de votre vue
            'account_number': '1234567890123456',
            'cardholder_name': 'John Doe',
            'expiration_date': '12/24',
            'cvc': '999'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/payment-success.html')

    def test_payment_view_with_invalid_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/payment/', {  
            'account_number': '1234567890',  # Numéro de compte invalide
            'cardholder_name': 'John Doe',
            'expiration_date': '12/24',
            'cvc': '123'
        })
        self.assertEqual(response.status_code, 200)
        
