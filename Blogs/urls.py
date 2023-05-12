from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('sign-up', views.sign_up, name="sign_up"),
    path('create-post', views.create_post, name="create_post"),
    path('leave-comment/<int:post_pk>/', views.leave_comment, name="leave-comment"),
    path('post-details/<int:pk>/', views.post_details, name="post-details"),
    path('profile', views.profileView, name="profile"),
    path('saved_posts', views.saved_posts_list, name="saved_post"),
    path('save-post', views.savePost, name="save_post"),

]
