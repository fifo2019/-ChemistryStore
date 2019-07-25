from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from authapp.models import ShopUser
from django.contrib.auth.decorators import login_required


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {'title': title,
               'login_form': login_form,
               'next': next,
               }

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
            username = request.POST['username']
            password = request.POST['password1']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', content)


@login_required
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


@login_required
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
