from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, redirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


# class OrderList(ListView):
#     model = Order
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
#
#     @method_decorator(login_required())
#     def dispatch(self, *args, **kwargs):
#         return super(ListView, self).dispatch(*args, **kwargs)
@login_required
def orderList(request):
    title = 'Заказы'
    orders = Order.objects.filter(user=request.user)
    basket = Basket.objects.filter(user=request.user)

    content = {
        'title': title,
        'orders': orders,
        'basket': basket,
    }

    return render(request, 'ordersapp/order_list.html', content)

@login_required
def orderItemsCreate(request):
    basket_items = Basket.objects.filter(user=request.user)
    if len(basket_items) > 0:
        productItemlist = []
        total_price_order = 0
        order_new = Order()
        order_new.user = request.user
        order_new.save()
        for num in basket_items:
            orderItems_new = OrderItem()
            orderItems_new.order = order_new
            orderItems_new.product = num.product
            orderItems_new.quantity = num.quantity
            orderItems_new.save()
            productItemlist.append(orderItems_new)
            total_price_order += num.product.price * num.quantity
        basket_items.delete()

        userItem = ShopUser.objects.get(pk=order_new.user.pk)

        content = {
            'order_new': order_new,
            'productItemlist': productItemlist,
            'userItem': userItem,
            'total_price_order': total_price_order
        }

        mailfrom = settings.EMAIL_HOST_USER
        mailto = [settings.EMAIL_HOST_USER]
        subject = 'Заказ № {0}'.format(order_new.id)
        message = 'Заказ № {0} Заказчик {1}. Телефон: {2}. Email: {3}'.format(order_new.id, userItem.first_name, userItem.phone, userItem.email)
        send_mail(subject, message, mailfrom, mailto)
        sent = True
        return render(request, 'ordersapp/order_info.html', content)
    else:
        return redirect('ordersapp:orders_list')


@login_required
def orderRead(request, pk):
    title = 'Просмотр заказа'

    basket = Basket.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user, pk=pk)
    orderItems = OrderItem.objects.filter(order__id=pk)
    userItem = ShopUser.objects.get(pk=request.user.pk)
    lengthDict = len(order)

    try:

        if userItem.pk == order[0].user.pk:

            content = {
                'title': title,
                'order': order,
                'basket': basket,
                'orderItems': orderItems
            }

            return render(request, 'ordersapp/order_detail.html', content)

    except IndexError:

            return redirect('ordersapp:orders_list')

# class OrderRead(DetailView):
#     model = Order
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super(OrderRead, self).get_context_data(**kwargs)
#         context['title'] = 'заказ/просмотр'
#         return context
#
#     @method_decorator(login_required())
#     def dispatch(self, *args, **kwargs):
#         return super(DetailView, self).dispatch(*args, **kwargs)


@login_required
def orderDelete(request, pk):
    title = 'Удалить заказа'

    basket = Basket.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user, pk=pk)
    orderItems = OrderItem.objects.filter(order__id=pk)
    userItem = ShopUser.objects.get(pk=request.user.pk)

    try:
        if userItem.pk == order[0].user.pk:
            if request.method == 'POST':
                order[0].delete()
                order[0].save()

                return redirect('ordersapp:orders_list')

    except IndexError:

        return redirect('ordersapp:orders_list')

    content = {'title': title,
               'userItem': userItem,
               'basket': basket,
               'order': order,
               'orderItems': orderItems
               }

    return render(request, 'ordersapp/order_confirm_delete.html', content)

# class OrderDelete(DeleteView):
#     model = Order
#     success_url = reverse_lazy('ordersapp:orders_list')
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)
#
#     @method_decorator(login_required())
#     def dispatch(self, *args, **kwargs):
#         return super(DeleteView, self).dispatch(*args, **kwargs)
