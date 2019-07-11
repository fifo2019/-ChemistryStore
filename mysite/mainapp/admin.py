from django.contrib import admin
from .models import ProductCategory, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "image", "short_desc", "description", "price"]
    list_filter = ["category"]
    search_fields = ["name", "short_desc", "description", "price"]

    class Meta:
        model = Product


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

    class Meta:
        model = ProductCategory



admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
