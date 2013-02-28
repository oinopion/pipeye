from urllib import urlencode
from django.core import urlresolvers


def url(view_name, *args, **kwargs):
    return urlresolvers.reverse(view_name, args=args, kwargs=kwargs)


def url_lazy(view_name, *args, **kwargs):
    return urlresolvers.reverse_lazy(view_name, args=args, kwargs=kwargs)


def qs_url(view_name, *args, **kwargs):
    if '_qs' in kwargs:
        qs = kwargs.pop('_qs')
    else:
        qs = kwargs.pop('qs', '')
    if isinstance(qs, dict):
        qs = urlencode(qs)
    path = url(view_name, *args, **kwargs)
    return "%s?%s" % (path, qs)
