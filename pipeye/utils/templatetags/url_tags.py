from urllib import urlencode
from django import template

register = template.Library()

@register.simple_tag
def qs(path=None, defaults=None, **query_params):
    if isinstance(path, dict):
        path, defaults = None, path
    if defaults:
        query_params = dict(defaults, **query_params)
    query_string = urlencode(query_params)
    if path:
        return "%s?%s" % (path, query_string)
    return query_string
