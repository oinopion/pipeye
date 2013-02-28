from django.test import TestCase
from expecter import expect
from mock import patch
from ..urls import url, url_lazy


@patch('pipeye.utils.urls.urlresolvers')
class UrlTest(TestCase):
    args = ('a1', 'a2')
    kwargs = {'kw1': 'kwarg1', 'kw2': 'kwarg2'}

    def test_passes_args_and_kwargs(self, resolvers):
        url('view_name', *self.args, **self.kwargs)
        resolvers.reverse.assert_called_with('view_name',
                args=self.args, kwargs=self.kwargs)

    def test_returns_result(self, resolvers):
        result = url('view_name')
        expect(result) == resolvers.reverse.return_value


@patch('pipeye.utils.urls.urlresolvers')
class LazyUrlTest(TestCase):
    args = ('a1', 'a2')
    kwargs = {'kw1': 'kwarg1', 'kw2': 'kwarg2'}

    def test_passes_args_and_kwargs(self, resolvers):
        url_lazy('view_name', *self.args, **self.kwargs)
        resolvers.reverse_lazy.assert_called_with('view_name',
                args=self.args, kwargs=self.kwargs)

    def test_returns_result(self, resolvers):
        result = url_lazy('view_name')
        expect(result) == resolvers.reverse_lazy.return_value


