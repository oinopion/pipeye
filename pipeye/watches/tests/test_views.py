from expecter import expect
from pipeye.utils.urls import url, url_lazy
from pipeye.utils.testing import ViewTestCase
from pipeye.packages.tests.factories import PackageFactory
from .factories import WatchFactory
from ..models import Watch


class WatchesListViewTest(ViewTestCase):
    url = url_lazy('watches_list')

    def test_requires_login(self):
        self.assert_requires_login()

    def test_displays_only_user_watches(self):
        user = self.login()
        own = WatchFactory.create(user=user)
        other = WatchFactory.create()
        resp = self.get()
        watches = resp.context['watches']
        expect(watches).contains(own)
        expect(watches).does_not_contain(other)


class CreateWatchViewTest(ViewTestCase):
    package = None

    def get_url(self):
        if not self.package:
            self.package = PackageFactory.create()
        return url('create_watch', self.package.name)

    def test_requires_login(self):
        self.assert_requires_login()

    def test_creates_watch(self):
        user = self.login()
        resp = self.post()
        expect(resp.status_code)  == 302
        qs = Watch.objects.filter(user=user, package=self.package)
        expect(qs.exists()) == True

    def test_is_indempotent(self):
        watch = WatchFactory.create()
        self.login(watch.user)
        self.package = watch.package
        resp = self.post()
        expect(resp.status_code) == 302


class DeleteWatchViewTest(ViewTestCase):
    package = None

    def get_url(self):
        if not self.package:
            self.package = PackageFactory.create()
        return url('delete_watch', self.package.name)

    def test_requires_login(self):
        self.assert_requires_login()

    def test_deletes_watch(self):
        watch = WatchFactory.create(user=self.login())
        self.package = watch.package
        resp = self.post()
        expect(resp.status_code) == 302
        qs = self.package.watch_set.filter(user=watch.user)
        expect(qs.exists()) == False


