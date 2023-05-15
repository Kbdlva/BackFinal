from django.contrib import admin
from .models import UserProfile, Room, Message, Post, Tag, File
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(File)
