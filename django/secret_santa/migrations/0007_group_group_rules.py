# Generated by Django 5.1.2 on 2024-11-20 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0006_group_admin_alter_giftpreference_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_rules',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
