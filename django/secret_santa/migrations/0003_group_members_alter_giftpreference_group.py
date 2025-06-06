# Generated by Django 5.1.2 on 2024-11-16 00:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0002_alter_group_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='secret_santa_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='giftpreference',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift_preferences', to='secret_santa.group'),
        ),
    ]
