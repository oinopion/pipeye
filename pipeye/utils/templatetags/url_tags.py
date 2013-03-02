from urllib import urlencode
from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag(takes_context=True)
def qs(context, path=None, defaults=None, **query_params):
    if isinstance(path, dict):
        path, defaults = None, path
    if defaults:
        query_params = dict(defaults, **query_params)
    qs_url = urlencode(query_params)
    if path:
        qs_url = "%s?%s" % (path, qs_url)
    if context.autoescape:
        qs_url = escape(qs_url)
    return qs_url
