import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from . import forms
from .models import Twit, Like, Comment
from django.contrib.auth.models import User, Permission
from django.db.models import Q


def home(request):
    form = forms.CreateTwit()

    user = auth.get_user(request)
    # if user is not None:
    #     twits = []
    #     for i in user.following:
    #         twits += i.twits
    # else:
    twits = Twit.objects.all().order_by('-created_date')
    return render(request, 'home.html', {'name': '12345', 'form': form, 'twits': twits})


def twit_details(request, id):
    twit = Twit.objects.get(id=id)
    return render(request, 'twit_detail.html', {'twit': twit})


@require_http_methods(["POST"])
def search(request):
    form = forms.SearchForm(request.POST)
    if form.is_valid():
        name = form.data['content']
        perm = Permission.objects.get(codename=name)
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()

    form = forms.CreateTwit()
    result = User.objects.all()
    return render(request, 'search.html', {'form': form, 'result': result})


@require_http_methods(["POST"])
def follow(request):
    form = forms.SearchForm(request.POST)
    if form.is_valid():
        name = form.data['content']
        perm = Permission.objects.get(codename=name)
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()

    form = forms.CreateTwit()
    result = User.objects.all()
    return render(request, 'search.html', {'form': form, 'result': result})



@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def create_twit(request):
    form = forms.CreateTwit(request.POST)
    if form.is_valid():
        twit = Twit(user=auth.get_user(request), content=form.cleaned_data['content'])
        twit.save()

    form = forms.CreateTwit()
    twits = Twit.objects.all().order_by('created_date')
    return render(request, 'home.html', {'name': '12345', 'form': form, 'twits': twits})


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def like_view(request, id, model_type):
    model = Twit if model_type == 'twit' else Comment
    obj = model.objects.get(pk=id)

    try:
        like = Like.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
        like.delete()
        result = False
    except Like.DoesNotExist:
        obj.votes.create(user=request.user)
        result = True

    return HttpResponse(
        json.dumps({
            "result": result,
            "like_count": obj.votes.likes().count(),
            "dislike_count": obj.votes.dislikes().count(),
            "sum_rating": obj.votes.sum_rating()
        }),
        content_type="application/json"
    )
