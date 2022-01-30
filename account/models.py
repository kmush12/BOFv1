from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)
    def get_absolute_url(self):
        return reverse('account:profile-view', kwargs={'id': self.user.id})
    def get_send_request_url(self):
        return reverse('account:send-request-view', kwargs={'id': self.user.id})


class Request(models.Model):
    user_from = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,  related_name='user_to', on_delete=models.CASCADE)
    def get_accept_request_url(self):
        return reverse('account:accept-request-view', kwargs={'id': self.id})
    def get_decline_request_url(self):
        return reverse('account:decline-request-view', kwargs={'id': self.id})