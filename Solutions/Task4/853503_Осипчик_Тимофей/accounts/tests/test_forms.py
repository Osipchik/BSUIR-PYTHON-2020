from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import UserCreateForm, AuthenticateForm, ImageForm, HeaderImageForm, DescriptionForm


class TestForm(TestCase):

    def test_UserCreateForm_form(self):
        data = {'email': 'qweqwe@gmail.com', 'password1': '12345678', 'username': '123', 'first_name': '123'}
        form = UserCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_AuthenticateForm_form(self):
        user = User.objects.create_user('qwe', 'Lrazanchik@gmail.com', 'qwe')
        user.save()
        data = {'username': 'qwe', 'password': 'qwe'}
        form = AuthenticateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_ImageForm_form(self):
        data = {'image': 'media/userpick.webp'}
        form = ImageForm(data=data)
        self.assertTrue(form.is_valid())

    def test_HeaderImageForm_form(self):
        data = {'header_image': 'media/userpick.webp'}
        form = HeaderImageForm(data=data)
        self.assertTrue(form.is_valid())

    def test_DescriptionForm_form(self):
        data = {'description': 'media/userpick.webp'}
        form = DescriptionForm(data=data)
        self.assertTrue(form.is_valid())
