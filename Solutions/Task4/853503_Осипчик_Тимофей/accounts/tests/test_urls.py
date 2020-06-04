from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):

    def test_signup_url_resolves(self):
        url = reverse('accounts:signup')
        self.assertEquals(resolve(url).func, signup_view)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_activate_url_resolves(self):
        url = reverse('accounts:activate', kwargs={'uidb64': '123', 'token': '123'})
        self.assertEquals(resolve(url).func, activate_view)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile', kwargs={'id': 1})
        self.assertEquals(resolve(url).func, profile_view)

    def test_update_image_url_resolves(self):
        url = reverse('accounts:update_image', kwargs={'image_type': 'asd'})
        self.assertEquals(resolve(url).func, update_user_image)

    def test_change_description_url_resolves(self):
        url = reverse('accounts:change_description')
        self.assertEquals(resolve(url).func, change_description)

    def test_follow_url_resolves(self):
        url = reverse('accounts:follow', kwargs={'author_id': 1})
        self.assertEquals(resolve(url).func, follow_view)

    def test_unfollow_view_url_resolves(self):
        url = reverse('accounts:unfollow', kwargs={'author_id': 1})
        self.assertEquals(resolve(url).func, unfollow_view)

    def test_followers_url_resolves(self):
        url = reverse('accounts:followers', kwargs={'user_id': 1})
        self.assertEquals(resolve(url).func, followers)

    def test_following_view_url_resolves(self):
        url = reverse('accounts:following', kwargs={'user_id': 1})
        self.assertEquals(resolve(url).func, following)
