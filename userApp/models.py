from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='users', null=True)
