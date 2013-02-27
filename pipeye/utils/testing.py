import expecter
from django.test import TestCase
from pipeye.accounts.tests import factories


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

    def assert_requires_login(self):
        resp = self.get(follow=False)
        expecter.expect(resp).is_redirect()


def is_success(response):
    return response.status_code == 200
expecter.add_expectation(is_success)


def is_redirect(response):
    return response.status_code == 302
expecter.add_expectation(is_redirect)
