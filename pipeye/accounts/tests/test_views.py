from expecter import expect
from pipeye.accounts.tests.factories import UserFactory
from pipeye.utils.testing import ViewTestCase
from pipeye.utils.urls import url_lazy


class UserPreferencesViewTest(ViewTestCase):
    url = url_lazy('preferences')

    def test_requires_login(self):
        self.assert_requires_login()

    def test_renders_correct_template(self):
        self.login()
        resp = self.get()
        self.assertTemplateUsed(resp, 'accounts/preferences.html')

    def test_redirects_to_self(self):
        self.login()
        data = UserFactory.attributes()
        resp = self.post(data=data)
        expect(resp).is_redirect()
