from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    STATUS = (
        ('regular', 'regular'),
        ('subsciber', 'subsciber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices= STATUS, default='regular')
    description = models.TextField('Description', max_length=500, default='', blank=True)
    
    def __str__(self) :
        return self.username