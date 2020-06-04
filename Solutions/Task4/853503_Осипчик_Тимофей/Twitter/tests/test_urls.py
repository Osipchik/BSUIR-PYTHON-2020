from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Twitter.views import *


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)


    def test_like_url_resolves(self):
        url = reverse('like', kwargs={'id': 1})
        self.assertEquals(resolve(url).func, like_view)

    def test_twit_detail_url_resolves(self):
        url = reverse('twit_detail', kwargs={'twit_id': 1})
        self.assertEquals(resolve(url).func, twit_details)

    def test_create_twit_url_resolves(self):
        url = reverse('create_twit')
        self.assertEquals(resolve(url).func, create_twit)

    def test_get_twits_url_resolves(self):
        url = reverse('get_twits', kwargs={'take': 1, 'start_from_id': 1})
        self.assertEquals(resolve(url).func, get_twits)

    def test_delete_twit_url_resolves(self):
        url = reverse('delete_twit', kwargs={'twit_id': 1})
        self.assertEquals(resolve(url).func, delete_twit)

    def test_restore_twit_url_resolves(self):
        url = reverse('restore_twit', kwargs={'twit_id': 1})
        self.assertEquals(resolve(url).func, restore_twit)

    def test_liked_twits_url_resolves(self):
        url = reverse('liked_twits', kwargs={'take': 1, 'start_from_id': 1, 'user_id': 1})
        self.assertEquals(resolve(url).func, get_liked_twits)

    def test_media_twits_url_resolves(self):
        url = reverse('get_media_twits', kwargs={'take': 1, 'start_from_id': 1, 'user_id': 1})
        self.assertEquals(resolve(url).func, get_media_twits)

    def test_get_user_twits_url_resolves(self):
        url = reverse('get_user_twits', kwargs={'take': 1, 'start_from_id': 1, 'user_id': 1})
        self.assertEquals(resolve(url).func, get_user_twits)


    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_find_by_name_url_resolves(self):
        url = reverse('find_by_name')
        self.assertEquals(resolve(url).func, find_users_by_name)

    def test_find_by_username_url_resolves(self):
        url = reverse('find_by_username')
        self.assertEquals(resolve(url).func, find_users_by_username)


    def test_bookmarks_url_resolves(self):
        url = reverse('bookmarks')
        self.assertEquals(resolve(url).func, bookmarks)

    def test_add_bookmark_url_resolves(self):
        url = reverse('add_bookmark', kwargs={'twit_id': 1})
        self.assertEquals(resolve(url).func, add_bookmark)

    def test_remove_bookmark_url_resolves(self):
        url = reverse('remove_bookmark', kwargs={'twit_id': 1})
        self.assertEquals(resolve(url).func, remove_bookmark)


    def test_create_comment_url_resolves(self):
        url = reverse('create_comment', kwargs={'twit_id': 1})
        self.assertEquals(resolve(url).func, create_comment)

    def test_get_comments_url_resolves(self):
        url = reverse('get_comments', kwargs={'twit_id': 1, 'take': 1, 'start_from_id': 1})
        self.assertEquals(resolve(url).func, get_comments)

    def test_user_comments_url_resolves(self):
        url = reverse('user_comments', kwargs={'take': 1, 'start_from_id': 1, 'user_id': 1, })
        self.assertEquals(resolve(url).func, get_user_comments)
