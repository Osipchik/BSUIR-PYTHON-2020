from django.contrib.auth.models import User
from django.test import TestCase
from mixer.backend.django import mixer

from Twitter.forms import SearchForm, CreateTwit, CommentForm


class TestForm(TestCase):

    def setUp(self):
        self.user = mixer.blend(User)

    def test_search_form(self):
        data = {'content': self.user.username}
        form = SearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_CreateTwit_form(self):
        data = {'content': 'ads', 'image': 'media/userpick.webp'}
        form = CreateTwit(data=data)
        self.assertTrue(form.is_valid())

    def test_CommentForm_form(self):
        data = {'content': 'asd'}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())
