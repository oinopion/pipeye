from expecter import expect
from django.test import TestCase
from pipeye.utils.factories import UserFactory
from pipeye.packages.tests.factories import PackageFactory
from ..forms import UserWatchForm


class UserWatchFormTest(TestCase):
    def test_saves_watch_with_user(self):
        user = UserFactory.create()
        package = PackageFactory.create()
        form = UserWatchForm(user=user, data={'package': package.pk})
        watch  = form.save()
        expect(watch.user) == user
