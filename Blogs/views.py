from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .utils import extract_tags
from .forms import RegisterForm, PostForm, CommentForm, Profile
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Tag, Post, Comment, UserProfile, Room, Message, File
import os


@login_required(login_url="/login")
def home(request):
    tags = Tag.objects.all()
    tags_value = []
    for tag in tags:
        tags_value.append({
            'name': tag.name,
            'amount': len(tag.post.all())
        })
    posts = Post.objects.all()
    if request.method == "POST":
        words = request.POST.get('words').split()
        if len(words) > 0:
            posts = set()
            for word in words:
                word = word.lower()
                for post in Post.objects.filter(description__icontains=word):
                    posts.add(post)
                for post in Post.objects.all():
                    if word in post.author.first_name.lower() or word in post.author.last_name.lower() or word in post.author.username.lower():
                        posts.add(post)

    for post in posts:
        if request.user.saveds.filter(pk=post.pk).exists():
            post.is_saved = True
        else:
            post.is_saved = False
        if request.user.likeds.filter(pk=post.pk).exists():
            post.is_liked = True
        else:
            post.is_liked = False
    return render(request, 'Blogs/home.html', {"posts": posts, "tags": tags_value}, )


def posts_by_tag(request, tag_name):
    try:
        tag = Tag.objects.get(name='#'+str(tag_name))
    except Tag.DoesNotExist:
        return redirect('home')
    posts = tag.post.all()
    tags = Tag.objects.all()
    tags_value = []
    for tag in tags:
        tags_value.append({
            'name': tag.name,
            'amount': len(tag.post.all())
        })
    for post in posts:
        if request.user.saveds.filter(pk=post.pk).exists():
            post.is_saved = True
        else:
            post.is_saved = False
        if request.user.likeds.filter(pk=post.pk).exists():
            post.is_liked = True
        else:
            post.is_liked = False

    return render(request, 'Blogs/home.html', {"posts": posts, "tags": tags_value, "tag_name": tag_name}, )

def default_view(request):
    return redirect('home')
def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all()
    is_saved = False
    is_liked = False
    if request.user.saveds.filter(pk=pk).exists():
        print(request.user.saveds.all())
        is_saved = True
    if request.user.likeds.filter(pk=pk).exists():
        print(request.user.likeds.all())
        is_liked = True

    context = {
        'post': post,
        'is_saved': is_saved,
        'is_liked': is_liked,
        'comments': comments
    }
    pf = None
    try:
        pf = post.file.file
    except:
        pf = None


    return render(request, 'Blogs/post.html', {'post': post, 'pf': pf,'comments': comments, 'redirect_page': 'home'})


def saved_posts_list(request):
    user = request.user
    tags = Tag.objects.all()
    tags_value = []
    for tag in tags:
        tags_value.append({
            'name': tag.name,
            'amount': len(tag.post.all())
        })
    posts = user.saveds.all()
    if request.method == "POST":
        words = request.POST.get('words').split()
        if len(words) > 0:
            posts = set()
            for word in words:
                word = word.lower()
                for post in user.saveds.filter(description__icontains=word):
                    posts.add(post)
                for post in user.saveds.all():
                    if word in post.author.first_name.lower() or word in post.author.last_name.lower() or word in post.author.username.lower():
                        posts.add(post)
    for post in posts:
        if request.user.saveds.filter(pk=post.pk).exists():
            post.is_saved = True
        else:
            post.is_saved = False
        if request.user.likeds.filter(pk=post.pk).exists():
            post.is_liked = True
        else:
            post.is_liked = False
    return render(request, 'Blogs/home.html', {"posts": posts, 'redirect_page': 'saveds', 'tags': tags_value}, )


def liked_posts_list(request):
    user = request.user
    tags = Tag.objects.all()
    tags_value = []
    for tag in tags:
        tags_value.append({
            'name': tag.name,
            'amount': len(tag.post.all())
        })
    posts = user.likeds.all()
    if request.method == "POST":
        words = request.POST.get('words').split()
        if len(words) > 0:
            posts = set()
            for word in words:
                word = word.lower()
                for post in user.likeds.filter(description__icontains=word):
                    posts.add(post)
                for post in user.likeds.all():
                    if word in post.author.first_name.lower() or word in post.author.last_name.lower() or word in post.author.username.lower():
                        posts.add(post)
    for post in posts:
        if request.user.saveds.filter(pk=post.pk).exists():
            post.is_saved = True
        else:
            post.is_saved = False
        if request.user.likeds.filter(pk=post.pk).exists():
            post.is_liked = True
        else:
            post.is_liked = False
    return render(request, 'Blogs/home.html', {"posts": posts, 'redirect_page': 'likeds', 'tags': tags_value}, )

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            description = request.POST.get('description')
            tags = extract_tags(description)
            post.author = request.user
            post.save()
            file = File(file=form.cleaned_data.get('file_field'), post=post)
            file.save()
            for tag in tags:
                try:
                    new_tag = Tag.objects.get(name=tag)
                    post.post_tags.add(new_tag.pk)
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag)
                    new_tag.save()
                    post.post_tags.add(new_tag.pk)

            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'Blogs/create_post.html', {"form": form})


def get_posts_by_tag(request, tag):
    res = []
    tag = '#' + str(tag)
    if Tag.objects.filter(name=tag).exists():
        for post in Tag.objects.get(name=tag).post.all():
            res.append(post.description)
        return JsonResponse({'data': res})
    else:
        return redirect('/create-post')


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
            comment.post = post
            comment.user = request.user
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


def get_image_path(relative_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath()))
    return os.path.join(base_dir, relative_path)


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user)
            profile.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def profileView(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = request.user
        if len(first_name) > 0:
            user.first_name = first_name
        if len(last_name) > 0:
            user.last_name = last_name
        if len(email) > 0 and not User.objects.filter(email=email).exists():
            user.email = email
        user.save()
    return render(request, 'Blogs/profile.html')


def get_context_data(self):
    context = super().get_context_data()
    post_comments_count = Comment.objects.filter(post=self.object.id).count()
    post_comments = Comment.objects.filter(post=self.object.id)
    context['form'] = self.form
    context['post_comments'] = post_comments
    context['post_comments_count'] = post_comments_count

    return context


def savePost(request):
    user = request.user
    path = request.POST.get('path')
    if request.method == 'POST':
        if request.POST.get('type') == "0":
            post = user.saveds.get(pk=request.POST.get('pk'))
            user.saveds.remove(post)
        else:
            user.saveds.add(request.POST.get('pk'))
    return redirect('http://127.0.0.1:8000/'+path+'#'+request.POST.get('pk'))


def likePost(request):
    user = request.user
    path = request.POST.get('path')
    if request.method == 'POST':
        if request.POST.get('type') == "0":
            post = user.likeds.get(pk=request.POST.get('pk'))
            user.likeds.remove(post)
        else:
            user.likeds.add(request.POST.get('pk'))
    return redirect('http://127.0.0.1:8000/'+path+'#'+request.POST.get('pk'))


def editProfile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print("cheeeek")
        print(last_name)
        user = request.user
        if len(first_name) > 0:
            user.first_name = first_name
        if len(last_name) > 0:
            user.last_name = last_name
        if len(email) > 0 and not User.objects.filter(email=email).exists():
            user.email = email
        user.save()
    return render(request, 'Blogs/profile.html')


def enterRoomPage(request):
    return render(request, 'chat/enterRoom.html')


def room(request, room):
    room_value = Room.objects.get(pk=room)
    if request.user not in room_value.user.all():
        return redirect("/home")
    user = request.user
    friend = user
    for x in room_value.user.all():
        if x.pk != user.pk:
            friend = x
            break
    return render(request, 'Blogs/messages.html', {'room': room_value, 'friend': friend})


def checkview(request):
    friend = User.objects.get(username=request.POST.get('friend'))

    for room in Room.objects.all():
        print(room.user.all())
        if request.user in room.user.all() and friend in room.user.all():
            return redirect('/chat/' + str(room.pk))
    name = str(request.user.pk) + str(friend.pk)
    new_room = Room.objects.create(name=name)
    new_room.user.add(request.user.pk)
    new_room.user.add(friend.pk)
    new_room.save()
    return redirect('/chat/' + str(new_room.pk))


def send(request):
    message = request.POST['message']
    user = request.user
    room_name = request.POST['room_id']
    room = Room.objects.get(pk=room_name)

    new_message = Message.objects.create(content=message, sender=user, chat=room)
    print(new_message)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(pk=room)

    messages = Message.objects.filter(chat=room_details.id)
    return JsonResponse({"messages": list(messages.values('sender', 'content', 'timestamp'))})


def get_tags(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    tags = post.tags.all()
    return HttpResponse(', '.join(tag.name for tag in tags))


def messages(request):
    chats = []
    return render(request, 'Blogs/messages.html', {'chats': chats})


def all_users(request):
    res = []
    for user in User.objects.all():
        try:
            res.append({'username': user.username, 'image': user.myprofile.image.url})
        except:
            pass
    return JsonResponse({'users': res})
