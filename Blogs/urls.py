from django.urls import path
from . import views
from .views import editProfile

urlpatterns = [
    path('', views.default_view),
    path('home', views.home, name="home"),
    path('sign-up', views.sign_up, name="sign_up"),
    path('create-post', views.create_post, name="create_post"),
    path('leave-comment/<int:post_pk>/', views.leave_comment, name="leave-comment"),
    path('post-details/<int:pk>/', views.post_details, name="post-details"),
    path('profile', views.profileView, name="profile"),
    path('edit-profile', editProfile.as_view(), name="edit-profile"),
    path('saveds', views.saved_posts_list, name="saveds"),
    path('likeds', views.liked_posts_list, name="likeds"),
    path('save-post', views.savePost, name="save_post"),
    path('like-post', views.likePost, name="like_post"),
    path('chat', views.enterRoomPage, name="chat"),
    path('chat/<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name="checkview"),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    # path('get_tags/<int:post_pk>/', views.get_tags, name='get_tags'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='tags'),
    path('messages', views.messages, name='messages'),
    path('all_users', views.all_users, name='all_users'),
]
