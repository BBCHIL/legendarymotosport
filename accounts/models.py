from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to='uploaded/accounts',
        default='/static/img/account/user.png',
    )
    is_active = models.BooleanField(default=False)
    is_manufacturer = models.BooleanField(default=False)
    activation_code = models.CharField(
        max_length=25, blank=True
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.username
    
    def create_activation_code(self):
        code = get_random_string(
            length=7,
            allowed_chars='0123456789'
        )
        self.activation_code = code

