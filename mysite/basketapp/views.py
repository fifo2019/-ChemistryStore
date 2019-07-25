from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def basket(request):
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

    content = {
        'title': title,
        'basket_items': basket_items,
        'basket': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk, *args, **kwargs):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    try:
        count =  int(request.POST.get('name'))

        product = get_object_or_404(Product, pk=pk)

        basket = Basket.objects.filter(user=request.user, product=product).first()

        if not basket:
            basket = Basket(user=request.user, product=product)

        if count > 0:
            basket.quantity += count
            basket.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except ValueError:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)

    if request.method == 'POST':
        basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk):
    try:
        quantity = int(request.POST.get('name'))

        new_basket_item = get_object_or_404(Basket, pk=int(pk))
        basket_count = Basket.objects.filter(user=request.user)

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except ValueError:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))