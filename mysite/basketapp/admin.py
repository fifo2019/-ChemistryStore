from django.contrib import admin
from .models import Basket


class BasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Basket._meta.fields]

    class Meta:
        model = Basket


admin.site.register(Basket, BasketAdmin)
