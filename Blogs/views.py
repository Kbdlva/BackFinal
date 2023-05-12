from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import RegisterForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment, Like
# Create your views here.

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            comments = Comment.objects.filter(id=post_id)
            if post and (post.author == request.user):
                post.delete()
    return render(request, 'Blogs/home.html', {"posts": posts, "comments": comments },)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()
    # liked = False
    # if request.user.is_authenticated:
    #     liked = Like.objects.filter(user=request.user, post=post).exists()
    # if request.method == 'POST' and 'like' in request.POST:
    #     if not liked:
    #         Like.objects.create(user=request.user, post=post)
    #
    #     else:
    #         Like.objects.filter(user=request.user, post=post).delete()
    #
    #     return redirect('home')


    return render(request, 'Blogs/create_post.html', {"form": form})

def leave_comment(request, post_pk, comment_pk=None):
    post = get_object_or_404(Post, pk=post_pk)

    if comment_pk is not None:
        comment = get_object_or_404(Comment, post_id=post_pk, pk=comment_pk)
    else:
        comment = None
    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect("/home")
    else:
        form = CommentForm()

    return render(request, 'Blogs/commentTest.html',
                  {"form": form,
                   "instance": comment,
                   "model_type": "Comment",
                   "related_instance": post,
                   "related_model_type": "Post"
                   })



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

def profileView(request):
    return render(request, 'Blogs/profile.html')

def get_context_data(self):
        context = super().get_context_data()
        post_comments_count = Comment.objects.filter(post=self.object.id).count()
        post_comments = Comment.objects.filter(post=self.object.id)
        context['form'] = self.form
        context['post_comments'] = post_comments
        context['post_comments_count'] = post_comments_count

        return context
