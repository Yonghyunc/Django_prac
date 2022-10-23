from django.shortcuts import render, redirect
from django.views.decorators.http import (
    require_safe,
    require_POST,
    require_http_methods,
)
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post

# Create your views here.
@require_safe
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


@require_http_methods(['GET', 'POST'])
@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)


@require_POST
def delete(request, post_pk):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=post_pk)
        post.delete()
    return redirect('posts:index')


@require_http_methods(['GET', 'POST'])
@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'posts/form.html', context)
