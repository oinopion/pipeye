from django.test import TestCase
from expecter import expect
from mock import patch
from ..urls import url, url_lazy, qs_url


class BaseUrlTest(object):
    args = ('a1', 'a2')
    kwargs = {'kw1': 'kwarg1', 'kw2': 'kwarg2'}

    def setUp(self):
        self.patch = patch('pipeye.utils.urls.urlresolvers')
        self.resolvers = self.patch.start()

    def tearDown(self):
        self.patch.stop()


class UrlTest(BaseUrlTest, TestCase):
    def test_passes_args_and_kwargs(self):
        url('view_name', *self.args, **self.kwargs)
        self.resolvers.reverse.assert_called_with('view_name',
                args=self.args, kwargs=self.kwargs)

    def test_returns_result(self):
        result = url('view_name')
        expect(result) == self.resolvers.reverse.return_value


class LazyUrlTest(BaseUrlTest, TestCase):
    def test_passes_args_and_kwargs(self):
        url_lazy('view_name', *self.args, **self.kwargs)
        self.resolvers.reverse_lazy.assert_called_with('view_name',
                args=self.args, kwargs=self.kwargs)

    def test_returns_result(self):
        result = url_lazy('view_name')
        expect(result) == self.resolvers.reverse_lazy.return_value


class QsUrlTest(BaseUrlTest, TestCase):
    def setUp(self):
        super(QsUrlTest, self).setUp()
        self.resolvers.reverse.return_value = '/path/'

    def test_adds_qs_to_url(self):
        result = qs_url('view', qs='a=b')
        expect(result) == '/path/?a=b'

    def test_underscore_qs_substitute(self):
        qs_url('view', qs='kwarg', _qs='a=b')
        self.resolvers.reverse.assert_called_with('view', args=(),
                kwargs={'qs': 'kwarg'})

    def test_qs_as_dict(self):
        result = qs_url('view', qs={'a': 'b'})
        expect(result) == '/path/?a=b'
