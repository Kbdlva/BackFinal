from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class Profile(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('__all__')


# class UserEditView(UserChangeForm):
#     class Meta:
#         model = UserProfile
#         fields = ('__all__')


class PostForm(forms.ModelForm):
    file_field = forms.FileField()
    class Meta:
        model = Post
        fields = ["title",  "description", "file_field", "image"]

        # widgets = {
        #     'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'})
        # }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


