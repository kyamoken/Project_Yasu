from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ユーザー
    title = models.CharField(max_length=255)  # タイトル
    content = models.TextField()  # 本文
    Image = models.ImageField(upload_to='images/', blank=True, null=True)  # 画像
    posted_at = models.DateTimeField(auto_now_add=True)  # 投稿日時
    likes = models.IntegerField(default=0)  # いいね数
    share_link = models.URLField(blank=True, null=True)  # シェアリンク
    comment_count = models.IntegerField(default=0)  # コメント数


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ユーザー
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 投稿
    content = models.TextField()  # 本文
    posted_at = models.DateTimeField(auto_now_add=True)  # 投稿日時


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ユーザー
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 投稿
    created_at = models.DateTimeField(auto_now_add=True)  # いいね日時

    class Meta:
        unique_together = ('user', 'post')  # ユーザーと投稿の組み合わせは一意
