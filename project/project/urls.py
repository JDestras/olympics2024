from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app.views import home_view, about_view, offers_view, event_offers_view, add_to_cart, cart_view, remove_from_cart, legal_view
from users.views import check_id_view, signup_view, signin_view, logout, activateAccount, sendActivationEmail, payment_view, user_account_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('about/', about_view, name='about_view'),
    path('offers/', offers_view, name='offers_view'),
    path('offers/<int:event_id>/', event_offers_view, name='event_offers_view'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('signup/', signup_view, name="signup_view"),
    path('check-id/', check_id_view, name='check_id_view'),
    path('send-email/<int:user_id>/<str:to_email>/', sendActivationEmail, name='sendActivationEmail'),
    path('activate/<uidb64>/<token>', activateAccount, name='activateAccount'),
    path('signin/', signin_view, name='signin_view'),
    path('logout/', logout, name='logout'),
    path('payment/', payment_view, name='payment_view'),
    path('user-account/', user_account_view, name='user_account_view'),
    path('legal/', legal_view, name='legal_view'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)