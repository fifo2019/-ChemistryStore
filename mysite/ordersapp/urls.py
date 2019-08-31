import ordersapp.views as ordersapp
from django.urls import re_path, path

app_name="ordersapp"

urlpatterns = [
   re_path(r'^$', ordersapp.orderList
           , name='orders_list'),
   path('create/', ordersapp.orderItemsCreate, name='order_create'),
   path('read/<int:pk>/', ordersapp.orderRead, name='order_read'),
   path('delete/<int:pk>/', ordersapp.orderDelete, name='order_delete'),
]