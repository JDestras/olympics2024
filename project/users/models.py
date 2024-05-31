from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone

class CustomUser(AbstractUser):
    id_key = models.CharField(max_length=100, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_users_groups',
        related_query_name='custom_user_group'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users_permissions',
        related_query_name='custom_user_permission'
    )
    
   
class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255, default="")
    event_sport = models.CharField(max_length=255, default="")
    event_date = models.DateTimeField(default=timezone.now)
    event_location = models.CharField(max_length=255, default="")
    offer_name = models.CharField(max_length=255)
    adults = models.IntegerField()
    children = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    payment_key = models.CharField(max_length=255, default="")
    QR_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.QR_code:
            data = (
                f"user: {self.user.username}, "
                f"payment_key: {self.payment_key}, "
                f"id_key: {self.user.id_key}, "
                f"transaction_date: {self.date}, "
                f"location: {self.event_location}, "
                f"date: {self.event_date}, "
                f"sport: {self.event_sport}, "
                f"event: {self.event_name}, "
                f"offer: {self.offer_name}, "
                f"adults: {self.adults}, "
                f"children: {self.children}"
            )
            
            self.QR_code.save('qr_code.png', generate_qr_code(data))
        super().save(*args, **kwargs)



def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return File(buffer, name="qr_code.png")