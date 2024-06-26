from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    patronymic = models.CharField(max_length=100, verbose_name='patronymic', **NULLABLE)
    email = models.EmailField(max_length=150, unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='phone number', **NULLABLE)
    position = models.CharField(max_length=100, verbose_name='position', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='city', **NULLABLE)
    avatar = models.ImageField(upload_to='users', verbose_name='profile photo', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='is active', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
