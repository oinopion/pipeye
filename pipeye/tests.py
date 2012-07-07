from django.core.urlresolvers import reverse
from django.test import TestCase

class HomeViewTest(TestCase):
    def get(self):
        url = reverse('home')
        return self.client.get(url)

    def test_renders_template(self):
        resp = self.get()
        self.assertTemplateUsed(resp, 'home.html')

    def test_response_is_ok(self):
        resp = self.get()
        self.assertEqual(200, resp.status_code)
