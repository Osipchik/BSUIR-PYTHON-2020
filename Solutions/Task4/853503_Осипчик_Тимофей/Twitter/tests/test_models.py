import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import TestCase


@pytest.mark.django_db
class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend(User, username='asd')
        cls.tweet = mixer.blend('Twitter.Tweet', content='asd', user=cls.user, image='media/userpick.webp')
        cls.comment = mixer.blend('Twitter.Comment', content='asd', user=cls.user, tweet=cls.tweet)

    def test_create_tweet(self):
        length = self.tweet._meta.get_field('content').max_length
        assert length == 235

    def test_comment_tweet(self):
        length = self.comment._meta.get_field('content').max_length
        assert length == 235

