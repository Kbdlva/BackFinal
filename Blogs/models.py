from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# from taggit.managers import TaggableManager


class UserProfile(models.Model):
    image = models.ImageField(default='profile.png', upload_to='images')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='myprofile')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='profile_images', default='YourBlog/static/images/profile.png', null=True)
    saved = models.ManyToManyField(User, related_name='saveds')
    liked = models.ManyToManyField(User, related_name='likeds')

    def __str__(self):
        return self.title + "\n" + self.description


class File(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files', null=True)
# class SavedPost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# class Category(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name
#     def get_absolute_url(self):
#         return reversed('home')
#
class Tag(models.Model):
    name = models.CharField(max_length=200)
    post = models.ManyToManyField(Post, related_name='post_tags')


# class Chat(models.Model):
#     participants = models.ManyToManyField(User, related_name='chats')
#     created_at = models.DateTimeField(auto_now_add=True)

class Room(models.Model):
    name = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User, related_name='all_chats')

class Message(models.Model):
    chat = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000000)
    file = models.FileField(upload_to="static/")
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
