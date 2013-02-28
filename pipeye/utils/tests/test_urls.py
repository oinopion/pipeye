from django.test import TestCase
from expecter import expect
from mock import patch
from ..urls import url, url_lazy


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
