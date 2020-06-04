# Generated by Django 3.0.6 on 2020-05-27 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='text',
            field=models.TextField(null=True, verbose_name='Email text'),
        ),
        migrations.AlterField(
            model_name='mail',
            name='topic',
            field=models.CharField(max_length=100, verbose_name='Email Subject'),
        ),
    ]
