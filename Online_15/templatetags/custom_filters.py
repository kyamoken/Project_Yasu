# Online_15/templatetags/custom_filters.py

from django import template
from Online_15.models import Like

register = template.Library()

@register.filter
def has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()