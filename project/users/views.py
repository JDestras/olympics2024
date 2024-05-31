from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .forms import SignUpForm, SignInForm, PaymentForm
from . tokens import generateToken
from project import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, Order, generate_qr_code
from app.models import Event, Offer
from app.views import calculate_discounted_price



def not_superuser(user):
    return not (user.is_authenticated and user.is_superuser)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Générer le nom d'utilisateur
            username = form.cleaned_data['first_name'] + '_' + form.cleaned_data['last_name']
            user.username = username
            user.is_active = False
            user.save()
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            request.session['username'] = user.username  
            return redirect('check_id_view')  
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {
        'form': form,
        'title': "S'inscrire"
        })

def check_id_view(request):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email')
    if not user_id or not user_email:
        return redirect('signup_view')
    return render(request, 'users/check-id.html', {
        'title': 'Validation identité',
        'user_id': user_id,
        'user_email': user_email,
    })


def sendActivationEmail(request, user_id, to_email):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('signup_view')
    
    current_site = get_current_site(request)
    email_subject = "Confirm your email!"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generateToken.make_token(user)
    activation_link = f"{request.scheme}://{current_site.domain}{reverse('activateAccount', kwargs={'uidb64': uid, 'token': token})}"
    
    message = render_to_string('users/activation-email.html', {
        'name': user.first_name,
        'activation_link': activation_link
    })
    
    email = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email]
    )
    
    email.fail_silently = False
    email.send()

    return render(request, 'app/home.html', {'messages': messages.get_messages(request)})


def activateAccount(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active = True
        user.id_key = "AUTHENTICATED_USER"       
        user.save()
        messages.add_message(request, messages.SUCCESS, "Your account is activated. You can now log in.")
        return render(request, "app/home.html", {'messages': messages.get_messages(request)})
    else:
        messages.add_message(request, messages.ERROR, 'Activation failed. Please try again.')
        return render(request, 'users/signup.html', {'messages': messages.get_messages(request)})


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
    
                return redirect('cart_view')  # Rediriger vers la page d'accueil après connexion
            else:
                # Afficher un message d'erreur si l'authentification échoue
                form.add_error(None, 'Invalid username or password.')
    else:
        form = SignInForm()
    return render(request, 'users/signin.html', {
        'form': form,
        'title':'Se connecter'
        })

@login_required
def logout(request):
    django_logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home_view')

@user_passes_test(not_superuser)
@login_required
def user_view(request):
    user = request.user
    return render(request, 'base.html', {'user':user})

@user_passes_test(not_superuser)
@login_required
def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            cryptogram = form.cleaned_data.get('cvc')
            if cryptogram == '999':
                cart = request.session.get('cart', [])
                for item in cart:
                    try:
                        event = Event.objects.get(id=item['event'])
                        offer = Offer.objects.get(id=item['offer'])
                    except (Event.DoesNotExist, Offer.DoesNotExist):
                        continue

                    adults = int(item['adults'])
                    children = int(item['children'])
                    standard_price = event.standard_price
                    discount_adult = offer.discount_adult
                    discount_child = offer.discount_child
                    by_adult_price = calculate_discounted_price(standard_price, discount_adult)
                    by_child_price = calculate_discounted_price(standard_price, discount_child)
                    offer_price = adults * by_adult_price + children * by_child_price

                    Order.objects.create(
                        user=request.user,
                        event_name=event.complete_name,
                        event_sport=event.sport,
                        event_date=event.time,
                        event_location=event.location,
                        offer_name=offer.name,
                        adults=adults,
                        children=children,
                        price=offer_price,
                        payment_key='HAS_PAID'
                    )

                request.session['cart'] = []
                return render(request, 'payment/payment-success.html')
            else:
                return render(request, 'payment/payment-failed.html')
        else:
            return render(request, 'payment/payment.html', {'form': form})
    else:
        form = PaymentForm()

    total_price = request.session.get('total_price', 0)
    formatted_total_price = format(total_price, '.2f')

    return render(request, 'payment/payment.html', {'form': form, 'total_price': formatted_total_price, 'title': 'Paiement'})



@user_passes_test(not_superuser)
@login_required
def user_account_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'users/user-account.html', {
        'title': 'Compte utilisateur',
        'orders': orders,
    })
    
