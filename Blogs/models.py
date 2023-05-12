from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    image = models.ImageField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='profile_images', default='YourBlog/static/images/profile.png', null=True)
    tag = models.ManyToManyField('Tag', related_name='tags')
    saved = models.ManyToManyField(User, related_name='saveds')
    liked = models.ManyToManyField(User, related_name='likeds')

    def __str__(self):
        return self.title + "\n" + self.description


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
    post = models.ManyToManyField(Post, related_name='posts')


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField()
    timestamp = models.DateTimeField(auto_now_add=True)
