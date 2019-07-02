from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from authapp.models import ShopUser


# Рассмотрим контроллер login. Здесь мы воспользовались
# механизмом форм Django. Форма генерируется автоматически
# на основе соответствующей модели (в данном случае ShopUser).
def login(request):
    title = 'вход'

    # Не вдаваясь в подробности, будем считать, что ShopUserLoginForm(data=request.POST)
    # возвращает html-код классической формы для логина. Если запрос выполнен методом GET,
    # форма будет пустая (так как request.POST равен None)
    # создаем экземпляр класса ShopUserLoginForm (объект формы)
    login_form = ShopUserLoginForm(data=request.POST or None)
    # Если запрос выполнен методом POST, форма будет заполнена данными,
    # которые ввел пользователь на странице. Метод формы is_valid() проверяет
    # их корректность в соответствии с атрибутами модели.
    if request.method == 'POST' and login_form.is_valid():
        # Далее получаем из словаря POST-данных логин и пароль
        username = request.POST['username']
        password = request.POST['password']

        # вызываем встроенную в Django функцию аутентификации:
        # В случае успеха она вернет объект пользователя в переменную user.
        user = auth.authenticate(username=username, password=password)
        # Если пользователь активен
        # (проверяем атрибут модели is_active) —
        # вызываем функцию auth.login(request, user).
        if user and user.is_active:
            # Она пропишет пользователя в объект запроса request.
            auth.login(request, user)
            # возвращаем переадресацию на главную
            return HttpResponseRedirect(reverse('main'))

    # в контент передаем название странице - title, и объект формы login_form
    content = {'title': title, 'login_form': login_form}
    # рендерим - визиализируем в шаблон и возвращаем пользователю
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return render(request, 'authapp/verification.html')
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user) # instance=request.user - это экземпляр(правим конкретного пользователя)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def delete(request, pk):
    title = 'удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()

        return render(request, 'authapp/message_delete_user.html')

    content = {'title': title,
               'user_to_delete': user,
               }

    return render(request, 'authapp/delete.html', content)
