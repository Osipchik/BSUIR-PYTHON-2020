from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models.signals import post_save

from twits.managers import LikeManager


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeManager()


class Twit(models.Model):
    content = models.TextField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='twits')
    likes = GenericRelation(Like, related_name='likes')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    twit = models.ForeignKey(Twit, on_delete=models.CASCADE, related_name='twit')
    content = models.TextField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like, related_name='likes')
