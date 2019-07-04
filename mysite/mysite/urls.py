"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
# функция pach() первым аргументом принимает часть пути, вторым — ссылку на функцию-обработчик, третим -

import mainapp.views as mainapp # импортируем функцию обработчик и даём ей псевдоним

urlpatterns = [
    path('', mainapp.main, name='main'),
    # При помощи функции include() мы подключаем еще один файл urls.py,
    # который необходимо создать в папке приложения. Аргумент namespace='products'
    # позволяет обращаться в шаблонах к адресам из подключаемого файла через пространство имен.
    path('products/', include('mainapp.urls', namespace='products')),
    # 'feedback/' - часть пути, mainapp.feedback - функция обработчик
    path('feedback/', mainapp.feedback, name='feedback'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('search/', mainapp.search, name='search'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG: # доступ в режиме отладки к медиафайлам
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # делаем папку MEDIA_ROOT доступной по адресу MEDIA_URL = '/media/'


# На самом деле при работе с запросами в функцию-обработчик всегда по умолчанию передается
# еще дополнительная информация — объект request. Он играет большую роль в Django и является
# в некотором смысле буфером обмена между контроллерами (views.py) и шаблонами (templates).
# Замечание: объект request — это по сути контекстный процессор, который прописан в файле
# settings.py в константе TEMPLATES[“OPTIONS”][“context_processors”] — список, один из элементов
# которого django.template.context_processors.request.
# Необходимо учитывать, что Django сработает на первое совпадение запрашиваемого url-адреса с
# путем из списка. Поэтому если какой-то из адресов обрабатывается не той функцией — просто
# поменяйте местами элементы в urlpatterns.
# Если адрес не подходит ни под одно из выражений — Django вызовет исключение 404.
# Замечание: будьте внимательны к символам «/» в конце адреса — в Django это имеет значение.
