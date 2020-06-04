import pytest
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from six import BytesIO

from accounts.views import login_view


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture
def user(db):
    return mixer.blend(User, username='test', password='1234')


@pytest.fixture()
def client(db):
    return Client()


def test_login_view(factory, user, db, client):
    path = reverse('accounts:login')
    request = factory.get(path)
    request.user = AnonymousUser()

    response = login_view(request)
    assert response.status_code == 200

    user = User.objects.create_user('asd', 'razanchik@gmail.com', 'asd')
    user.save()
    response = client.get(path)
    form = response.context['form']
    data = form.initial
    data['username'] = 'asd'
    data['password'] = 'asd'
    response = client.post(path, data)
    assert response.status_code == 302


def test_logout_view(user, client):
    path = reverse('accounts:logout')
    response = client.post(path)
    assert response.status_code == 302

    client.force_login(user)
    response = client.post(path)
    assert response.status_code == 302


def test_signup(client):
    path = reverse('accounts:signup')
    response = client.get(path)
    assert response.status_code == 200

    response = client.post(path, {'first_name': 'asd', 'username': 'qwe', 'password1': 'qwe', 'email': 'ntavvka@gmail.com'})
    assert response.status_code == 200


def test_followers(client, user):
    path = reverse('accounts:followers', kwargs={'user_id': user.id})
    response = client.get(path)
    assert response.status_code == 200

    response = client.get(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    assert response.status_code == 200


def test_following(client, user):
    path = reverse('accounts:following', kwargs={'user_id': user.id})
    response = client.get(path)
    assert response.status_code == 200

    response = client.get(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    assert response.status_code == 200


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


def test_update_user_image(user, client):
    path = reverse('accounts:update_image', kwargs={'image_type': 'image'})
    response = client.post(path)
    assert response.status_code == 302

    with open('userpick.webp', 'rb') as img:
        image = SimpleUploadedFile('userpick.webp', img.read(), content_type='image/webp')

    client.force_login(user)
    response = client.post(path, {'image': image}, follow=True)
    assert response.status_code == 201

    with open('test.txt', 'rb') as img:
        image = SimpleUploadedFile('test.txt', img.read(), content_type='text/plain')

    client.force_login(user)
    response = client.post(path, {'image': image}, follow=True)
    assert response.status_code == 400


def test_change_description(user, client):
    path = reverse('accounts:change_description')
    response = client.post(path)
    assert response.status_code == 302

    client.force_login(user)
    response = client.post(path)
    assert response.status_code == 400

    client.force_login(user)
    response = client.post(path, {'description': 'asd'})
    assert response.status_code == 201


def test_profile_view(user, client):
    path = reverse('accounts:profile', kwargs={'id': user.id})
    response = client.get(path)
    assert response.status_code == 302

    client.force_login(user)
    response = client.get(path)
    assert response.status_code == 200

    client.force_login(user)
    response = client.get(path, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    assert response.status_code == 200


def test_follow_view(client, user):
    test_user = mixer.blend(User)
    path = reverse('accounts:follow', kwargs={'author_id': test_user.id})
    response = client.post(path)
    assert response.status_code == 302

    client.force_login(user)
    path = reverse('accounts:follow', kwargs={'author_id': 9999})
    response = client.post(path)
    assert response.status_code == 404

    path = reverse('accounts:follow', kwargs={'author_id': test_user.id})
    client.force_login(user)
    response = client.post(path)
    assert response.status_code == 201


def test_unfollow_view(client, user):
    test_user = mixer.blend(User)
    response = client.post(reverse('accounts:unfollow', kwargs={'author_id': test_user.id}))
    assert response.status_code == 302

    client.force_login(user)
    response = client.post(reverse('accounts:unfollow', kwargs={'author_id': 9999}))
    assert response.status_code == 404

    client.force_login(user)
    client.post(reverse('accounts:follow', kwargs={'author_id': test_user.id}))
    client.force_login(user)
    response = client.post(reverse('accounts:unfollow', kwargs={'author_id': test_user.id}))
    assert response.status_code == 201
