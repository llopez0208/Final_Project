
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import SignUpForm, UserProfileForm, PostForm
from .models import UserProfile, Post

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()
    if request.GET.get('q'):
        query = request.GET['q']
        posts = posts.filter(title__icontains=query)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [{"title": post.title, "content": post.content} for post in posts]
        return JsonResponse({"posts": data})
    return render(request, 'post_list.html', {'posts': posts})

def fetch_posts(request):
    posts = Post.objects.all().values('title', 'content', 'author__username')
    return JsonResponse(list(posts), safe=False)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/posts/')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/posts/')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('/posts/')
    return render(request, 'post_confirm_delete.html', {'post': post})
