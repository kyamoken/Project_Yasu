from django.contrib import admin

# Register your models here.
from .models import CustomUser, Post, Comment, Like, CommentLike, Announcement

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentLike)
admin.site.register(Announcement)