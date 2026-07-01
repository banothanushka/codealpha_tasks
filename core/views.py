from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile


def feed(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        if 'content' in request.POST:
            content = request.POST.get('content')
            if content:
                Post.objects.create(user=request.user, content=content)
                return redirect('feed')
        
        elif 'comment_text' in request.POST:
            comment_text = request.POST.get('comment_text')
            post_id = request.POST.get('post_id')
            if comment_text and post_id:
                post = get_object_or_404(Post, id=post_id)
                Comment.objects.create(post=post, user=request.user, text=comment_text)
                return redirect('feed')
            
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts})


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('feed')


def profile_view(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'core/profile.html', {'profile_user': user, 'user_posts': user_posts})


def follow_user(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
    user_to_follow = get_object_or_404(User, username=username)
    current_profile = request.user.profile
    
    if current_profile.follows.filter(id=user_to_follow.profile.id).exists():
        current_profile.follows.remove(user_to_follow.profile)
    else:
        current_profile.follows.add(user_to_follow.profile)
        
    return redirect('profile_view', username=username)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')