from django.contrib import admin
from .models import ShopUser


class ShopUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShopUser._meta.fields]

    class Meta:
        model = ShopUser


admin.site.register(ShopUser, ShopUserAdmin)
