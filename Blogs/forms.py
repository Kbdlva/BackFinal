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


# choices = Category.objects.all().values_list('name','name')
#
# choice_list = [('', '' ), ('sport','sport'),('news','news'),('entertainment', 'entertainment' )]
#
# for item in choices:
#     choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title",  "description", "tag"]

        # widgets = {
        #     'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'})
        # }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


