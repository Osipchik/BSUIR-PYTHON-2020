from django.contrib import admin

from accounts.models import UserProfile
from .models import Twit, Comment, Like

admin.site.register(Twit)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UserProfile)
