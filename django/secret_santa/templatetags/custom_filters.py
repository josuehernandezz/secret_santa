# custom_filters.py
from django import template

register = template.Library()

@register.filter
def has_gift_preference(member, group):
    # This filter checks if the member has a gift preference for the group
    return member.user_gift_preference.filter(group=group).exists()
