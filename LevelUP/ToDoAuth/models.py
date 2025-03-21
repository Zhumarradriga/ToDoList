

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from  django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True, verbose_name='Email')
    first_name=models.CharField(max_length=30, blank=True, verbose_name='Имя')
    last_name=models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    phone_number=models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    data_joined=models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff=models.BooleanField(default=False, verbose_name='Сотрудник')

    objects=CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name']
    def __str__(self):
        return  self.email
    @property
    def full_name(self):
        return  f"{self.first_name} {self.last_name}".strip()