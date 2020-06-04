import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, Client
from django.urls import reverse
from mixer.backend.django import mixer

from Twitter.forms import SearchForm
from Twitter.views import *


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user(db):
    return mixer.blend(User, username='test', password='1234')


@pytest.fixture
def tweet(db):
    return mixer.blend('Twitter.Tweet', user=mixer.blend(User), content='qwe')


@pytest.fixture
def comment(db):
    return mixer.blend('Twitter.Comment', user=mixer.blend(User), content='qwe')


@pytest.fixture
def tweets(db):
    user = mixer.blend(User)
    for i in range(20):
        mixer.blend('Twitter.Tweet', user=user, content='qwe')


@pytest.fixture
def users(db):
    return [mixer.blend('Twitter.Tweet', user=mixer.blend(User), content='qwe') for _ in range(20)]


@pytest.fixture()
def client(db):
    return Client()


def test_home(factory, tweets):
    path = reverse('home')
    request = factory.patch(path)
    request.user = AnonymousUser()

    response = home(request)
    assert response.status_code == 200

    request = factory.patch(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    request.user = AnonymousUser()

    response = home(request)
    assert response.status_code == 200


def test_create_twit(factory, client, user):
    path = reverse('create_twit')
    request = factory.post(path)
    request.user = AnonymousUser()
    response = create_twit(request)
    assert response.status_code == 302

    client.force_login(user)
    response = client.post(path, {'content': 'content', 'image': 'media/userpick.webp'})
    assert response.status_code == 200

    client.force_login(user)
    response = client.post(path)
    assert response.status_code == 400


def test_delete_tweet(factory, user, tweet):
    path = reverse('delete_twit', kwargs={'twit_id': 1})
    request = factory.patch(path)
    request.user = AnonymousUser()
    twit_id = tweet.id

    response = delete_twit(request, twit_id=twit_id)
    assert response.status_code == 302
    request.user = user
    response = delete_twit(request, twit_id=twit_id)
    assert response.status_code == 200

    path = reverse('restore_twit', kwargs={'twit_id': twit_id})
    request = factory.patch(path)
    request.user = AnonymousUser()

    response = restore_twit(request, twit_id=twit_id)
    assert response.status_code == 302
    request.user = user
    response = restore_twit(request, twit_id=twit_id)
    assert response.status_code == 200

    request.user = user
    response = delete_twit(request, twit_id=twit_id)
    response = delete_twit(request, twit_id=twit_id)
    assert response.status_code == 201


def test_get_twits(factory, tweets):
    path = reverse('get_twits', kwargs={'take': 10, 'start_from_id': 0})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_twits(request, take=10, start_from_id=0)
    assert response.status_code == 200


def test_get_user_twits(factory, tweets, user):
    path = reverse('get_user_twits', kwargs={'take': 10, 'start_from_id': 0, 'user_id': user.id})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_user_twits(request, take=10, start_from_id=0, user_id=user.id)
    assert response.status_code == 200


def test_get_liked_twits(factory, tweets, user):
    path = reverse('liked_twits', kwargs={'take': 10, 'start_from_id': -1, 'user_id': user.id})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_liked_twits(request, take=10, start_from_id=-1, user_id=user.id)
    assert response.status_code == 200

    path = reverse('liked_twits', kwargs={'take': 10, 'start_from_id': 1, 'user_id': user.id})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_liked_twits(request, take=10, start_from_id=1, user_id=user.id)
    assert response.status_code == 200


def test_get_media_twits(factory, tweets, user):
    path = reverse('get_media_twits', kwargs={'take': 10, 'start_from_id': -1, 'user_id': user.id})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_media_twits(request, take=10, start_from_id=-1, user_id=user.id)
    assert response.status_code == 200


def test_twit_details(factory, tweet):
    path = reverse('twit_detail', kwargs={'twit_id': tweet.id})
    request = factory.get(path)
    request.user = AnonymousUser()

    response = twit_details(request, twit_id=tweet.id)
    assert response.status_code == 200

    request = factory.patch(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    request.user = AnonymousUser()

    response = twit_details(request, twit_id=tweet.id)
    assert response.status_code == 200


def test_search(factory, users):
    path = reverse('search')
    request = factory.get(path)
    request.user = AnonymousUser()

    response = search(request)
    assert response.status_code == 200

    request = factory.patch(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    request.user = AnonymousUser()

    response = search(request)
    assert response.status_code == 200


def test_find_users_by_name(client, user):
    path = reverse('find_by_name')
    mixer.blend(User, username='123')

    response = client.get(path, {'form': SearchForm()})
    assert response.status_code == 404

    response = client.get(path, {'content': '123'})
    assert response.status_code == 200


def test_find_users_by_username(client, user):
    path = reverse('find_by_username')
    mixer.blend(User, username='123')

    response = client.get(path, {'form': SearchForm()})
    assert response.status_code == 404

    response = client.get(path, {'content': '123'})
    assert response.status_code == 200


def test_like_tweet(factory, tweet, user):
    path = reverse('like', kwargs={'id': tweet.id})
    request = factory.post(path)
    request.user = user
    response = like_view(request, id=tweet.id)
    assert response.status_code == 400

    request = factory.post(path, data=json.dumps({'model': 'twit'}), content_type='application/json')
    request.user = user
    response = like_view(request, id=tweet.id)
    assert response.status_code == 200

    response = like_view(request, id=tweet.id)
    assert response.status_code == 200


def test_like_comment(factory, comment, user):
    path = reverse('like', kwargs={'id': comment.id})
    request = factory.post(path, data=json.dumps({'model': 'comment'}), content_type='application/json')
    request.user = user
    response = like_view(request, id=comment.id)
    assert response.status_code == 200


def test_create_comment(factory, client, user, tweet):
    path = reverse('create_comment', kwargs={'twit_id': tweet.id})
    request = factory.post(path)
    request.user = AnonymousUser()
    response = create_comment(request, twit_id=tweet.id)
    assert response.status_code == 302

    client.force_login(user)
    response = client.post(path, {'content': 'content'})
    assert response.status_code == 200


def test_get_comments(factory, tweet):
    for _ in range(10):
        mixer.blend('Twitter.Comment', tweet=tweet)

    path = reverse('get_comments', kwargs={'twit_id': tweet.id, 'start_from_id': 0, 'take': 10})
    request = factory.get(path)
    request.user = AnonymousUser()
    response = get_comments(request, twit_id=tweet.id, start_from_id=0, take=10)
    assert response.status_code == 200


def test_get_user_comments(factory, user, tweet):
    for _ in range(10):
        mixer.blend('Twitter.Comment', tweet=tweet, user=user)

    path = reverse('user_comments', kwargs={'take': 10, 'start_from_id': 0, 'user_id': user.id})
    request = factory.get(path)
    request.user = user
    response = get_user_comments(request, take=10, start_from_id=0, user_id=user.id)
    assert response.status_code == 200


def test_bookmarks(factory, user):
    path = reverse('bookmarks')
    request = factory.get(path)
    request.user = AnonymousUser()
    response = bookmarks(request)
    assert response.status_code == 302

    request.user = user
    response = bookmarks(request)
    assert response.status_code == 200

    request = factory.get(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    request.user = user
    response = bookmarks(request)
    assert response.status_code == 200


def test_add_bookmark(factory, user, tweet):
    path = reverse('add_bookmark', kwargs={'twit_id': tweet.id})
    request = factory.post(path)
    request.user = AnonymousUser()
    response = add_bookmark(request, twit_id=tweet.id)
    assert response.status_code == 302

    path = reverse('add_bookmark', kwargs={'twit_id': 0})
    request = factory.post(path)
    request.user = user
    response = add_bookmark(request, twit_id=0)
    assert response.status_code == 404

    path = reverse('add_bookmark', kwargs={'twit_id': tweet.id})
    request = factory.post(path)
    request.user = user
    response = add_bookmark(request, twit_id=tweet.id)
    assert response.status_code == 200


def test_remove_bookmark(factory, user, tweet):
    path = reverse('remove_bookmark', kwargs={'twit_id': tweet.id})
    request = factory.delete(path)
    request.user = AnonymousUser()
    response = remove_bookmark(request, twit_id=tweet.id)
    assert response.status_code == 302

    path = reverse('remove_bookmark', kwargs={'twit_id': 0})
    request = factory.delete(path)
    request.user = user
    response = remove_bookmark(request, twit_id=0)
    assert response.status_code == 404

    mixer.blend('Twitter.Bookmark', user=user, tweet=tweet)
    path = reverse('remove_bookmark', kwargs={'twit_id': tweet.id})
    request = factory.delete(path)
    request.user = user
    response = remove_bookmark(request, twit_id=tweet.id)
    assert response.status_code == 200

