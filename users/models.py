from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'

    ROLE_CHOICES = [
        (STUDENT, 'Студент'),
        (TEACHER, 'Учитель'),
    ]

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT, verbose_name='Роль')

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
