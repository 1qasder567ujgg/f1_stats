from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import main_view

class MainPageTests(TestCase):
    def test_main_view_status_code(self):
        url = reverse('main_view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_main_url_resolves_main_view(self):
        view = resolve('/')
        self.assertEquals(view.func, main_view)