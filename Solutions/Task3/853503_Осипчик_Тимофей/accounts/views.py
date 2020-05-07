from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserCreateForm, AuthenticateForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods


def signup_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.data['first_name']
            user.save()
            # u_profile = UserProfile(user=user, description='user description', follow=user)
            # u_profile.save()
            # asd = u_profile.user
            login(request, user)
            return redirect('home')

    form = UserCreateForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    form = AuthenticateForm()
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('home')


@require_http_methods(['POST'])
@login_required(login_url='/accounts/login/')
def delete_account(request):
    user = auth.get_user(request)
    user.delete()
    return render(request, 'home.html')


@login_required(login_url='/accounts/login/')
def profile(request, id):
    user = User.objects.get(id=id)

    twits = user.twits.all()
    return render(request, 'accounts/profile.html', {'user': user, 'twits': twits})


