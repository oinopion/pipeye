from expecter import expect
from django.core.urlresolvers import reverse_lazy
from pipeye.utils.testing import ViewTestCase
from .factories import WatchFactory


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
