# Generated by Django 3.0.6 on 2020-05-27 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=120)),
                ('text', models.TextField()),
                ('date', models.DateField(db_index=True, verbose_name='date')),
                ('time', models.TimeField()),
                ('check_send', models.BooleanField(db_index=True, default=False)),
                ('users', models.ManyToManyField(limit_choices_to={'Verified': True}, to='accounts.UserProfile')),
            ],
        ),
    ]
