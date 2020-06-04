import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import TestCase


@pytest.mark.django_db
class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend(User, username='asd')

    def test_profile(self):
        length = self.user.user_profile._meta.get_field('description').max_length
        assert length == 160
