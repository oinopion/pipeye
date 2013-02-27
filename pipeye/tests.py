from expecter import expect
from pipeye.utils.testing import ViewTestCase
from pipeye.utils.urls import url_lazy


class HomeViewTest(ViewTestCase):
    url = url_lazy('home')

    def test_renders_template(self):
        resp = self.get()
        self.assertTemplateUsed(resp, 'home.html')

    def test_response_is_ok(self):
        resp = self.get()
        expect(resp).is_success()
