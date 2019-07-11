from django.shortcuts import render, get_object_or_404
import datetime
from .models import Product, ProductCategory
from basketapp.models import Basket
from random import random, sample
from django.db.models import Q
from django.views import View

# В контроллер всегда передается как минимум один аргумент — объект запроса request.
# Мы пользуемся функцией render() из модуля django.shortcuts, которая должна
# получить как минимум два аргумента: объект request (по сути, он через нее пробрасывается в шаблон)
# и путь к шаблону. Внимание: контроллер всегда должен возвращать объект ответа — должен быть return.


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def main(request):
    title = 'Главная'
    links_menu = ProductCategory.objects.exclude(name='Новинки')
    products = Product.objects.filter(category__name='Новинки')

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    content = {'title': title,
               'links_menu': links_menu,
               'products': products,
               'basket': basket,
               }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.exclude(name='Новинки')
    basket = get_basket(request.user)

    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category__pk=pk).order_by('price')
    title = '{0}'.format(category.name)
    
    content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'products': products,
        'basket': basket,
    }

    return render(request, 'mainapp/products_list.html', content)


def product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    title = '{0}'.format(product.name)

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.exclude(name='Новинки'),
        'product': product,
        'same_products': Product.objects.filter(category__pk=product.category.pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)


def feedback(request):
    title = 'Написать нам'

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    content = {'title': title,
               'basket': basket,
               }

    return render(request, 'mainapp/feedback.html', content)


def search(request, *args, **kwargs):

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    query = request.GET.get('q')
    search_product = Product.objects.filter(
        Q(name__icontains=query)|
        Q(name__istartswith=query)|
        Q(short_desc__icontains=query)|
        Q(short_desc__istartswith=query)|
        Q(description__icontains=query)|
        Q(description__istartswith=query)
    )

    contextOne = {
        'search_product': search_product,
        'links_menu': ProductCategory.objects.exclude(name='Новинки'),
        'basket': basket,
    }

    contextTwo = {
        'links_menu': ProductCategory.objects.exclude(name='Новинки'),
        'basket': basket,
    }

    if query == '':
        return render(request, 'mainapp/search.html', contextTwo)
    else:
        return render(request, 'mainapp/search.html', contextOne)