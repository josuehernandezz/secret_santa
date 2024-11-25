from django.contrib import admin
from .models import Group, GiftPreference, Assignment

# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'admin', 'created_at')  # Fields to display in the list view
    list_filter = ('code', 'created_at', 'admin', 'members')  # Filters to add in the sidebar
    search_fields = ('name', 'code', 'admin__username')  # Searchable fields
    ordering = ('created_at',)  # Default ordering

admin.site.register(Group, GroupAdmin)

class GiftPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'gift')  # Fields to display in the list view
    list_filter = ('group__code', 'group', 'user')  # Filters by group and user
    search_fields = ('group__code', 'user__username', 'group__name')  # Searchable by username and group name

admin.site.register(GiftPreference, GiftPreferenceAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('giver', 'receiver', 'group', 'assigned_at')  # Display these fields
    list_filter = ('group__code', 'group', 'giver', 'receiver')  # Filters by group, giver, and receiver
    search_fields = ('giver__username', 'receiver__username', 'group__name', 'group__code')  # Searchable fields
    ordering = ('assigned_at',)  # Default ordering by assignment date

admin.site.register(Assignment, AssignmentAdmin)
