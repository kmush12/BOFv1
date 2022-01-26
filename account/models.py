from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)


class Request(models.Model):
    user_from = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,  related_name='user_to', on_delete=models.CASCADE)