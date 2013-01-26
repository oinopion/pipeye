from .base import *
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.parse('postgres://localhost/pipeye')
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'debug_toolbar',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'ENABLE_STACKTRACES' : False,
}

try:
    GITHUB_APP_ID = os.environ['GITHUB_APP_ID']
    GITHUB_API_SECRET = os.environ['GITHUB_API_SECRET']
except KeyError:
    raise ImproperlyConfigured('Please provide GitHub app credentials')
