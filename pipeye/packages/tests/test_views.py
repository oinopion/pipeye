from expecter import expect
from django.core.urlresolvers import reverse_lazy
from pipeye.utils.testing import ViewTestCase
from .factories import PackageFactory

class PackageSearchViewTest(ViewTestCase):
    url = reverse_lazy('package_search')

    def test_filters_by_name(self):
        a = PackageFactory(name='aaa')
        b = PackageFactory(name='bbb')
        resp = self.get(data={'q': 'a'})
        packages = resp.context['packages']
        expect(packages).contains(a)
        expect(packages).does_not_contain(b)


