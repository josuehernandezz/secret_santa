# Generated by Django 5.1.2 on 2024-11-20 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0009_rename_group_rules_group_rules_group_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftpreference',
            name='gift_list',
        ),
        migrations.RemoveField(
            model_name='giftpreference',
            name='max_price',
        ),
        migrations.AddField(
            model_name='giftpreference',
            name='gift',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='giftpreference',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
