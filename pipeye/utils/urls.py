from django.core import urlresolvers

def url(viewname, *args, **kwargs):
    return urlresolvers.reverse(viewname, args=args, kwargs=kwargs)

def url_lazy(viewname, *args, **kwargs):
    return urlresolvers.reverse_lazy(viewname, args=args, kwargs=kwargs)
