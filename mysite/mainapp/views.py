from django.shortcuts import render, get_object_or_404
import datetime
from .models import Product, ProductCategory
from basketapp.models import Basket
# В контроллер всегда передается как минимум один аргумент — объект запроса request.
# Мы пользуемся функцией render() из модуля django.shortcuts, которая должна
# получить как минимум два аргумента: объект request (по сути, он через нее пробрасывается в шаблон)
# и путь к шаблону. Внимание: контроллер всегда должен возвращать объект ответа — должен быть return.


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


def products(request, pk=None, page=1):
    print(pk)

    links_menu = ProductCategory.objects.exclude(name='Новинки')

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

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


def feedback(request):
    title = 'Написать нам'

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    content = {'title': title,
               'basket': basket,
               }

    return render(request, 'mainapp/feedback.html', content)
