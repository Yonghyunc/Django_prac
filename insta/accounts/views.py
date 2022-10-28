from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.decorators.http import (
    require_safe,
    require_POST,
    require_http_methods,
)
from django.contrib.auth.decorators import login_required
from .models import User, Profile


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'posts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
@login_required()
def delete(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.delete()
            auth_logout(request)
            return redirect('posts:index')
        else:
            return render(request, 'accounts/delete.html')
    else:
        return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
@login_required()
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@require_http_methods(['GET', 'POST'])
@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('posts:index')

    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)


@require_safe
def profile(request, user_name):
    user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=user.pk)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_update(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('accounts:login')
