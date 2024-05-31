from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Order

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('id_key',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('id_key',)}),
    )

    def get_queryset(self, request):
        return CustomUser.objects.all()
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer_name', 'id')

