from django.template import Template, Context
from django.test import TestCase
from expecter import expect


class QsTagTest(TestCase):
    def test_adds_query_string(self):
        template = "{% qs '/path/' q='Django' %}"
        self.expect_to_render(template, {}, '/path/?q=Django')

    def test_works_with_variables(self):
        template = "{% qs url q=query %}"
        context = dict(url='/path/', query='Django')
        self.expect_to_render(template, context, '/path/?q=Django')

    def test_works_with_default_parameters(self):
        template = "{% qs '/path/' params %}"
        context = dict(params={'q': 'Django'})
        self.expect_to_render(template, context, '/path/?q=Django')

    def test_works_without_path(self):
        template = "{% qs q='Django' %}"
        self.expect_to_render(template, {}, 'q=Django')

    def test_detects_defaults_and_no_path(self):
        template = "{% qs params %}"
        context = dict(params={'q': 'Django'})
        self.expect_to_render(template, context, 'q=Django')

    def test_params_override_defaults(self):
        template = "{% qs params page=3 %}"
        context = dict(params={'page': 1})
        self.expect_to_render(template, context, 'page=3')

    def expect_to_render(self, template, context, expected_result):
        result = self.render(template, context)
        expect(result) == expected_result

    def render(self, template_fragment, context):
        template = "{% load url_tags %}" + template_fragment
        return Template(template).render(Context(context))
