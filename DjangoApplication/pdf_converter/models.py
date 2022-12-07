from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    pass


class Resume(models.Model):
    filename = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d")
    contacts = models.TextField(blank=True)
    education = models.TextField(blank=True)
    awards = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    username = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def get_first_letters(self):
        ls = self.name.split(' ')
        if len(ls) >= 2:
            return f'{(ls[0][0] + ls[1][0]).upper()}'
        if len(ls) == 1:
            return f'{ls[0][0].upper()}'
        return ''