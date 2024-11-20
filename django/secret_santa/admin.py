from django.contrib import admin
from .models import Group, GiftPreference, Assignment

# Register your models here.

admin.site.register(Group)
admin.site.register(GiftPreference)
admin.site.register(Assignment)
