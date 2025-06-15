from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fullname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    # username is required by AbstractUser, but we use email for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        return self.fullname or self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
