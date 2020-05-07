from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    description = models.CharField(max_length=160, default='')
    image = models.ImageField(upload_to='profile_image', blank=True)
    header_image = models.ImageField(upload_to='header_image', blank=True)
    following = models.ForeignKey(User, related_name='following', on_delete=models.DO_NOTHING)
    # followers = models.ForeignKey(User, related_name='followers', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user_profile = UserProfile.objects.create(user=user, following=user)


post_save.connect(create_profile, sender=User)
