# Generated by Django 5.1.2 on 2024-11-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0010_remove_giftpreference_gift_list_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftpreference',
            name='url',
        ),
        migrations.AlterField(
            model_name='giftpreference',
            name='gift',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
