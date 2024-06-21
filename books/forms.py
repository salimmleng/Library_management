from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms 
from .models import Review


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','comment']

