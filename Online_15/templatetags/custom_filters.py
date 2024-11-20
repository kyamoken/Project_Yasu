from django import template
from Online_15.models import Like, CommentLike

register = template.Library()

@register.filter
def has_liked(user, post):
    return Like.objects.filter(user=user, post=post).exists()

@register.filter
def has_liked_comment(user, comment):
    return CommentLike.objects.filter(user=user, comment=comment).exists()