from django.test import TestCase
from django.template import Template, Context
from django.test.client import RequestFactory
from expecter import expect
from pipeye.packages.tests.factories import PackageFactory
from pipeye.accounts.tests.factories import UserFactory
from pipeye.watches.tests.factories import WatchFactory

class WatchButtonTagTest(TestCase):
    TAG_HTML = "{% load watches_tags %}{% watch_button package %}"

    def render(self, context):
        template = Template(self.TAG_HTML)
        context['request'] = RequestFactory().get('/')
        return template.render(Context(context))

    def test_displays_watch_button(self):
        package = PackageFactory.create()
        user = UserFactory.create()
        html = self.render({'user': user, 'package': package})
        expect(html).contains('Watch this package')

    def test_displays_unwatch_button(self):
        watch = WatchFactory.create()
        html = self.render({'user': watch.user, 'package': watch.package})
        expect(html).contains('Stop watching this package')
