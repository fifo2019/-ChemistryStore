from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(verbose_name='фотография', upload_to='users_avatars', blank='True', default='users_avatars/default.jpg')
    phone = models.CharField(verbose_name='номер телефона', max_length=30)
