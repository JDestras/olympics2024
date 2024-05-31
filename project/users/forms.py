from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Une adresse e-mail valide est requise.')
    first_name = forms.CharField(max_length=30, label="Prénom")
    last_name = forms.CharField(max_length=30, label="Nom")

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # L'utilisateur est inactif par défaut
        if commit:
            user.save()
        return user

class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisez les étiquettes des champs si nécessaire
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        
class PaymentForm(forms.Form):
    account_number = forms.CharField(label='Numéro de compte', max_length=16)
    cardholder_name = forms.CharField(label='Nom du titulaire', max_length=100)
    expiration_date = forms.CharField(label='Date de validité (MM/YY)', max_length=5)
    cvc = forms.CharField(label='Code CVC', max_length=3)
    
    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if not account_number.isdigit() or len(account_number) != 16:
            raise forms.ValidationError("Le numéro de compte doit contenir 16 chiffres.")
        return account_number
    
    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        try:
            expiration_date = "01/" + expiration_date  # Ajouter "01/" devant la date
            expiration_date = datetime.strptime(expiration_date, "%d/%m/%y")
            if expiration_date < datetime.now():
                raise ValidationError("La date d'expiration doit être postérieure à aujourd'hui.")
        except ValueError:
            raise forms.ValidationError("Saisissez une date valide au format MM/YY.")
        return expiration_date

    
    def clean_cvc(self):
        cvc = self.cleaned_data.get('cvc')
        if not cvc.isdigit() or len(cvc) != 3:
            raise forms.ValidationError("Le code CVC doit contenir 3 chiffres.")
        return cvc