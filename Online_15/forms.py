# Online_15/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, CustomUser, Comment, Announcement


class PostForm(forms.ModelForm):
    class Meta:
        model = Post # どのモデルを使うか記載する
        fields = ['title', 'content', 'Image'] # ここにある３種類の
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'style': 'resize:none;'}), #resizeはテキストエリアのサイズ変更を禁止する
        } # 内容(contentのデザインを変更する部分)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=100)
    email = forms.EmailField(label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']