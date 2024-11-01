# Online_15/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, CustomUser

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'Image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'style': 'resize:none;'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=100)
    email = forms.EmailField(label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)