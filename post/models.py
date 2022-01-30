from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='post_photos', null=True)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def get_absolute_url(self):
        return reverse('post:post-detail-view', kwargs={'id': self.id})

    def get_like_url(self):
        return reverse('post:post-like-view', kwargs={'id': self.id})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)