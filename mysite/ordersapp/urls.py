import ordersapp.views as ordersapp
from django.urls import re_path, path

app_name="ordersapp"

urlpatterns = [
   re_path(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
   path('create/', ordersapp.orderItemsCreate, name='order_create'),
   path('read/<int:pk>/', ordersapp.OrderRead.as_view(), name='order_read'),
]