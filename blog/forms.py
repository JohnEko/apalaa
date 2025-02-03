from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
   class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'participants']

   # we can use it to make user update the fileds they like to update
class UserForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ['username', 'email']