from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from users.models import Order
from django.utils import timezone


class AboutJO(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nom de l'article")
    text = models.CharField(max_length=250, blank=True, verbose_name="Paragraphe")
    image = models.ImageField(upload_to="about/", blank=True, null=True, verbose_name="Image")
    image_description = models.CharField(max_length=100, blank=True, verbose_name="Description de l'image")
    image_credit = models.CharField(max_length=100, blank=True, verbose_name="Crédit")

    class Meta:
        verbose_name = ("À propos des JO")
        verbose_name_plural = ("À propos des JO")
        
    def __str__(self):
        return self.name

class Legal(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nom de la version")
    editor_name = models.CharField(max_length=255, blank=True, default="Webnoa", verbose_name="Nom de l'éditeur")
    editor_website = models.URLField(max_length=200, blank=True, default="www.webnoa.fr", verbose_name="Site web de l'éditeur")
    utilisation = models.CharField(max_length=255, blank=True, default="Utilisation par le Temple Saint-Etienne", verbose_name="Utilisation")
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.active:
            # Définir tous les autres enregistrements comme non actifs
            Legal.objects.filter(active=True).update(active=False)
            # Note: Ce code désactivera toutes les autres instances, y compris celle qui était précédemment active.
        super(Legal, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = ("Mentions légales")
        verbose_name_plural = ("Mentions légales")
        
    def __str__(self):
        return self.name 

class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de l'emplacement")
    city = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Site"

    def __str__(self):
        return self.name

class Sport(models.Model):
    name = models.CharField(max_length=100, verbose_name="Intitulé")
    
    class Meta:
        verbose_name = "Sport"
    
    def __str__(self):
        return self.name  
         
class Event(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name="Nom de l'épreuve")
    CHOICES = [
        ('a', ''),
        ('b', 'féminin'),
        ('c', 'masculin'),
    ]
    genre = models.CharField(max_length=10, choices=CHOICES, default='a', verbose_name="Genre")
    complete_name = models.CharField(max_length=200, blank=True, verbose_name="Épreuve")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='events', verbose_name="Sport")
    time = models.DateTimeField(default=timezone.now, verbose_name="Date et horaire de début")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, related_name='events', verbose_name="Lieu de l'épreuve")
    standard_price = models.PositiveIntegerField(default=15, verbose_name="prix standard en €")
    
    class Meta:
        verbose_name = "Épreuve"
        
    def save(self, *args, **kwargs):
        self.complete_name = f"{self.name} {self.get_genre_display()}".strip()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.complete_name
    
    
    
class Offer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Intitulé")
    description = models.TextField(blank=True, verbose_name="Description de l'offre")
    max_adult = models.IntegerField(default=0, verbose_name="Nombre max de tickets adulte auquel l'offre ouvre droit")
    min_adult = models.IntegerField(default=0, verbose_name="Nombre min de tickets adulte pour disposer de l'offre")
    discount_adult = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="Remise sur le ticket adulte (%)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    with_child = models.BooleanField(default=False , verbose_name="Cette offre propose des tickets enfants")
    max_child = models.IntegerField(default=0, verbose_name="Nombre max de tickets enfant auquel l'offre ouvre droit")
    min_child = models.IntegerField(default=0, verbose_name="Nombre min de tickets enfant pour disposer de l'offre")
    discount_child = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="Remise sur le ticket enfant (%)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
        
    class Meta:
        verbose_name = "Offre"
    
    def __str__(self):
        return self.name
    
    def count_sales(self):
        return Order.objects.filter(offer_name=self.name, payment_key='HAS_PAID').count()