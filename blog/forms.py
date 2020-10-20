from django import forms
from .models import User, Post


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
