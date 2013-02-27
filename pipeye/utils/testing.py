from django.test import TestCase
from expecter import expect
from pipeye.accounts import factories


class ViewTestCase(TestCase):
    url = None

    def get_url(self):
        if self.url is None:
            raise Exception('%s has no URL defined' % self.__class__.__name__)
        return self.url

    def get(self, *args, **kwargs):
        return self.client.get(self.get_url(), *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.client.post(self.get_url(), *args, **kwargs)

    def login(self, user=None):
        if not user:
            user = factories.UserFactory.create()
        name = user.username
        # in tests all users have password set to their username
        self.client.login(username=name, password=name)
        return user

    def assertRequiresLogin(self):
        resp = self.get(follow=False)
        expect(resp.status_code) == 302
