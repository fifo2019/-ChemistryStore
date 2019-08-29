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


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


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


class OrderRead(DetailView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(DetailView, self).dispatch(*args, **kwargs)
