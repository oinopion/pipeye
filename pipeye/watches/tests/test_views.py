from expecter import expect
from django.core.urlresolvers import reverse_lazy
from pipeye.utils.testing import ViewTestCase
from pipeye.packages.tests.factories import PackageFactory
from .factories import WatchFactory
from ..models import Watch


class WatchesListViewTest(ViewTestCase):
    url = reverse_lazy('watches_list')

    def test_requires_login(self):
        self.assertRequiresLogin()

    def test_displays_only_user_watches(self):
        user = self.login()
        own = WatchFactory.create(user=user)
        other = WatchFactory.create()
        resp = self.get()
        watches = resp.context['watches']
        expect(watches).contains(own)
        expect(watches).does_not_contain(other)


class CreateWatchViewTest(ViewTestCase):
    url = reverse_lazy('create_watch')

    def test_requires_login(self):
        self.assertRequiresLogin()

    def test_creates_watch(self):
        user = self.login()
        package = PackageFactory.create()
        resp = self.post({'package': package.pk})
        expect(resp.status_code)  == 302
        qs = Watch.objects.filter(user=user, package=package)
        expect(qs.exists()) == True
