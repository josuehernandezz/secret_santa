# Generated by Django 5.1.2 on 2024-11-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0011_remove_giftpreference_url_alter_giftpreference_gift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftpreference',
            name='gift',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]
