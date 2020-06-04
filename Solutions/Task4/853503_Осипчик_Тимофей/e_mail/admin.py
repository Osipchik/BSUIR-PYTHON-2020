from django.contrib import admin
from e_mail.models import Mail


class CollectionMail(admin.ModelAdmin):
    filter_vertical = ('users',)


admin.site.register(Mail, CollectionMail)
