from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from importlib import import_module
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate
from django.urls import resolve

class DualSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Vérifier si la demande est destinée à l'interface d'administration
            if resolve(request.path_info).app_name == 'admin':
                return

            # Reste du traitement pour votre site web
            request.admin_session = True
            engine = import_module(settings.SESSION_ENGINE)
            session_key = request.COOKIES.get(settings.ADMIN_SESSION_COOKIE_NAME)
            request.session = engine.SessionStore(session_key)

            if SESSION_KEY in request.session:
                user_id = request.session[SESSION_KEY]
                backend_path = request.session[BACKEND_SESSION_KEY]
                user = authenticate(request, backend=backend_path, user_id=user_id) or AnonymousUser()
            else:
                user = AnonymousUser()
            
            request.user = user
        else:
            # Si la demande n'est pas destinée à l'interface d'administration, ne rien faire
            pass

    def process_response(self, request, response):
        if hasattr(request, 'admin_session') and request.admin_session:
            request.session.save()
            response.set_cookie(settings.ADMIN_SESSION_COOKIE_NAME, request.session.session_key)
        return response


    def process_response(self, request, response):
        if hasattr(request, 'admin_session') and request.admin_session:
            request.session.save()
            response.set_cookie(settings.ADMIN_SESSION_COOKIE_NAME, request.session.session_key)
        return response




class RestrictSuperuserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            if not request.path.startswith(reverse('admin:index')):
                return redirect(reverse('admin:login'))
        
        response = self.get_response(request)
        return response

