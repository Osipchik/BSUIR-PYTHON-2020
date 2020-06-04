from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from Twitter.validators import validate_image_file


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    Verified = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)

    description = models.CharField(max_length=160, default='')
    image = models.ImageField(upload_to='user_icons/', default='userpick.webp', blank=True, validators=[validate_image_file])
    header_image = models.ImageField(upload_to='profile_headers/', blank=True, validators=[validate_image_file])

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.user_profile.Verified = instance.is_active
        instance.user_profile.save()


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                            through=Contact,
                            related_name='followers',
                            symmetrical=False))


